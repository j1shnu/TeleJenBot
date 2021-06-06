# TeleJenBot
A Telegram BOT To Manage Jenkins Jobs

#### Python3 required
### INSTALLATION

Simply clone the repository and do the following.
- Move config.ini.TEMPLATE to config.ini
```sh
cd TeleJenBot/jenbot/work_dir/ ; mv config.ini.TEMPLATE config.ini
```
Edit the file as it says.
- Follow these steps to start the bot
```sh
cd TeleJenBot
python3 -m venv venv
. ./venv/bin/active
pip install -r requirements.txt
python -m jenbot
```
### Commands Available

/start  -  Show Bot and Jenkins info.
/jobs   -  Show jobs available in Jenkins Server.