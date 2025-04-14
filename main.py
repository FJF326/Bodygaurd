import subprocess
import argparse

closePort = 0
deleteCron = False
lockUser = ""
addEmail = ""
takeAction = False
deleteCronJob = ""
deleteCronUser = ""
safeUser=""

parser = argparse.ArgumentParser()

parser.add_argument('-a', action='store_true', help='Enable takeAction')
parser.add_argument('-cP',type=int, help='Close specific port (requires port number)')
parser.add_argument('-l', type=str, help='Lock user')
parser.add_argument('-e', type=str, help='Add email to config file')
parser.add_argument('-dC',nargs =2,type=str,help='Delete cron job: [user] [job]')
parser.add_argument('-s',type=str,help='add dafe user to config file' )
args = parser.parse_args()

takeAction = args.a
closePort = args.cP
lockUser = args.l
addEmail = args.e
if args.dC:
    deleteCronUser = args.dC[0]
    deleteCronJob = args.dC[1]

safeUser = args.s


if takeAction == True:
    command = ["python3","takeaction.py"]
    subprocess.call(command)

elif closePort is not None:
    command = ["python3","portCloser.py",str(closePort)]
    subprocess.call(command)

elif lockUser is not None:
    command = ["python3","lockUser.py",lockUser]
    subprocess.call(command)

elif addEmail is not None:
    command = ["python3","addEmail.py",addEmail]
    subprocess.call(command)


elif deleteCronJob and deleteCronUser:
    command = ["python3","deleteCron.py",deleteCronUser,deleteCronJob]
    subprocess.call(command)


elif safeUser is not None:
    command = ["python3","addSafeUser.py",safeUser]
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

