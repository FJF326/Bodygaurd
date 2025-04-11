import argparse

parser = argparse.ArgumentParser()
parser.add_argument("email", type=str)

args = parser.parse_args()

configure = open("Bodygaurd.conf","a")

configure.write("email="+args.email)