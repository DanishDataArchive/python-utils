#!/usr/bin/env python

import getopt, sys, os, zipfile

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:j:", ["class=", "jars="])

    except getopt.GetoptError as err:
        print str(err)

    lines = []
    classes = dict()
    classToFind = ""

    for o, a in opts:
        if o in ("-c", "--class"):
            classToFind = a.strip()
        elif o in ("-j", "--jars"):
            jars = open(a)
            for line in jars.readlines():
                lines.append(line.rstrip("\n"))
            jars.close()

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
        zFile.close()

    if classes.has_key(classToFind):
        for line in classes[classToFind]:
            print line
    else:
        print "Not found"