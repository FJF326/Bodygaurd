import subprocess
import argparse

closePort = 0
deleteCron = False
lockUser = ""
addEmail = ""
takeAction = False



parser = argparse.ArgumentParser()

parser.add_argument('-a', action='store_true', help='Enable takeAction')
parser.add_argument('-cP', help='Close specific port (requires port number)')
parser.add_argument('-l', type=str, help='Lock user')
parser.add_argument('-e', type=str, help='Add email')

args = parser.parse_args()

takeAction = args.a
closePort = args.cP
lockUser = args.l
addEmail = args.e




if takeAction == True:
    command = ["python3","takeaction.py"]
    subprocess.call(command)

elif closePort != 0:
    command = ["python3","portCloser.py",closePort]
    subprocess.call(command)

elif lockUser != "":
    command = ["python3","lockUser.py",lockUser]
    subprocess.call(command)

elif addEmail != "":
    command = ["python3","addEmail.py",addEmail]
    subprocess.call(command)



else:
    command = ["python3", "portscanner.py"]
    subprocess.call(command)

    command=["python3", "loginscanner.py"]
    subprocess.call(command)

    command=["python3", "checkRoot.py"]
    subprocess.call(command)

    command=["python3", "checkCron.py"]
    subprocess.call(command)

    command = ["python3","sendmail.py"]
    subprocess.call(command)

