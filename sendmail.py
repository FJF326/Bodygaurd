import smtplib, ssl

emails = []
conf = open("Bodygaurd.conf","r")
report = open("BGreport.txt","r")
reportInfo = report.read()
info = conf.read()
lines = info.split()
for line in lines:
    if line.startswith("email="):
        print(line)
        words=line.split("=")
        emails.append(words[1])


port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "bodygaurdreport@gmail.com"
password = "xzyj enjm syzo qpfz"
message = reportInfo
for  email in emails:
    receiver_email = email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)