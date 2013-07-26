#!/usr/bin/env python

import magic, getopt, sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:f:m", ["bytes=", "file=", "mime"])
    except getopt.GetoptError as err:
        print str(err)

    bytes = 10
    file = ""
    mime = False

    for o, a in opts:
        if o in ("-f", "--file"):
            file = a
        elif o in ("-m", "--mime"):
            mime = True
        elif o in ("-b", "--bytes"):
            bytes = int(a)

    if len(file) > 0:
        print magic.from_buffer(open(file).read(bytes), mime)
    else:
        print "Please specify a file"

if __name__ == "__main__":
    main()
