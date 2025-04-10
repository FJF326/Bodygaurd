import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user", type=str)

args = parser.parse_args()

subprocess.call(["passwd","-l",args.user],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

