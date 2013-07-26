#!/usr/bin/env python

import magic, getopt, sys, os

def printUsage():
    print os.path.basename(sys.argv[0]) + ", looks at file, tries to identify the file type\n"
    print "-f or --file\t\tThe file to inspect"
    print "-m or --mime\t\tPrint the mime-type instead"
    print "-b or --bytes\t\tNumber of bytes to use in inspection"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:f:hm", ["bytes=", "file=", "help", "mime"])
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
        elif o in ("-h", "--help"):
            printUsage()
            sys.exit(0)

    if len(file) > 0:
        print magic.from_buffer(open(file).read(bytes), mime)
    else:
        print "Please specify a file"

if __name__ == "__main__":
    main()
