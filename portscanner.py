import socket
import subprocess
import sys
from datetime import datetime
import requests

file = open("BGreport.txt",'w')
file.write("PORT SCANNER\n")
file.write("_"*60)
file.write("\n\n")
file.write("Open:\n")


subprocess.call('clear',shell=True)

remoteServer = "127.0.0.1"
remoteServerIp = socket.gethostbyname(remoteServer)


t1 = datetime.now()
print("Scanning Ports...")
for port in range(1,9000):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result= sock.connect_ex((remoteServerIp, port))
    if(result == 0):
        command = ["nmap", "-sV", "-p", str(port), "localhost"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8')
        
        allLines = output.splitlines()
        count =0

        for line in allLines:
            if "PORT" in line:
                info = allLines[count +1 ]
            count = count+1
        words = info.split()
        service = words[2]
        try:
            float(words[4].strip())
            is_version = True
        except ValueError:
            is_version = False
        if(is_version):
            version = " ".join(words[3:5])
        else:
            version = words[3]

        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={version}"
        response = requests.get(url)
        myResults = response.json()
        v = myResults["vulnerabilities"][0]["cve"]
        id= v["id"]
        description = "No description available"
        if 'descriptions' in v and len(v['descriptions']) > 0:

            for d in v['descriptions']:
                if d['lang'] == 'en':
                    description = d['value']
                    break
        descWords = description.split()
        score =0
        if 'metrics' in v:
            metrics = v['metrics']
            
            if 'cvssMetricV31' in metrics and len(metrics['cvssMetricV31']) > 0:
                score = metrics['cvssMetricV31'][0]['cvssData']["baseScore"] 
                   
            elif 'cvssMetricV30' in metrics and len(metrics['cvssMetricV30']) > 0:
                score =  metrics['cvssMetricV30'][0]['cvssData']["baseScore"]
                
            elif 'cvssMetricV2' in metrics and len(metrics['cvssMetricV2']) > 0:
                score =  metrics['cvssMetricV2'][0]['cvssData']["baseScore"]
               
            if float(score) >= 7.0:
                severity = "HIGH"
            elif float(score) >= 4.0:
                severity = "MEDIUM"
            else:
                severity = "LOW"

        file.write("PORT "+str(port)+": OPEN "+ service + " "+ version+"\n")
        file.write("Vulnerabilitie:\n")
        file.write("CVE ID: "+id+"\n")
        file.write("Description: ")
        allLines=[]
        for i in range(0,len(descWords),20):
            allLines.append(' '.join(descWords[i:i+15]))
        printDesc= "\n".join(allLines)
        file.write(printDesc)
        file.write("\nSeverity: "+severity+" " +str(score)+"\n\n")
    sock.close()


print("Finished Scanning Ports")
t2 = datetime.now()
totalTime = t2-t1

file.write("Finished in "+str(totalTime)+"\n")

file.write("_"*60)
file.write("\n")


