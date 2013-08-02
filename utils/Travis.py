#!/usr/bin/env python

import urllib2, simplejson, sys, pkg_resources

from optparse import OptionParser
from types import *

def printBuild(build, printNumber = False):
    if printNumber:
        print "\tNumber: " + str(build['number'])

    if build['config']:
        if build['config']['jdk']:
            if type(build['config']['jdk']) is list:
                print "\tJDK: " + build['config']['jdk'][0]
            else:
                print "\tJDK: " + str(build['config']['jdk'])
    print "\tFinished at: " + str(build['finished_at'])
    print "\tResult: " + str(build['result']) + "\n"

def getProjectInfo(parent, projectName):
    return simplejson.load(urllib2.urlopen("https://api.travis-ci.org/repos/" + parent + "/" + projectName + ".json"))

def getLastestBuildId(project):
    return project['last_build_id']

def getBuilds(parent, projectName):
    return simplejson.load(urllib2.urlopen("https://api.travis-ci.org/repos/" + parent + "/" + projectName + "/builds.json"))

def printBuildList(buildList):
    for build in buildList:
        print "#" + build['number'] + " '" + build['message'] + "' from commit '" + build['commit'][:7] + " (" + build['branch'] + ")' Duration: " + str(build['duration'])

def getBuildFromBuildNumber(parent, projectName, buildNumber):
    builds = getBuilds(parent, projectName)

    for build in builds:
        if int(build['number']) == int(buildNumber):
            return getBuildInfo(parent, projectName, build['id'])

    return None

def getBuildInfo(parent, projectName, buildId):
    return simplejson.load(urllib2.urlopen("https://api.travis-ci.org/repos/" + parent + "/" + projectName + "/builds/" + str(buildId) + ".json"))

def printBuildDetails(projectName, build):
    print "Build " + str(build['number'])

    if len(build['matrix']) > 1:
        for subBuild in build['matrix']:
            printBuild(subBuild, True)
    else:
        printBuild(build)

def main():
    parser = OptionParser(version=pkg_resources.require("py-utils-dda")[0].version, epilog="Fetch info from travis-ci.org", description="GPL")
    parser.add_option("-a", "--list-builds", dest="listBuilds", action="store_true")
    parser.add_option("-b", "--build", dest="buildNumber", action="store", type="int")
    parser.add_option("-p", "--project", dest="projectName", action="store", type="string")
    parser.add_option("-l", "--latest-build", dest="latestBuild", action="store_true")
    parser.add_option("-o", "--owner", dest="owner", action="store", type="string")

    (opts, args) = parser.parse_args(sys.argv)

    if not opts.projectName:
        print "Please provide a project"
        sys.exit(-1)

    if not opts.owner:
        print "Please provide a owner"
        sys.exit(-1)

    projectName = opts.projectName
    parent = opts.owner

    try:
        project = getProjectInfo(parent, projectName)
    except urllib2.HTTPError as err:
        print "Project " + projectName + " " + err.reason
        sys.exit(-1)

    if opts.latestBuild:
        print "Lastest build for " + projectName
        lastBuildId = getLastestBuildId(project)
        build = getBuildInfo(parent, projectName, lastBuildId)

        printBuildDetails(projectName, build)

    if opts.buildNumber:
        build = getBuildFromBuildNumber(parent, projectName, opts.buildNumber)
        if build:
            printBuildDetails(projectName, build)
        else:
            print "Not found"

    if opts.listBuilds:
        printBuildList(getBuilds(parent, projectName))

if __name__ == '__main__':
    main()
