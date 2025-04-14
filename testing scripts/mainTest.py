import socket
import threading
from crontab import CronTab

def run_fake_service(port, banner):
    def handler():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", port))
            s.listen(5)
            print(f"Listening on port {port} with banner: {banner.strip()}")
            while True:
                conn, addr = s.accept()
                with conn:
                    try:
                        conn.sendall(banner.encode())
                    except:
                        pass  # Client disconnected
    thread = threading.Thread(target=handler, daemon=True)
    thread.start()

def add_cron_jobs():
    cron = CronTab(user=True)
    jobs = [
        ("* * * * *", "echo 'SSH simulated' >> ~/cron_ssh.log"),
        ("*/2 * * * *", "echo 'HTTP simulated' >> ~/cron_http.log"),
        ("*/3 * * * *", "echo 'FTP simulated' >> ~/cron_ftp.log"),
        ("*/5 * * * *", "echo 'SMTP simulated' >> ~/cron_smtp.log")
    ]
    for time, command in jobs:
        job = cron.new(command=command)
        job.setall(time)
    cron.write()
    print("Cron jobs added.")

if __name__ == "__main__":
    add_cron_jobs()

    # Banners that protocol scanners (e.g., nmap) use to fingerprint services
    run_fake_service(3000, "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.4\r\n")  # SSH
    run_fake_service(3001, "HTTP/1.1 200 OK\r\nServer: Apache\r\n\r\n")     # HTTP
    run_fake_service(3002, "220 (vsFTPd 3.0.3)\r\n")                        # FTP
    run_fake_service(3003, "220 smtp.example.com ESMTP Postfix\r\n")       # SMTP

    print("All fake ports are listening. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
