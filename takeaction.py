import subprocess
from datetime import datetime
from colorama import Fore
import os
import psutil

subprocess.call(["clear"])

config = open("BG.conf","r")
confLines = config.read().splitlines()

for line in confLines:
    if line.startswith("threshold="):
        words=line.split("=")
        threshhold=words[1]

subprocess.call(["python3","main.py"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

report = open("BGreport.txt","r")
lines = report.read().splitlines()

#action for ports
print(Fore.LIGHTMAGENTA_EX+"ANALYZING PORTS:")
for line in lines:
    if line.startswith("Port"):
        words = line.split()
        port=words[1].replace(":","")
        print(Fore.BLUE + "Port "+port+" is open using protocol "+words[3])
        userResponse=input(Fore.YELLOW+"WOULD YOU LIKE TO CLOSE PORT "+port+"(y/n):")
        if userResponse == 'y':
           subprocess.call(["python3","portCloser.py",port], stdout=subprocess.DEVNULL)
           print(Fore.GREEN+"Closed Port "+port+" Successfully")
    else:
        continue


#action for user
print(Fore.LIGHTMAGENTA_EX+"\nANALYZING USERS:")
noUsers = True
section = False
for line in lines:
    if line.startswith("Failed Logins"):
       section = True
       continue
    
    if section ==True:
        if line.strip() == "":
            break
        words = line.strip().split(":")
        user = words[0]
        failedLogins=words[1].replace("(SAFE USER)","")
        if(int(failedLogins) >=int(threshhold)):
            noUsers = False
            if "(SAFE USER)"  in words[1]:
                print(Fore.GREEN+ user+" is above the threshold but is a SAFE USER")
                continue

            print(Fore.BLUE+user+" is above the threshold("+str(threshhold)+")")
            userResponse=input(Fore.YELLOW+"Would you like to LOCK the user?(y/n):") 
            if userResponse == "y":
                subprocess.call(["python3","lockUser.py",user])
                print(Fore.GREEN+user+" has been LOCKED")

if noUsers == True:
    print(Fore.BLUE+"No Users are above the threshold")
        

#action for root user
print(Fore.LIGHTMAGENTA_EX+"\nAnalyzing Root User:")
for line in lines:
    if line.startswith("Root user is"):
        words = line.split()
        if words[3]== "LOCKED":
            print(Fore.GREEN+"Root User is LOCKED")
        if words[3] == "UNLOCKED":
            print(Fore.BLUE+"Root User is UNLOCKED")
            userResponse = input(Fore.YELLOW+"Would you like to lock the Root user?(y/n)")
            if userResponse == "y":
                subprocess.call(["python3","lockUser.py","root"])
                print(Fore.GREEN+"Root User Has been LOCKED")



#actions for cron jobs
print(Fore.LIGHTMAGENTA_EX+"\nANALYZING CRON JOBS:")
noCronJobs = True
section = False
currentUser =""
currentJob=""

for line in lines:
     if line.startswith("All Running Jobs:"):
       section = True
       continue
     if section == True and line!="":
        words=line.split()
        if words[0].startswith("User"):
            currentUser = words[1].strip(":")
            continue

        elif line.startswith("Finished"):
            break
        
        elif "." in line:
            words=line.split(".")
            currentJob = words[1].strip()
            print(Fore.BLUE+"User "+currentUser+" has cron job "+currentJob)
            userResponse = input(Fore.YELLOW+"Would you like to Delete this job?(y/n)")
            if userResponse =="y":
                subprocess.call(["python3","deleteCron.py",currentUser,currentJob])
                print(Fore.GREEN+"JOB has been DELETED")


print(Fore.LIGHTGREEN_EX+ "ALL SUGGESTIONS HAVE BEEN COMPLETED")