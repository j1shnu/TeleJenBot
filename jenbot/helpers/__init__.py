from jenkins import Jenkins

from jenbot import Common

Common = Common()
jenkinsUsername = Common.jenkins_user
jenkinsPassword = Common.jenkins_password
jenkinsUrl = Common.jenkins_url

jenkinServer = Jenkins(
    jenkinsUrl, username=jenkinsUsername, password=jenkinsPassword, timeout=5
)

user = jenkinServer.get_whoami()
