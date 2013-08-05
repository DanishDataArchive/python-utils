#!/usr/bin/env python

import urllib2, datetime, sys, ConfigParser, os, pkg_resources

from optparse import OptionParser

class JobColors:
    SUCCES = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'

protocol = "http"
secure = False
host = ""
port = ""

projectName = ""
buildNumber = 0

def buildHostUrl():
    url = protocol
    
    if secure:
        url += "s"
    
    url += "://"
    
    url += host
    
    url += ":"
    
    url += str(port)
    
    url += "/"
    
    return url

def getConsoleOutputForBuild(projectName, buildId, numberOfLines):
    try:
        consoleOutPut = urllib2.urlopen(buildHostUrl() + "job/" + projectName + "/" + str(buildId) + "/logText/progressiveText?start=0").read().split("\n")
        trimmedOutPut = consoleOutPut[len(consoleOutPut) - numberOfLines:]

        result = ""

        for line in trimmedOutPut:
            result += line + "\n"

        return result
    except urllib2.HTTPError as err:
        print err.reason

def evalJson(json):
    (true,false,null) = (True,False,None)
    return eval(urllib2.urlopen(json).read())

def getLastSuccessFulBuild(projectName):
    return evalJson(buildHostUrl() + "job/" + projectName + "/api/python?pretty=true")['lastSuccessfulBuild']

def getLastUnsuccessFulBuild(projectName):
    return evalJson(buildHostUrl() + "job/" + projectName + "/api/python?pretty=true")['lastUnsuccessfulBuild']

def getBuildDetails(projectName, buildId):
    return evalJson(buildHostUrl() + "job/" + projectName + "/" + str(buildId) + "/api/python?pretty=true")

def getDateTimeFromTimeStamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1e3)

def startBuildOfJob(job):
    req = urllib2.Request(buildHostUrl() + "job/" + job + "/build")
    urllib2.urlopen(req).read()

def getProjects():
    return evalJson(buildHostUrl() + "api/python?pretty=true")

def main():
    global host
    global port
    global protocol
    global secure

    parser = OptionParser(version=pkg_resources.require("py-utils-dda")[0].version, epilog="Fetch info from a jenkins host", description="GPL")
    parser.add_option("-b", "--build", dest="buildNumber", action="store", type="int")
    parser.add_option("-c", "--console", dest="console", action="store_true")
    parser.add_option("-e", "--encrypted", dest="encrypted", action="store_true")
    parser.add_option("--host", dest="host", action="store", type="string")
    parser.add_option("-j", "--job", dest="job", action="store", type="string")
    parser.add_option("-l", "--list", dest="list", action="store_true")
    parser.add_option("--port", dest="port", action="store", type="int")
    parser.add_option("-q", "--start-job", dest="startJob", action="store_true")
    parser.add_option("-s", "--status", dest="status", action="store_true")
    parser.add_option("-n", "--number-of-lines", dest="numberOfLines", action="store", type="int", default=10)

    (opts, args) = parser.parse_args(sys.argv)

    Config = ConfigParser.ConfigParser()
    Config.read(os.path.join(os.path.expanduser("~"), ".py-jenkins/py-jenkins.conf"))

    if 'global' in Config.sections():
        for option in Config.options('global'):
            if option in 'host':
                host = Config.get('global', option)
            elif option in 'port':
                port = Config.get('global', option)
            elif option in 'protocol':
                protocol = Config.get('global', option)
            elif option in 'secure':
                secure = Config.getboolean('global', option)

    if opts.host:
        host = opts.host

    if opts.port:
        port = opts.port

    if opts.encrypted:
        secure = True

    if opts.job:
        projectName = opts.job

    if opts.buildNumber:
        buildNumber = opts.buildNumber

    if opts.list:
        projects = getProjects()

        for project in projects['jobs']:
            if project['color'] == "blue":
                print JobColors.SUCCES + project['name'] + JobColors.END
            elif project['color'] == "blue_anime":
                print JobColors.SUCCES + project['name'] + " (working)" + JobColors.END
            else:
                print JobColors.FAIL + project['name'] + " (" + project['color'] + ")" + JobColors.END

    if opts.status:
        projects = getProjects()

        for project in projects['jobs']:
            if project['color'] == "blue":
                print JobColors.SUCCES + project['name'] + JobColors.END
            elif project['color'] == "blue_anime":
                print JobColors.SUCCES + project['name'] + " (working)" + JobColors.END
            else:
                print JobColors.FAIL + project['name'] + " (" + project['color'] + ")" + JobColors.END

            success = getLastSuccessFulBuild(project['name'])
            if success:
                successDetails = getBuildDetails(project['name'], success['number'])
                print "\tLast Successful: " + str(success['number']) + " at " + str(getDateTimeFromTimeStamp(successDetails['timestamp']))

            unsucces = getLastUnsuccessFulBuild(project['name'])

            if unsucces:
                unsuccessDetails = getBuildDetails(project['name'], success['number'])
                print "\tLast Unsuccessful: " + str(unsucces['number']) + " at " + str(getDateTimeFromTimeStamp(unsuccessDetails['timestamp']))

    if opts.console:
        output = getConsoleOutputForBuild(projectName, buildNumber, opts.numberOfLines)
        if output:
            print output

    if opts.startJob:
        startBuildOfJob(projectName)

if __name__ == '__main__':
    main()
