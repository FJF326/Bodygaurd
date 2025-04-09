import subprocess

command = ["python3", "portscanner.py"]
subprocess.call(command)

command=["python3", "loginscanner.py"]
subprocess.call(command)

command=["python3", "checkRoot.py"]
subprocess.call(command)

command=["python3", "checkCron.py"]
subprocess.call(command)