# abuseipdb

### **Hello everyone!**

With all this talk of home labs, I wanted to quickly share a personal project that I have been working on that recently came to fruition. Enter… Honeypot!
Over the past week I’ve created a fully functioning honeypot, paired with an automated log collector/parser that ingests logs from OpenCanary (the open source and lightweight honeypot framework utilized in the project) and reports each threat IP to AbuseIPDB. Both systems (the honeypot and the log-collector) run on an AWS EC2 debian-based micro instance, meaning that I was able to achieve all of this at absolutely ***ZERO COST***.

I thought this might be worth sharing for those that want to get into detection engineering or home lab methodologies, but do not have the money to spend for on-site gear.

My AbuseIPDB profile: https://www.abuseipdb.com/user/57866

<a href="https://www.abuseipdb.com/user/57866" title="AbuseIPDB is an IP address blacklist for webmasters and sysadmins to report IP addresses engaging in abusive behavior on their networks" alt="AbuseIPDB Contributor Badge">
	<img src="https://www.abuseipdb.com/contributor/57866.svg" style="width: 401px;">
</a>

*I took heavy inspiration for this project from https://m4lwhere.org/ who, if you are familiar, was the winner of the NCL Spring Preseason Individual event.*

#### **What is a honeypot?**

A honeypot is a networked system put in place to intentionally attract the attention of automated or targeted threat actors over the web or on a LAN with the hopes of detecting and actioning malicious activity. Since I have no current infrastructure to protect, my honeypot is accessible to anyone over the web.

#### **How does it work?**

My honeypot is running several different [fake] services, including: FTP(21), SSH (22), Telnet (23), MSSQL (1433), MYSQL (3306), VNC (5000), and redis (6379). Anytime someone that is not me attempts to access or scan these services; an event is created that is then logged to the opencanary event log. 

Events from OpenCanary are logged in json format and look like this: 

```
{"dst_host": "172.31.14.62", "dst_port": 3306, "local_time": "2021-05-24 14:20:04.732789", "local_time_adjusted": "2021-05-24 14:20:04.732827", "logdata": {"PASSWORD": null, "USERNAME": "root"}, "logtype": 8001, "node_id": "winniethepooh", "src_host": "34.76.80.167", "src_port": 52956, "utc_time": "2021-05-24 14:20:04.732820"}
```

#### **What to do with the logs?**

You can do all sort of things with these logs. You could perform some data visualization to see where most of the malicious traffic is coming from. You could perform frequency analysis on credentials to see what usernames and passwords are most likely to be attempted. You might even customize service signatures to see if a particular version of a service is abused more often than another. Really the possibilities are only limited by how creative you want to get with it. 

For me, I am using a custom python script and daily cronjob to retrieve, parse, and report these threat IP’s to AbuseIPDB. I am also additional analysis on any anomalous activity in the logs that piques my interest. 

Here is a link to the repo containing my python script: https://github.com/tyrioslol/abuseipdb

#### **Conclusion:** 

I wanted to share my experience with building this honeypot in hopes that home labs and detection labs can be more approachable for people looking to get started. This is also an easy project with a huge payoff that you can add to your resume or portfolio. 
If you have any questions, you can always ping me on discord @tyrios. 

*p.s. I highly recommend reading m4lwhere’s blog on his website if you are interested in doing this yourself.*

