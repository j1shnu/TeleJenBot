from pyrogram.types import Message
from pyrogram import filters, emoji

from jenbot.bot import JenkinsBot, JenkinsData, delete_msg


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
        return await delete_msg(reply_msg, 10)


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
        return await delete_msg(reply_msg, 10)


@JenkinsBot.on_message(filters.command("listauth"))
async def listAuthChats(c: JenkinsBot, m: Message):
    from_user = m.from_user
    if from_user.username == JenkinsData.admin or from_user.id == JenkinsData.admin:
        if not JenkinsData.authorized_chats:
            reply_msg = await m.reply_text(
                f"Hi {from_user.username}, I'm not authorized with any chats now."
            )
            return await delete_msg(reply_msg, 10)
        chats = [await c.get_chat(i) for i in JenkinsData.authorized_chats]
        msg = ""
        for chat in chats:
            msg += (
                f"`{chat.username}`(User)\n"
                if chat.type == "private"
                else f"`{chat.title}`(Group)\n"
            )
            text = f"Hi {from_user.username},\nHere are the authorized chats list"
        reply_msg = await m.reply_text(f"{text}\n\n{msg}")
        return await delete_msg(reply_msg, 20)
