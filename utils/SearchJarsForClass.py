#!/usr/bin/env python

import getopt, sys, os, zipfile

def printUsage():
    print os.path.basename(sys.argv[0]) + ", search a number of jar files for class\n"
    print "-c or --class\t\tclass to find"
    print "-j or--jars\t\tfile container location of the jars, alternatively you can specify on stdin"
    print "-v or --verbose\t\tshow which classes are in the jars"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:j:v", ["class=", "jars=", "verbose"])

    except getopt.GetoptError as err:
        print str(err)

    lines = []
    classes = dict()
    classToFind = ""
    verbose = False

    for o, a in opts:
        if o in ("-c", "--class"):
            classToFind = a.strip()
        elif o in ("-j", "--jars"):
            jars = open(a)
            for line in jars.readlines():
                lines.append(line.rstrip("\n"))
            jars.close()
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            printUsage()

    if len(lines) == 0:
        for line in sys.stdin:
            lines.append(line.rstrip("\n"))

    if len(lines) == 0:
        print "Please provide jars to search"
        sys.exit(-1)

    for file in lines:
        zFile = zipfile.ZipFile(file)

        for filename in zFile.namelist():
            if filename.endswith(".class"):
                key = filename.replace('/', '.').replace(".class", "").strip()
                if classes.has_key(key):
                    classes[key].append(file + "!" + filename)
                else:
                    classes[key] = [file + "!" + filename]

                if verbose:
                    print "Added " + file + "!" + filename
        zFile.close()

    if classes.has_key(classToFind):
        for line in classes[classToFind]:
            print line
    else:
        print "Not found"

if __name__ == "__main__":
    main()
