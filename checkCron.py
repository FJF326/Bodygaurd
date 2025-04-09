from datetime import datetime


report = open("BGreport","a")
cron = open("/tmp/crontab","r")

cronLines =cron.read()
print(cronLines)