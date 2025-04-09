import subprocess
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("user", type=str)
parser.add_argument("job", nargs='*', type=str)

args = parser.parse_args()

cron = open("/var/spool/cron/crontabs/"+args.user,"r")
cronWrite = open("/var/spool/cron/crontabs/"+args.user, "w")

info =cron.read()
lines = info.splitlines()
job = " ".join(args.job)
count = 0
print(job)
for line in lines:
    if job in line and line.startswith("#") == False:
        lines[count]=""
        break
    else:
        coutn = count +1

for line in lines:
    modified = modified + line

