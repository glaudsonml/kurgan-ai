'''
Configuration file.
'''
VERSION="0.2.2"
PHASE1=True
PHASE2=True
PHASE3=True
FOLLOW_URL=True
SPIDER_GET_ALL_LINKS=False


KURGAN_HOME="/home/glaudson/workspace/Kurgan-Framework/"

BRUTEFORCE_LOGIN_FILE="wordlists/logins_simple.txt"
BRUTEFORCE_PASSWORD_FILE="wordlists/passwords_simple.txt"


CRAWLING_GET_ALL_LINKS=False


#Database SQLite
DB_WEBSERVERS="db/webservers.db"


#Stomp Credentials
STOMP_USERNAME = "admin"
STOMP_PASSWORD = "KuRg4nLives!"
STOMP_TOPIC = "/topic/kurgan"

#Agent list
AGENTS_DIR="./agents/"
AGENTS_FILES = ["masterAgent","agentTarget","agentWebInfra","agentPageClassifier","agentSpider","agentBruteForce"]
#AgentBackup Configurations


#Apache Apollo Stomp
APACHE_APOLLO_CMD="/infra/stomp/kurgan/bin/apollo-broker-service"

#Binaries
PHANTOMJS="/usr/bin/phantomjs"
CHROME_HEADLESS="/usr/bin/google-chrome"