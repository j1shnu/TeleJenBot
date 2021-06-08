import configparser


class Common:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()

        self.work_dir = "jenbot/work_dir"
        self.config_file = "jenbot/work_dir/config.ini"
        self.config.read(self.config_file)

        self.bot_session = self.config.get("bot-configuration", "SESSION")
        self.bot_api_key = self.config.get("bot-configuration", "API_KEY")
        self.chats = self.config.get("bot-configuration", "AUTHORIZED_CHATS")
        self.admin = self.config.get("bot-configuration", "ADMIN")

        self.jenkins_user = self.config.get("jenkins-credentials", "USERNAME")
        self.jenkins_password = self.config.get("jenkins-credentials", "PASSWORD")
        self.jenkins_url = self.config.get("jenkins-credentials", "URL")
        self.jenkins_name = self.config.get("jenkins-credentials", "NAME")