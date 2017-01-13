'''
Configuration file.
'''
VERSION="0.2.2"
PHASE1=True
PHASE2=True
PHASE3=True
FOLLOW_URL=True
CRAWLING_GET_ALL_LINKS=False


#Database SQLite
DB_WEBSERVERS="db/webservers.db"


#Stomp Credentials
STOMP_USERNAME = "admin"
STOMP_PASSWORD = "password"
STOMP_TOPIC = "/topic/kurgan"

#Agent list
AGENTS_DIR="./agents/"
AGENTS = ["masterAgent","agentBackup","agentTarget","agentWebInfra"]
#AgentBackup Configurations


#Apache Apollo Stomp
APACHE_APOLLO="/usr/local/kurgan/apache-apollo-1.7.1/kurgan$ sudo bin/apollo-broker-service"

#Binaries
PHANTOMJS="/usr/bin/phantomjs"