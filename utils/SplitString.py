#!/usr/bin/env python

import sys, pkg_resources

from optparse import OptionParser

def main():
    parser = OptionParser(version=pkg_resources.require("py-utils-dda")[0].version, epilog="Split a string with a delimiter", description="GPL")
    parser.add_option("-s", "--string", dest="string", action="store", type="string")
    parser.add_option("-d", "--delimiter", dest="delimiter", action="store", type="string")

    (opts, args) = parser.parse_args(sys.argv)

    delimiter = ":"
    line = ""

    if opts.string:
        line = opts.string

    if opts.delimiter:
        delimiter = opts.delimiter

    if(len(line) == 0):
        print "Please pass a string"
        sys.exit(-1)

    splits = line.split(delimiter)

    for split in splits:
        print split

if __name__ == "__main__":
    main()
