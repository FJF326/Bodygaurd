import subprocess
import argparse

closePort = False
deleteCron = False
lockUser = False
addEmail = False
takeAction = False




command = ["python3", "portscanner.py"]
subprocess.call(command)

command=["python3", "loginscanner.py"]
subprocess.call(command)

command=["python3", "checkRoot.py"]
subprocess.call(command)

command=["python3", "checkCron.py"]
subprocess.call(command)