import socket
import threading
import http.server
import socketserver
from crontab import CronTab
import os

# --- Service Functions ---

def ssh_like_server(port):
    def handle_client(conn, addr):
        conn.sendall(b"Welcome to fake SSH. Type 'exit' to quit.\n")
        while True:
            conn.sendall(b"$ ")
            cmd = conn.recv(1024).strip()
            if cmd == b"exit":
                break
            conn.sendall(b"Fake output for: " + cmd + b"\n")
        conn.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"SSH-like server on port {port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def http_server(port):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Hello from fake HTTP!</h1></body></html>")

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"HTTP server running on port {port}")
        httpd.serve_forever()

def ftp_like_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"FTP-like server on port {port}")
    while True:
        conn, addr = server.accept()
        conn.sendall(b"220 Fake FTP Server Ready.\n")
        conn.close()

def smtp_like_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"SMTP-like server on port {port}")
    while True:
        conn, addr = server.accept()
        conn.sendall(b"220 Fake SMTP Server Ready.\n")
        conn.close()

# --- Cron Jobs ---

def add_cron_jobs():
    cron = CronTab(user=True)
    jobs = [
        ("* * * * *", "echo 'SSH fake server alive' >> ~/ssh_cron.log"),
        ("*/2 * * * *", "echo 'HTTP fake server alive' >> ~/http_cron.log"),
        ("*/3 * * * *", "echo 'FTP fake server alive' >> ~/ftp_cron.log"),
        ("*/5 * * * *", "echo 'SMTP fake server alive' >> ~/smtp_cron.log")
    ]

    for time, command in jobs:
        job = cron.new(command=command)
        job.setall(time)

    cron.write()
    print("Cron jobs added.")

# --- Main ---

if __name__ == "__main__":
    add_cron_jobs()

    threading.Thread(target=ssh_like_server, args=(3000,), daemon=True).start()
    threading.Thread(target=http_server, args=(3001,), daemon=True).start()
    threading.Thread(target=ftp_like_server, args=(3002,), daemon=True).start()
    threading.Thread(target=smtp_like_server, args=(3003,), daemon=True).start()

    print("All fake servers running. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down.")
