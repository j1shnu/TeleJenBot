# TeleJenBot

TeleJenBot is Telegram-Jenkins Bot written in _Python_ using [Pyrogram](https://github.com/pyrogram/pyrogram).

## INSTALLATION

Simply clone the repository and do the following.

- Move config.ini.TEMPLATE to config.ini

```sh
cd TeleJenBot/jenbot/work_dir/ && mv config.ini.TEMPLATE config.ini
```

Check <a href="https://github.com/j1shnu/TeleJenBot#variables">Variables</a> and edit the file as it says.

### Docker Method

- Install Docker by following the [official docker docs](https://docs.docker.com/engine/install)
- Start the Docker daemon by (Skip if already running)

```sh
dockerd
```

- Make sure Docker daemon running by

```sh
docker info
```

- Build the Docker Image by

```sh
docker build . -t telejenbot
```

- Run the container by

```sh
docker run -d --name jenkinsBot telejenbot
```

### Legacy Method

- Python 3.8 or higher version required.
- Install and run the bot by

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
- `ADMIN` : Set username or user id of the user who wants full control on the TeleJenBot.
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

- `/start` - Show you the bot owner and Jenkins version.
- `/getid` - Show you the chat/user id.
- `/auth` - Authorise a group or a particular user you're replying to.
- `/unauth` - This'll do the opposite of `/auth`.
- `/listauth` - Show you all chats and users those are authorised to use the bot.
- `/jobs` - Show you the available Jenkins jobs.
- `/showbuild` - Show you the running Builds.
