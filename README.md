# TeleJenBot

TeleJenBot is Telegram-Jenkins Bot written in _Python_ using [Pyrogram](https://github.com/pyrogram/pyrogram).

#### Python 3 required

## INSTALLATION

Simply clone the repository and do the following.

- Move config.ini.TEMPLATE to config.ini

```sh
cd TeleJenBot/jenbot/work_dir/ && mv config.ini.TEMPLATE config.ini
```

Check <a href="https://github.com/j1shnu/TeleJenBot#variables">Variabled</a> and edit the file as it says.

- Follow these steps to start the bot.

```sh
cd TeleJenBot
python3 -m venv venv
. ./venv/bin/active
pip install -r requirements.txt
python3 -m jenbot
```

- If you're adding the bot to group chat then make sure the bot has admin privileges.

## Variables

#### Mandatory Variables

- `API_ID` , `API_HASH` : Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).
- `API_KEY` : Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.
- `ADMIN` : Set username or userid of the user who wants full control on the TeleJenBot.
- `USERNAME` : Username of your Jenkins server.
- `PASSWORD` : Password or API KEY to access the Jenkins server.
- `URL` : URL of your Jenkins server.
  - Example : http://localhost:8080 or https://jenkins.myserver.com
- `NAME` : Name the who is using the bot to show in bot message.
  - Example : If you set NAME = foo , Then the bot'll reply "This is foo's Bot"

#### Optional Variables

- `AUTHORIZED_CHATS` : Add the id of group or user who want to access the bot. Use `/getid` to see the id.
  - Example : AUTHORIZED_CHATS = [id1, id2, id3]
- `SESSION` : You can edit or leave it the same. BTW don't leave it empty.

## Commands Available

- `/start` - This'll simply show you the bot owner and Jenkins version.
- `/getid` - This'll show you the current chat/user id.
- `/auth` - This authorise a group or a particular user you're replying to.
- `/unauth` - This do the opposite of `/auth`.
- `/listauth` - This'll show you all chats and users are authorised to use the bot.
- `/jobs` - This'll show you the available Jenkins job in Inline Keyboard format.
- `/showbuild` - This'll show you the running Builds.
