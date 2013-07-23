#!/usr/bin/env python

import getopt, sys, os

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

if __name__ == "__main__":
    lines = []
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:", ["files="])

    except getopt.GetoptError as err:
        print str(err);

    for o, a in opts:
        if o in ("-f", "--files"):
            files = open(a)
            for line in files.readlines():
                lines.append(line.rstrip("\n"))
            files.close()

    if len(lines) == 0:
        for line in sys.stdin:
            lines.append(line.rstrip("\n"))

    if len(lines) == 0:
        print "Please provide some files to check for"
    
    checkIfFilesExists(lines)    
