from datetime import datetime, timedelta
import json


log= open("/var/log/auth.log","r")
report = open("BGreport.txt","a")
report.write("\n")
report.write("Invalid Logins\n")
report.write("_"*60)
report.write("\n")
t1 = datetime.now()
failedLogins={}
print("Scanning Logins...")
for line in log:
    if "authentication failure" in line:
        index =-1
        i =0
        words = line.split()
        date = words[0]
        for value in words:
            if value.startswith("user="):
                index=i
                break
            i=i+1
        if(index != -1):   
            user=words[i][5:]
            loginType =words[2].strip(":")
            report.write("User: "+user + " Login Type: "+loginType+ " Date: "+date+"\n")
            entry = {"date":date}
            if user in failedLogins:
                failedLogins[user].append(entry)
            else:
                failedLogins[user]=[]
                failedLogins[user].append(entry)


report.write("\nFailed Logins per User in Last 24 Hours\n")
for user,dates in  failedLogins.items():
        
        dateChecker = datetime.fromisoformat(dates[len(dates)-1]['date']) - timedelta(hours=24)
        recentFails =0
        for date in dates:
            newDate = datetime.fromisoformat(date["date"])
            if dateChecker < newDate:
                recentFails = recentFails+1
        report.write(user+": " + str(recentFails)+ "\n")
       
       
        


t2=datetime.now()
totalTime = t2-t1
report.write("\n")
report.write("Finished in "+ str(totalTime)+"\n")
report.write("_"*60)

print("Finished Scanning Logins")
