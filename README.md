# WinnieTheBlue

### **Hello everyone!**

With all this talk of home labs, I wanted to quickly share a personal project that I've been working on that recently came to fruition. 

#### Enter… Honeypot!

Over the past week, I’ve built a cloud-hosted honeypot, paired with an automated log collector/parser that ingests logs from OpenCanary (the open source and lightweight honeypot framework utilized in this project) and reports each threat IP to AbuseIPDB. Both systems (the honeypot and the log-collector) run on a debian-based AWS EC2 micro instance, meaning that I was able to achieve all of this at absolutely ***ZERO COST***.

I thought this might be worth sharing for those that want to get into detection engineering or security research, but do not have the money to spend on physical infrastructure.

My AbuseIPDB profile: https://www.abuseipdb.com/user/57866

<a href="https://www.abuseipdb.com/user/57866" title="AbuseIPDB is an IP address blacklist for webmasters and sysadmins to report IP addresses engaging in abusive behavior on their networks" alt="AbuseIPDB Contributor Badge">
	<img src="https://www.abuseipdb.com/contributor/57866.svg" style="width: 401px;">
</a>

*I followed a writeup from https://m4lwhere.org/ for this project. I highly recommend checking out his site for more info on honeypots and their general purpose.*

#### **What is a honeypot?**

A honeypot is a networked system strategically placed to attract the attention of automated or targeted threat actors. Becasue I have no on-prem infrastructure to protect, my honeypot is accessible to anyone over the web.

#### **How does it work?**

The honeypot is running several different [fake] services, including: FTP (21), SSH (22), Telnet (23), MSSQL (1433), MYSQL (3306), VNC (5000), and redis (6379). Anytime someone attempts to access or enumerate these services, an event is logged to ```/var/tmp/opencanary.log```. 

Events from OpenCanary are logged in json: 

```
{"dst_host": "172.31.14.62", "dst_port": 3306, "local_time": "2021-05-24 14:20:04.732789", "local_time_adjusted": "2021-05-24 14:20:04.732827", "logdata": {"PASSWORD": null, "USERNAME": "root"}, "logtype": 8001, "node_id": "winniethepooh", "src_host": "34.76.80.167", "src_port": 52956, "utc_time": "2021-05-24 14:20:04.732820"}
```

#### **What do you do with the logs?**

You can do all sort of things with these logs. You could perform some data visualization based on geolocation to see where most of the malicious traffic is coming from. You could perform frequency analysis on credentials to see what usernames and passwords are most likely to be attempted. You might even customize service signatures to see if a particular version of a service is abused more often than another. Really the possibilities are only limited by how creative you want to get with it. 

For me, I am using a custom python script and daily cronjob to retrieve, parse, and report these threat IPs to AbuseIPDB. 

Here is a link to the repo containing my python script: https://github.com/tyrioslol/winnietheblue

#### **Conclusion:** 

I wanted to share my experience in building this honeypot with hopes that home/detection labs can be more approachable for people looking to get started. This is also an easy project with a huge payoff that you can add to your resume or portfolio.
