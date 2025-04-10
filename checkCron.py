from datetime import datetime
import subprocess

report = open("BGreport.txt","a")
report.write("\nCrontab Scan\n")
report.write("_"*60)
report.write("\n")
report.write("All Running Jobs:\n\n")

print("Checking Cron Jobs...")

t1=datetime.now()

command = subprocess.run("cut -d: -f1,3 /etc/passwd | egrep ':[0-9]{4}$' | cut -d: -f1", shell=True, capture_output=True, text=True)

output = command.stdout
users = output.split()

for user in users:
    report.write("User "+user+":\n")
    try:
        cron=open("/var/spool/cron/crontabs/"+user,"r")
        info = cron.read()
        cronLines = info.splitlines()
    
        count = 1
        for line in cronLines:
            if line.startswith("#"):
                continue
            else:
                report.write(str(count)+". "+line+"\n")
                count = count +1
        report.write("\n")           
    except:
         report.write("User has no crontab established\n")

t2= datetime.now()
totalTime = t2-t1
report.write("Finished in "+str(totalTime) )

print("Finished Checking Cron Jobs")