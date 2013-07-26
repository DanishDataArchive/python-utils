#!/usr/bin/env python

import getopt, sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:d:", ["string=", "delimiter="])
    except getopt.GetoptError as err:
        print str(err)
    
    delimiter = ":"
    line = ""
    
    for o, a in opts:
        if o in ("-d", "--delimiter"):
            delimiter = a
        elif o in ("-s", "--string"):
            line = a
    
    if(len(line) == 0):
        print "Please pass a string"
        sys.exit(-1)
        
    splits = line.split(delimiter)
    
    for split in splits:
        print split

if __name__ == "__main__":
    main()
