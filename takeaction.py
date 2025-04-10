import subprocess
from datetime import datetime
from colorama import Fore
import os
import psutil

threshhold =3

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
print(Fore.GREEN+"\nANALYZING USERS:")
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
        failedLogins=words[1]
        if(int(failedLogins) >=threshhold):
            print(Fore.BLUE+user+" is above the threshold("+str(threshhold)+")")
            userResponse=input(Fore.YELLOW+"Would you like to LOCK the user?(y/n):") 
            if userResponse == "y":
                subprocess.call(["python3","lockUser.py",user])
                print(Fore.GREEN+user+" has been LOCKED")
        

