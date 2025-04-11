import subprocess
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("user", type=str)
parser.add_argument("job", nargs='*', type=str)

args = parser.parse_args()

cron = open("/var/spool/cron/crontabs/"+args.user,"r")
info =cron.read()
lines = info.splitlines()
job = " ".join(args.job)
count = 0


for line in lines:
    if job in line:
        lines[count]=""
        break
    else:
        count = count +1

modified = ""
for line in lines:
    modified +=  line + "\n"



subprocess.run(['crontab', '-u',args.user,'-'], input=modified, text=True)

