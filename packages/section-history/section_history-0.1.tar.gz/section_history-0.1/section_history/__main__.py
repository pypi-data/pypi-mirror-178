from collections import namedtuple
from dataclasses import dataclass
from operator import indexOf
import sys
import glob
import os
from time import sleep
from rich import print as rprint
from section_history.console import console
from section_history.colored_output import get_edits_string
from textwrap import indent
from more_itertools import pairwise
from pathlib import Path
from git.repo import Repo
from section_history.entry import Entry
from datetime import datetime
import typer
from typing import Optional
from rich.progress import Progress, track
import time

from section_history.cache import Cache, StoreResult, CacheStatus
import time
from configparser import ConfigParser


def _check_path_in_directory(repo, dir_path, path):
    subdirectory = str(dir_path)[len(str(repo.working_dir)) + 1 :]
    return True if subdirectory in path else False


def _get_changed_files_and_their_status(repo, dir_path, commit1, commit2):
    StatusAndPath = namedtuple("StatusAndPath", ["status", "path"])
    diff_strings = repo.git.diff(commit2.hexsha, commit1.hexsha, "--name-status").split(
        "\n"
    )
    # D mypath.md
    # A mypath2.md
    return_values = []
    for diff_string in diff_strings:
        status = diff_string.split("\t")[0]
        path = diff_string.split("\t")[-1]
        if _check_path_in_directory(repo, dir_path, path):
            return_values.append(StatusAndPath(status, path))
    return return_values


def _get_changes_in_commit(repo, commit, file_path, regex, entries):
    try:
        file_text = repo.git.execute(["git", "show", f"{commit.hexsha}:{file_path}"])
    except Exception as e:
        # Fatal bad object error resulting from trying to execute git show on a submodule
        # Decided to ignore the error if it's a directory
        # if dir
        if not Path(file_path).is_file():
            return
        raise Exception("Unexpected error when executing git show")  # pragma: no cover

    for entry in Entry.parse(file_path, file_text, commit, regex):

        entry_id_found = False
        if entries == []:
            entries.append(entry)
        else:
            # reversed to not throw off indecies when deleting
            for x in reversed(entries):
                if entry.id == x.id:
                    entry_id_found = True
                    # compare entry texts not accounting for whitelines
                    if "".join(entry.text.split()) != "".join(x.text.split()):
                        entries.append(entry)
                    else:
                        # if text is the same we replace the entry
                        # with the entry further back in the commit history
                        index = entries.index(x)
                        entries[index] = entry
                    break
            if entry_id_found == False:
                entries.append(entry)


class _Commit(object):
    def __init__(self, hexsha):
        self.hexsha = hexsha


def add_to_cache(repo, path, cache, regex):
    """Create or add to the cache of the history of sections

    Parameters
    ----------
    repo : `Repo`
        Repo object containing information on the repository containing the sections to be added to the cache
    path : `str`
        String of the path to the code containing the sections to be added to the cache
    cache : `Cache`
        Cache object which specifies the cache where the history of different sections is stored
    regex : `str`
        String of the regular expression which matches the sections of which history will be added to the cache
    """
    entries = []
    all_commits = list(repo.iter_commits(paths=path))

    # Add the empty tree sha to the list of all commits
    EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    empty_commit = _Commit(EMPTY_TREE_SHA)
    all_commits.append(empty_commit)

    commit_tuples = list(pairwise(all_commits))

    with Progress(transient=True) as progress:
        task = progress.add_task(
            "Going through commit history...",
            total=len(commit_tuples),
        )
        while not progress.finished:
            # ALL OTHER COMMITS - Go through all commits in directory pairwise and adds the requirement to the cache if it has changed since last commit.
            # Note: Looping through all kind of files, optimisation might be to only look though for specific file types
            for commit1, commit2 in commit_tuples:
                # If commit has been added to the cache we exit the for loop
                # Okay since we add to the cache in the end of this function
                # Thus if the process was ended mid run we will never have a partially filled cache
                if (
                    cache.check_commit_in_cache(commit1.hexsha)
                    == StoreResult.ALREADY_STORED
                ):
                    progress.remove_task(task)
                    break
                """
                # Outputs the list of files in the commit provided in the second argument to git diff
                diff = repo.git.diff(commit2.hexsha, commit1.hexsha, "--name-only")
                changed_paths = diff.splitlines()
                # If files outside the subdirectory were changed in the same commit they are also included
                # Remove them by calling check_subdirectory
                changed_paths = filter_include_only_files_in_subdirectory(
                    repo, path, changed_paths
                )
                """
                # Function solves conflicts regarding removed files in merge. With name status we see which ones are deleted,
                # we remove these from changed_paths as to not look for a file that does not exist.
                for return_value in _get_changed_files_and_their_status(
                    repo, path, commit1, commit2
                ):
                    status, file_path = return_value
                    if status == "D":
                        continue
                    _get_changes_in_commit(repo, commit1, file_path, regex, entries)
                progress.update(task, advance=1)

    for entry in track(entries, description="Adding to cache..."):
        cache.store(entry)


