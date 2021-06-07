
# TeleJenBot
A Telegram BOT To Manage Jenkins Jobs

#### Python 3 required
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
python3 -m jenbot
```
- If you're adding the bot to group chat then make sure the bot has admin privileges.
### Commands Available

- `/start`  -  This'll simply show you the bot owner and Jenkins version.
- `/getid`  -  This'll show you the current chat/user id.
- `/auth`   -  This authorise a group or a particular user you're replying to.
- `/unauth` -  This do the opposite of `/auth`.
- `/listauth` - This'll show you all chats and users are authorised to use the bot.
- `/jobs`   -  This'll show you the available Jenkins job in Inline Keyboard format.
