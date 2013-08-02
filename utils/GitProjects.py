#!/usr/bin/env python

from git import *
import os, optparse, sys

class GitColors:
    UP_TO_DATE = '\033[92m'
    HAVE_CHANGES = '\033[91m'
    END = '\033[0m'

def printChanges(repo):
    print "\tFiles with changes:"

    index = repo.index
    diffs = index.diff(None)

    for diff in diffs:
        print "\t\t" + diff.a_blob.path

    if len(repo.untracked_files) > 0:
        print "\tUntracked files:"
        for file in repo.untracked_files:
            print "\t\t" + file

    print ""

def checkForChanges(projects):
    for project in projects:
        repo = None
        try:
            repo = Repo(os.path.join(os.getcwd(), project))

            if repo.is_dirty(True, True, True):
                print project + " - " + GitColors.HAVE_CHANGES + "have changes" + GitColors.END
                printChanges(repo)
            elif not repo.is_dirty(True, True, True):
                print project + " - " + GitColors.UP_TO_DATE + "up-to-date" + GitColors.END

        except InvalidGitRepositoryError:
            print project + " is not a valid git repository"

def pull(projects):
    for project in projects:
        repo = None
        try:
            repo = Repo(os.path.join(os.getcwd(), project))

            origin = repo.remote()
            origin.pull()

        except InvalidGitRepositoryError:
            print project + " is not a valid git repository"

def fetch(projects):
    for project in projects:
        repo = None
        try:
            repo = Repo(os.path.join(os.getcwd(), project))

            origin = repo.remote()
            origin.pull()

        except InvalidGitRepositoryError:
            print project + " is not a valid git repository"

def main():
    parser = optparse.OptionParser(version="0.1", epilog="Git for multiple repos", description="GPL")
    parser.add_option("-s", "--status", dest="status", action="store_true")
    parser.add_option("-l", "--pull", dest="pull", action="store_true")
    parser.add_option("-f", "--fetch", dest="fetch", action="store_true")

    (opts, args) = parser.parse_args(sys.argv)

    projects = []
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir[0] == '.':
            projects.append(dir)

    if opts.status:
        checkForChanges(projects)

    if opts.pull:
        pull(projects)

    if opts.fetch:
        fetch(projects)

if __name__ == "__main__":
    main()
