# Kurgan AI - Web Application Security Analyzer
## [http://www.kurgan.com.br/](http://www.kurgan.com.br/)


### How Kurgan AI works?

<p>MasterAgent is loaded waiting for receive a Url Target and options of 
configuration. When he receives that, he try understand what the user wants.</p>

<p>If he only receives url target without any options, then he load POMDP to 
run Default Actions and Default Goals.</p> 

<p>After that, Master Agent executes phase one - reconnaissance - where he try 
mapping what resources and technologies are running in webserver of target URL.</p>

<p>Next phase is try to discovery some vulnerabilities, run crawlers and check for 
protections.</p>

<p>The last phase is to attack the target. Load and run some agents responsible for
testing many class of attacks.</p>
 
### Diagrams

| Phase | Description         | Actions          |
|:-----:|:-------------------:| :---------------:|
|   0   | Configuration Scene | Set Url Target   |
|       |                     | set Goal         | 
|       |                     | Load POMDP files |
|   1   | Reconnaissance      |Capture Webserver |
|       |                     |App Framework     |

'''
Configuration Scene:
    - set Target;
    - set Goal;
    - Load POMDP Files;
'''


'''
Phase 1 - Reconnaissance's Agents
    - WebServer
    - App Framework
    - Other Technology
'''


'''
Phase 2 - Scanners's Agents
    - Check for public vulnerabilities(DB vuln)
    - Crawling
    - Check for protections layers(WAF, anti-CSRF, etc);
    - Finding entry points;
'''


'''
Phase 3 - Attack's Agents
    - Run exploits
    - Run attacks
    - Try find new vulnerabilities
'''

### Usage