def get_history(req_id, cache):
    """Retrieve the history of a specific section from the cache.

    Parameters
    ----------
    req_id : `str`
        String whose value should be a unique id of a section
    cache : `Cache`
        Cache object which specifies the cache where the history of different sections is stored

    Returns
    -------
    history : `list` [`Entry`]
        A list of Entry objects relating the history of the section specified by the req_id located in the given cache
    """
    # Retrieves the cached entries with the matching Requirement id
    if req_id == None:
        raise typer.BadParameter("Missing argument 'REQ_ID'")
    history = cache.get_cached_history(req_id)
    return history


def _get_regex_from_config_file(repo_path):
    config_file_path = Path(repo_path) / "config.ini"
    cfg = ConfigParser()

    # Check if configuration file exists
    if not os.path.isfile(config_file_path):
        raise Exception("config.ini does not exist in target root directory")

    cfg.read(config_file_path)

    # Check if configuration file correctly formatted
    try:
        regex_val = cfg["regex_section"]["regex_val"]
    except KeyError as e:
        raise Exception("config.ini not formatted correctly")
    return regex_val


def parse_entry_output(entries, highlight_diff):
    """Display entries in console with different highlighting formatted

    Parameters
    ----------
    entries : `list` [`Entry`]
        A list of Entry objects relating the history of a specific section
    highlight_change : `boolean`
        A boolean value which if true the change in the text of the section will be highlighted
    """
    previous_entry = ""
    for entry in reversed(entries):
        # Meta data
        rprint(entry)

        # Text
        if highlight_diff:
            if previous_entry == "":
                print(indent(get_edits_string("", entry.text), "    "))
            else:
                print(indent(get_edits_string(previous_entry.text, entry.text), "    "))
        else:
            print(indent(entry.text, "    "))
        previous_entry = entry


def main(
    path: str = typer.Argument(Path.cwd()),
    req_id: Optional[str] = typer.Argument(None),
    highlight_diff: bool = typer.Option(
        True, " /--no-diff", help="Markup of requirement changes in the output "
    ),
    update_cache: bool = typer.Option(False, help="Update the global cache"),
    cache_path: str = typer.Option("", help="Specify the path to cache directory"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force update the cache. Must include the update-cache flag as well.",
    ),
):
    # Initiates and check if repo
    try:
        repo = Repo(path, search_parent_directories=True)
    except Exception as e:
        if e.__class__.__name__ == "NoSuchPathError":
            raise Exception("Path does not exist")
        if e.__class__.__name__ == "InvalidGitRepositoryError":
            raise Exception("Path is not a repository")
        raise Exception("Other path error")  # pragma: no cover

    root_path = repo.working_tree_dir

    # Gets regex to identify a section. Specified in config file in root directory of target repo.
    regex = _get_regex_from_config_file(root_path)

    if cache_path:
        cache = Cache(cache_path)
    else:
        # Initates cache in the target repo root directory
        cache = Cache(root_path)

    # Adds all the reqs in the directory specified to the cache
    if update_cache:
        # Force update cache, i.e. remove the cache and then add the entries anew
        if force:
            cache.remove_cache()
        add_to_cache(repo, path, cache, regex)
    # Fetch the history for a given requirement id
    else:
        if cache.check_cache_empty() == CacheStatus.EMPTY:
            add_to_cache(repo, path, cache, regex)
        entries = get_history(req_id, cache)
        if type(entries) != str:
            parse_entry_output(entries, highlight_diff)
        if len(entries) == 0:
            print(
                "The provided regex and ID did not match any sections in the directory."
            )
        return entries


if __name__ == "__main__":
    typer.run(main)
