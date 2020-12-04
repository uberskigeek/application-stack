#############################################
# Test script to run odo java-openliberty stack
# in guithub actions environment
###############################################
import os
import subprocess
import sys
import time

os.system("echo Current directory")
os.system("pwd")

# Function to test the health endpoint
def testHealth(urlList):
     print("In test health ",urlList )
     httpURL = getHttpURL(urlList)
     if httpURL:
         print("httpURL not empty")
         liveURL = httpURL + "/health/live"
         readyURL = httpURL + "/health/ready"
         print("live URL = ", liveURL)
         print("ready URL = ", readyURL)
         # lets give the server time to start
         time.sleep(60)
         curlResults = subprocess.run(["curl", liveURL],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
         print("Health URL check results", curlResults.stdout, "\nError =", curlResults.stderr, " RC =", curlResults.returncode)
     else:
         print("Http URL is empty")

# function to return the HTTP URL for the application
def getHttpURL(urlList):
    print("Parsing HTTP request from ", urlList)
    http = ""
    httpFound = False
    if len(urlList) >= 2:
        httpRequest = urlList[2].find("http")
        if httpRequest >= 0:
            print("getHttpURL http request = ", httpRequest)
            li = urlList[2].split(" ")
            for i in li:
                if i.find("http") >=0  and not httpFound:
                    http = i
                    httpFound = True
                elif i and httpFound:
                    http = http + ":" + i
                    break
            if http:
                print("Http root = ", http)
        else:
            print("Http URL not provided")
    return http

# check the odo log and look for failed tests
def checkTestResults(logData):
    print("begin checkTestResults")
    failures = 0
    errors = 0
    skipped = 0
    for i in logData:
        if i.find("[INFO] Tests run:") >=0:
            list = i.split(",")
            for result in list:
                if result.find("Failures:") >= 0:
                    if result.find("0") < 0:
                        failures = failures + 1
                elif reseult.find("Errors") >= 0:
                    if result.find("0") < 0:
                        errors = errors + 1
                elif result.find("Skipped") >= 0:
                    if result.find("0") < 0:
                        skipped = skipped + 1

            if failures or errors or skipped:
                print("Test Failure")
            else:
                print("Test Completed successfully")
    return failures + errors + skipped

# Delete the odo project on error or successful completion.
def deleteProject():
    processResults = subprocess.run(["odo","delete"],stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
returnCode = int(0)
os.system("kubectl version")

# Clone git repo
processResults = subprocess.run(["git", "clone", "https://github.com/OpenLiberty/application-stack-intro.git"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if(processResults.returncode == 0):
   os.chdir("application-stack-intro")\
   # create new project
   processResults = subprocess.run(["odo", "create", "myopenliberty"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)

   if( processResults.returncode == 0):
     # Added here to clean up minikube environment
     # this was suggested to allow the ingress to install and run successfully
     processResults = subprocess.run(["minikube", "delete"], stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
     print("Minikube delete results = ", processResults.stderr, " ", processResults.stdout)

     processResults = subprocess.run(["minikube","start"], stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)

     print("minikube start results ",  processResults.stderr, " ", processResults.stdout)

     # Enable ingress addon in minikube
     processResults = subprocess.run(["minikube", "addons", "enable", "ingress"])
     if( processResults.returncode == 0):
       processResults = subprocess.run(['kubectl','get','pods','-n','kube-system'], stdout=subprocess.PIPE, text=True )
       print("kubectl get pods results = ", processResults.stdout)
       processResults = subprocess.run(["minikube", "ip"], stdout=subprocess.PIPE, text=True )
       print("ingress ip = ", processResults.stdout)
       print("ingress ip return code =", processResults.returncode)

       if processResults.returncode == 0:
         url = processResults.stdout.strip() + ".nip.io"
         print("odo url create URL |", url,"|")
         # Create odo project URL using ingress
         processResults = subprocess.run(["odo", "url", "create", "--host", url.strip(), "--ingress"],
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

         if(processResults.returncode == 0):
             processResults = subprocess.run(["odo", "push"],
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

             if( processResults.returncode == 0):

                 # use the following to find the URL for the application
                 processResults = subprocess.run(["odo", "url", "list"], universal_newlines = True,
                                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 print("odo url list results ", processResults.stdout)

                 kubectlResults = subprocess.run(['kubectl', 'get', 'ingress'], universal_newlines = True,
                                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 print("kubectl get ingress results = ", kubectlResults.stdout," \nstderr ", kubectlResults.stderr)

                 if( processResults.returncode == 0 ):
                     # Test the health URL
                     # note this is inner loop testing.
                     # The below function still doesn't work.
                     # The URL being generated gets connection refused
                     testHealth(processResults.stdout.splitlines())
                     print("Return from testHealth")
                     processResults = subprocess.run(["odo","log"],
                                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     # look through the odo log and check the integration results.
                     if checkTestResults(processResults.stdout.splitlines()) > 0:
                         returncode = 12
                     deleteProject()
                 else:
                     print("odo url list failed rc = ", processResults.returncode, "\n URL List Error: \n ",
                           processResults.stderr)
                     deleteProject()
                     returncode = 12

             else:
                print("\nError with odo push after url create \n", processResults.stdout, "\n ERROR: \n ",
                      processResults.stderr)
                deleteProject()
                returnCode = 12

         else:
             print("Error issuing URL create ", processResults.stdout, "\nBegin Stderr \n", processResults.stderr, "\nEnd Stderr\m")
             deleteProject()
             returnCode = 12

       else:
         print("Error getting ingress ip ", processResults.stdout)
         deleteProject()
         returnCode = 12

     else:
       print("Error enabling ingress in minikube ", processResults.stdout)
       deleteProject()
       returnCode = 12

   else:
     print("Error creating odo project ", processResults.stdout)
     deleteProject()
     returnCode = 12

else:
   print("Error cloning openliberty stack ", git_clone_results.stdout)
   returnCode = 12

sys.exit(returnCode)
