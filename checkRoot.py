from datetime import datetime

report = open("BGreport.txt","a")
shadow = open("/etc/shadow","r")

report.write("\n\nRoot User Check\n")
report.write ("_"*60)
report.write("\n")

t1=datetime.now()
contents = shadow.read()
lines = contents.splitlines()

if lines[0][5]=='*' or lines[0][5]=="!":
    report.write("Root user is LOCKED\n")
else:
    report.write("Root user is UNLOCKED\n")

t2=datetime.now()

totalTime = t2-t1
report.write("Finished in "+ str(totalTime)+"\n")





