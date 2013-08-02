#!/usr/bin/env python

import urllib2, simplejson, sys, pkg_resources

from optparse import OptionParser

def getProjectInfo(parent, projectName):
    return simplejson.load(urllib2.urlopen("https://travis-ci.org/" + parent + "/" + projectName + ".json"))

def getLastBuildId(project):
    return project['last_build_id']

def getBuildInfo(parent, projectName, buildNumber):
    return simplejson.load(urllib2.urlopen("https://travis-ci.org/" + parent + "/" + projectName + "/builds/" + str(buildNumber) + ".json"))

def printBuildDetails(projectName, build):
    print "Lastest build for " + projectName

    print "Build " + str(build['number'])

    if len(build['matrix']) > 1:
        for subBuild in build['matrix']:
            print "\tNumber: " + str(subBuild['number'])
            print "\tFinished at: " + str(subBuild['finished_at'])
            print "\tResult: " + str(subBuild['result']) + "\n"
    else:
        subBuild = build['matrix'][0]
        print "\tFinished at: " + str(subBuild['finished_at'])
        print "\tResult: " + str(subBuild['result']) + "\n"

def main():
    parser = OptionParser(version=pkg_resources.require("py-utils-dda")[0].version, epilog="Fetch info from travis-ci.org", description="GPL")
    parser.add_option("-p", "--project", dest="projectName", action="store", type="string")
    parser.add_option("-l", "--latest-build", dest="latestBuild", action="store_true")
    parser.add_option("-o", "--organization", dest="org", action="store", type="string")
    parser.add_option("-u", "--user", dest="user", action="store", type="string")

    (opts, args) = parser.parse_args(sys.argv)

    if not opts.projectName:
        print "Please provide a project"
        sys.exit(-1)

    if not (opts.org or opts.user):
        print "Please provide a user or organization"
        sys.exit(-1)

    projectName = opts.projectName
    parent = opts.user or opts.org

    try:
        project = getProjectInfo(parent, projectName)
    except urllib2.HTTPError as err:
        print "Project " + projectName + " " + err.reason
        sys.exit(-1)

    if opts.latestBuild:
        lastBuildId = getLastBuildId(project)
        build = getBuildInfo(parent, projectName, lastBuildId)

        printBuildDetails(projectName, build)

if __name__ == '__main__':
    main()
