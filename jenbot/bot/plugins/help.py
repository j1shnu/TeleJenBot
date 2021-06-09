from pyrogram import filters, emoji
from pyrogram.types import Message

from jenbot.bot import JenkinsBot


@JenkinsBot.on_message(filters.command("help"))
async def help(c: JenkinsBot, m: Message):
    msg = (
        f"Hi `{m.from_user.username}`..!\n"
        f"I'm a Jenkins BOT{emoji.ROBOT} built by [Jishnu](https://github.com/j1shnu)."
        "I'll help you manage your Jenkins jobs from Telegram.\n\n"
        "**--Available commands.--**\n"
        "`/start`  -  __This'll simply show you the bot owner and Jenkins version.__ \n"
        "`/getid`  -  __This'll show you the current chat/user id.__\n"
        "`/auth`   -  __This authorize a group or a particular user you're replying to.__\n"
        "`/unauth` -  __This do the oposite of `/auth`.__\n"
        "`/listauth` - __This'll show you all chats and users are authorized to use the bot.__\n"
        "`/jobs`   -  __This'll show you the available Jenkins job in InlineKeyboard format.__\n"
        "`/showbuild` - __This'll show you the running Builds.__\n\n"
        f"And more features are coming...{emoji.SMILING_CAT_WITH_HEART_EYES}"
    )

    await m.reply_text(msg, disable_web_page_preview=True)