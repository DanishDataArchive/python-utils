#!/usr/bin/env python

import sys, os, pkg_resources, shutil

from optparse import OptionParser

class FileColors:
    EXISTS = '\033[92m'
    DOES_NOT_EXISTS = '\033[91m'
    END = '\033[0m'

def copyFile(src, dest):
        shutil.copy2(src, dest)

def copyFiles(files, dest):
    for file in files:
        sfile = os.path.join(os.getcwd(), file)
        if os.path.exists(sfile):
            filename = os.path.basename(sfile)
            pathToFile = file[:len(file)-len(filename)]

            if not os.path.exists(os.path.join(dest, pathToFile)):
                os.makedirs(os.path.join(dest, pathToFile))

            copyFile(sfile, os.path.join(dest, pathToFile))
        else:
             print sfile + " doesn't exists"

def main():
    lines = []

    parser = OptionParser(version=pkg_resources.require("py-utils-dda")[0].version, epilog="Copy a bunch of files", description="GPL")
    parser.add_option("-f", "--force", dest="force", action="store_true", default=False)
    parser.add_option("-s", "--file-sources", dest="files", action="store", type="string")
    parser.add_option("-d", "--destination", dest="dest", action="store", type="string")

    (opts, args) = parser.parse_args(sys.argv)

    if not opts.dest:
        print "Please provide a destination"
        sys.exit(-1)

    elif not os.path.exists(opts.dest):
        print FileColors.DOES_NOT_EXISTS + "" + opts.dest + " doesn't exist" + FileColors.END

        if opts.force:
            print "Creating destination"
            os.makedirs(opts.dest)
        else:
            print "Use -f to create the directory"            
            sys.exit(-1)

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

    copyFiles(lines, opts.dest)    

if __name__ == "__main__":
    main()
