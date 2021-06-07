from pyrogram.types import Message
from asyncio import sleep
from pyrogram import filters, emoji

from jenbot.bot import JenkinsBot, JenkinsData


@JenkinsBot.on_message(filters.command("auth"))
async def authorize(c: JenkinsBot, m: Message):
    from_user = m.from_user
    if from_user.username == JenkinsData.admin or from_user.id == JenkinsData.admin:
        if m.reply_to_message:
            user = m.reply_to_message.from_user
            msg = f"`{user.username}` Already authorized. {emoji.MAN_SHRUGGING}"
            if user.id not in JenkinsData.authorized_chats:
                msg = f"Authorized `{user.username}` and who can directly use the bot."
                JenkinsData.authorized_chats.append(user.id)
        else:
            msg = f"Chat Already authorized. {emoji.MAN_SHRUGGING}"
            if m.chat.id not in JenkinsData.authorized_chats:
                JenkinsData.authorized_chats.append(m.chat.id)
                msg = "Chat authorized, Members can use the Bot here."
        reply_msg = await m.reply_text(msg)
        await sleep(10)
        await reply_msg.delete()


@JenkinsBot.on_message(filters.command("unauth"))
async def unauthorize(c: JenkinsBot, m: Message):
    from_user = m.from_user
    if from_user.username == JenkinsData.admin or from_user.id == JenkinsData.admin:
        if m.reply_to_message:
            user = m.reply_to_message.from_user
            msg = f"`{user.username}` Not in the authorized users list. {emoji.MAN_SHRUGGING}"
            if user.id in JenkinsData.authorized_chats:
                JenkinsData.authorized_chats.remove(user.id)
                msg = f"`{user.username}`'s authorization revoked."
        else:
            msg = f"Chat Not in the authorized chats list. {emoji.MAN_SHRUGGING}"
            if m.chat.id in JenkinsData.authorized_chats:
                msg = "Chat authorization revoked, Members can no longer use the Bot."
                JenkinsData.authorized_chats.remove(m.chat.id)
        reply_msg = await m.reply_text(msg)
        await sleep(10)
        await reply_msg.delete()


@JenkinsBot.on_message(filters.command("listauth"))
async def listAuthChats(c: JenkinsBot, m: Message):
    from_user = m.from_user
    if from_user.username == JenkinsData.admin or from_user.id == JenkinsData.admin:
        chats = [await c.get_chat(i) for i in JenkinsData.authorized_chats]
        msg = ""
        for chat in chats:
            msg += (
                f"`{chat.username}`(User)\n"
                if chat.type == "private"
                else f"`{chat.title}`(Group)\n"
            )
            text = f"Hi {m.from_user.mention},\nHere are the authorized chats list"
        reply_msg = await m.reply_text(f"{text}\n\n{msg}")
        await sleep(20)
        await reply_msg.delete()
