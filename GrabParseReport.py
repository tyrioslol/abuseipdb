from paramiko import SSHClient
from scp import SCPClient
import time
import json
import requests


#### Written by: Bowen Aguero ####
#### https://www.linkedin.com/in/bowen-aguero-555a721ab/ ####


# replace with path to known hosts (usually /home/username/.ssh/known_hosts)
hosts = '/path/to/known/hosts'

# replace with the ip that hosts your logs
hostip = 'host_ip'

# replace with username on host box
username = 'username on host'

# replace with the path to your private key
privatekey = '/path/to/privatekey'

# replace with your api key
apikey = 'api_key'


client = SSHClient()
client.load_host_keys(hosts)
client.load_system_host_keys()

client.connect(hostip, port=2222, username=username, key_filename=privatekey)

scp = SCPClient(client.get_transport())

logname = time.asctime(time.localtime(time.time()))

scp.get('/var/tmp/opencanary.log', '/home/' + username + '/logs/' + logname)
scp.close()

path = '/home/' + username + '/logs/' + logname

def getcategory(port):
    category = ''

    if port == 22:
        category = '18, 22'
    if port == 1433:
        category = '18, 14'
    if port == 21:
        category = '18, 5'
    if port == 6379:
        category = '18, 14'
    if port == 5000:
        category = '18, 14'
    if port == 23:
        category = '18'
    if port == 3306:
        category = '18'
    return category

def getcomments(port):
    comment = ''

    if port == 22:
        comment = '[!] Brute-force attempt: SSH on port 22'
    if port == 1433:
        comment = '[!] Unauthorized access attempt: mssql on port 1433'
    if port == 21:
        comment = '[!] Brute-force attempt: FTP on port 21'
    if port == 6379:
        comment = '[!] Unauthorized access attempt: redis on port 6379'
    if port == 5000:
        comment = '[!] Unauthorized access attempt: VNC on port 5000'
    if port == 23:
        comment = '[!] Brute-force attempt: telnet on port 23'
    if port == 3306:
        comment = '[!] Unauthorized access attempt: mysql on port 3306'
    return comment

def getlist(path):
    reportlist = []
    with open(path, 'r') as f:

        for line in f:
            # ignore empty lines
            if line == "\n":
                continue

            log = json.loads(line)

            if not log['src_host']:
                continue
            if log['dst_port'] == 2222:
                continue

            ip = log['src_host']
            port = log['dst_port']
            categories = getcategory(port)
            comments = getcomments(port)
            date = log['local_time']

            reportlist.append([ip, categories, comments, date])

    return reportlist

def reportIP(key, ip, categories, comments):
    payload = {'key': apikey, 'categories': categories, 'comment': comments, 'ip': ip}
    url = 'https://api.abuseipdb.com/api/v2/report'

    try:
        print(">> requesting report for " + ip)
        r = requests.post(url, params=payload)
        print(r.text + "\n")
    except:
        print("[!] an error has occured \n")

ips = getlist(path)
collectedips = []

for i in ips:
    if i[0] not in collectedips:
        collectedips.append(i[0])
        reportIP(apikey, i[0], i[1], i[2])
    else:
        continue
