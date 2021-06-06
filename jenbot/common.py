import configparser


class Common:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()

        self.work_dir = "jenbot/work_dir"
        self.config_file = "jenbot/work_dir/config.ini"
        self.config.read(self.config_file)

        self.bot_session = self.config.get("bot-configuration", "session")
        self.bot_api_key = self.config.get("bot-configuration", "api_key")
        self.chats = self.config.get("bot-configuration", "authorized_chats")

        self.jenkins_user = self.config.get("jenkins-credentials", "username")
        self.jenkins_password = self.config.get("jenkins-credentials", "password")
        self.jenkins_url = self.config.get("jenkins-credentials", "url")
        self.jenkins_name = self.config.get("jenkins-credentials", "name")