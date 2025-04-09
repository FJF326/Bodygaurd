import psutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("port", type=int)
args = parser.parse_args()

for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == args.port:
            process = psutil.Process(conn.pid)
            process.terminate()

print("Port "+ str(args.port) + "has been closed successfully\n")




