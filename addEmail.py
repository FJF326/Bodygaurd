import argparse

parser = argparse.ArgumentParser()
parser.add_argument("email", type=str)

args = parser.parse_args()

configureRead = open("BG.conf","r")
lines = configureRead.read().splitlines()
configureRead.close()
section =False
count =0
for line in lines:
    if line.startswith("#to after"):
        section = True

    elif section ==True:
        if line == "":
            lines[count]="email="+args.email+"\n"
            break
    count+=1

modified=""
for line in lines:
    modified+=line + "\n"

configureWrite = open("BG.conf","w")
configureWrite.write(modified)



