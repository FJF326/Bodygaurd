from datetime import datetime, timedelta
import json


log= open("/var/log/auth.log","r")
report = open("BGreport.txt","a")
report.write("\n")
report.write("Invalid Logins\n")
report.write("_"*60)
report.write("\n")

safeUsers=[]
conf = open("BG.conf","r")
confLines = conf.read().splitlines()
for line in confLines:
    if line.startswith("safe="):
        words=line.split("=")
        safeUsers=words[1].split()
        print(safeUsers)

t1 = datetime.now()
failedLogins={}
invalidLoginCount=1
print("Scanning Logins...")
for line in log:
    if "authentication failure" in line:
        index =-1
        i =0
        words = line.split()
        month = words[0]
        day = words[1]
        time = words[2]
        fullDate= f"{month} {day} {time} {datetime.now().year}"

        parsedDate = datetime.strptime(fullDate, "%b %d %H:%M:%S %Y")
        entry = {"date": parsedDate}
        for value in words:
            if value.startswith("user=") or value.startswith("USER="):
                index=i
                break
            i=i+1
        if(index != -1):   
            user=words[i][5:].replace("]","")
            loginType =words[4].strip(":")
            report.write(str(invalidLoginCount)+". User: "+user + " Login Type: "+loginType+ " Date: "+fullDate+"\n")
            invalidLoginCount+=1
            if user in failedLogins:
                failedLogins[user].append(entry)
            else:
                failedLogins[user]=[]
                failedLogins[user].append(entry)


report.write("\nFailed Logins per User in Last 24 Hours\n")
for user,dates in  failedLogins.items():
        
        dateChecker = dates[-1]['date']- timedelta(hours=24)
        recentFails =0
        for date in dates:
            newDate = date["date"]
            if dateChecker < newDate:
                recentFails = recentFails+1
        if user in safeUsers:
            report.write(user+": " + str(recentFails)+ " (SAFE USER)\n")
        else:
            report.write(user+": " + str(recentFails)+ "\n")
       
       
        


t2=datetime.now()
totalTime = t2-t1
report.write("\n")
report.write("Finished in "+ str(totalTime)+"\n")
report.write("_"*60)

print("Finished Scanning Logins")
