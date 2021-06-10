from pyrogram import filters, emoji
from pyrogram.types import Message

from jenbot.bot import JenkinsBot, delete_msg


@JenkinsBot.on_message(filters.command("help"))
async def help(c: JenkinsBot, m: Message):
    msg = (
        f"Hi `{m.from_user.username}`..!\n"
        f"I'm a Jenkins BOT{emoji.ROBOT} built by [Jishnu](https://github.com/j1shnu)."
        "I'll help you manage your Jenkins jobs from Telegram.\n\n"
        "**--Available commands.--**\n"
        "`/start`  -  __Start and show you the bot owner and Jenkins version.__ \n"
        "`/getid`  -  __Show you the current chat/user id.__\n"
        "`/auth`   -  __Authorize a group or a particular user you're replying to.__\n"
        "`/unauth` -  __Oposite of `/auth`.__\n"
        "`/listauth` - __Show you all chats and users are authorized to use the bot.__\n"
        "`/jobs`   -  __Show you the available Jenkins job in InlineKeyboard format.__\n"
        "`/showbuild` - __Show you the running Builds.__\n\n"
        f"And more features are coming...{emoji.SMILING_CAT_WITH_HEART_EYES}"
    )

    msg = await m.reply_text(msg, disable_web_page_preview=True)
    return await delete_msg(msg, 30)
