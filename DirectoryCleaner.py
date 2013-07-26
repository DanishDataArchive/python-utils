#!/usr/bin/env python

import getopt, sys, os, time, shutil, syslog

cron = False
test = False
verbose = False

def usage():
    print "Directory Cleaner, cleans a directory for sub directories, starting with the oldest\n"
    print "-c or --cron\t\tIn cron mode, be quiet"
    print "-d or --dir\t\tDirectory to clean"
    print "-h or --help\t\tShows this help"
    print "-m or --max-dirs\tThe maximum number of dirs to keep (default = 10)"
    print "-t or --test\t\tTest the params --- DOES NOT EXECUTE COMMANDS"
    print "-v or --verbose\t\tVerbose, tell which files are being deleted"

def log(message):
    if verbose and not cron:
        print message

    syslog.syslog(message)

def onerror(function, path, sysinfo):
    log("Can't delete " + path)

def clean(directory, maxdirs):
    subdirs = os.listdir(directory)
    
    for dir in subdirs:
        if not os.path.isdir(os.path.join(directory, dir)) or os.path.islink(os.path.join(directory, dir)):
            subdirs.remove(dir)
    
    dirsToRemove = len(subdirs) - maxdirs
    
    if dirsToRemove < 0:
        dirsToRemove = 0
    
    if verbose and not cron:
        print "Going to clean: " + directory + " need to remove " + str(dirsToRemove) + " directories, keeping at max " + str(maxdirs)
    
    if len(subdirs) > maxdirs:
        if verbose and not cron:
            print "Dirs unsorted:"
            
            for dir in subdirs:
                print "\t" + dir
        
        dirsWithDate = []
        
        for dir in subdirs:
            dirsWithDate.append((dir, os.path.getmtime(os.path.join(directory, dir))))
            
        dirsWithDate.sort(cmp=None, key=lambda x: x[1], reverse=False)
        
        if verbose and not cron:
            print "\nDirs sorted:"
            for dir in dirsWithDate:
                print "\t" + dir[0]
        i = 0
        while i < dirsToRemove:
            if test and not cron:
                print "Would remove " + dirsWithDate[i][0]
            
            if not test:
                log("Deleting " + os.path.join(directory, dirsWithDate[i][0]))
                shutil.rmtree(os.path.join(directory, dirsWithDate[i][0]), False, onerror)
            
            i += 1

def main():
    syslog.openlog("DirectoryCleaner")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:tm:cv", ["help", "dir=", "test", "max-dirs=", "cron", "verbose"])
        
    except getopt.GetoptError as err:
        print str(err)
        log(err)
        syslog.closelog()
        sys.exit(-1)

    if len(opts) == 0:
        print "\nNo arguments, see help\n"
        usage()
        sys.exit(0)

    dir = "."
    maxdirs = 10

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            syslog.closelog()
            sys.exit(0)
            
        elif o in ("-d", "--dir"):
            dir = a
            if not os.path.isdir(dir):
                print "Path " + dir + " is not a dir or doesn't exist"
                log("Path " + dir + " is not a dir or doesn't exist")
                syslog.closelog()
                sys.exit(-1)
                
        elif o in ("-t", "--test"):
            test = True
            
        elif o in ("-m", "--max-dirs"):
            maxdirs = int(a)
            
        elif o in ("-c", "--cron"):
            cron = True
            
        elif o in("-v", "--verbose"):
            verbose = True

    clean(dir, maxdirs)
    
    syslog.closelog()

if __name__ == "__main__":
    main()
