#!/usr/bin/env python

import sys, os, pkg_resources

from optparse import OptionParser

class FileColors:
    EXISTS = '\033[92m'
    DOES_NOT_EXISTS = '\033[91m'
    END = '\033[0m'

def checkIfFileExists(file):
    if os.path.isfile(file):
        print file + (FileColors.EXISTS + " exists" + FileColors.END if os.path.exists(file) else FileColors.DOES_NOT_EXISTS + " does not exist" + FileColors.END)
    else:
        print FileColors.DOES_NOT_EXISTS + file + " is not a file" + FileColors.END

def checkIfFilesExists(files):
    for file in files:
        checkIfFileExists(file)

def main():
    lines = []

    parser = OptionParser(version=pkg_resources.require("py-utils-dda")[0].version, epilog="Check if files exists", description="GPL")
    parser.add_option("-f", "--files", dest="files", action="store", type="string")

    (opts, args) = parser.parse_args(sys.argv)

    if opts.files:
        files = open(opts.files)
        for line in files.readlines():
            lines.append(line.rstrip("\n"))
        files.close()

    if len(lines) == 0:
        for line in sys.stdin:
            lines.append(line.rstrip("\n"))

    if len(lines) == 0:
        print "Please provide some files to check for"

    checkIfFilesExists(lines)    

if __name__ == "__main__":
    main()
