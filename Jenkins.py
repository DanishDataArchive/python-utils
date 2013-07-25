#!/usr/bin/env python

import urllib2, datetime, sys, getopt

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
    
    url += port
    
    url += "/"
    
    return url

def getConsoleOutputForBuild(projectName, buildId):
    try:
        return urllib2.urlopen(buildHostUrl() + "job/" + projectName + "/" + str(buildId) + "/logText/progressiveText?start=0").read()
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

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:ceh:j:lp:qs", ["build=", "console", "encrypted", "host=", "job=", "list", "port=", "start-job", "status"])
        
    except getopt.GetoptError as err:
        print str(err)
    
    for o, a in opts:
        if o in ("-h", "--host"):
            host = a
            
        if o in ("-p", "--port"):
            port = a

        if o in ("-l", "--list"):
            projects = getProjects()
            
            for project in projects['jobs']:
                if project['color'] == "blue":
                    print JobColors.SUCCES + project['name'] + JobColors.END
                elif project['color'] == "blue_anime":
                    print JobColors.SUCCES + project['name'] + " (working)" + JobColors.END
                else:
                    print JobColors.FAIL + project['name'] + " (" + project['color'] + ")" + JobColors.END

        elif o in ("-s", "--status"):
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
        elif o in ("-e", "--encrypted"):
            secure = True

        elif o in ("-c" or "--console"):
            output = getConsoleOutputForBuild(projectName, buildNumber)
            if output:
                print output

        elif o in ("-j" or "--job"):
            projectName = a

        elif o in ("-b" or "--build"):
            buildNumber = a

        elif o in ("-q" or "start-job"):
            startBuildOfJob(projectName)
