import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user", type=str)

args = parser.parse_args()

configureRead = open("BG.conf","r")
lines = configureRead.read().splitlines()
configureRead.close()

count =0
for line in lines:
    if line.startswith("safe"):
        lines[count] = line + " " +args.user
    count+=1

modified=""
for line in lines:
    modified+=line + "\n"

configureWrite = open("BG.conf","w")
configureWrite.write(modified)
