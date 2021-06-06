import asyncio
from time import sleep
from math import floor
from pyrogram import filters, emoji
from pyrogram.errors import FloodWait, BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from jenbot.helpers import build
from jenbot.helpers import message_template
from jenbot.bot import JenkinsBot, JenkinsData
from jenbot.helpers.details import (
    get_jobs,
    get_job_details,
    get_param_names,
    get_param_datas,
)


@JenkinsBot.on_callback_query(filters.regex("^jobs_\d{0,2}$"))
async def show_jobs(c: JenkinsBot, m: CallbackQuery, call_from_code=False):
    """ This will Show the Jobs available in Jenkins Server """
    if not call_from_code:
        jobs = JenkinsData.jobs
        callback_data = m.data.split("_")[1]
        job_name = jobs[int(callback_data)]["name"]
        JenkinsData.job_params = (
            {} if JenkinsData.job_name != job_name else JenkinsData.job_params
        )
        JenkinsData.job_name = job_name

    job_details = get_job_details(jobName=JenkinsData.job_name)
    if not job_details:
        return bool(
            await m.answer("Error Fetching Details...! Try Again.", show_alert=True)
        )

    params, msg_params, markup = [], "", []
    if job_details["property"]:
        params = get_param_names(job_details["property"])
        for param in params:
            if not JenkinsData.job_params.get(param):
                JenkinsData.job_params[param] = ""
        markup = [
            [InlineKeyboardButton(param, callback_data=f"param_{id}")]
            for id, param in enumerate(params)
        ]
        msg_params = message_template.Template.generate_param_template(
            param_data=JenkinsData.job_params
        )
    markup.append(
        [
            InlineKeyboardButton(
                f"BUILD NOW {emoji.MAN_CONSTRUCTION_WORKER}",
                callback_data="start_build",
            )
        ],
    )
    markup.append(
        [InlineKeyboardButton(f"Back {emoji.BACK_ARROW}", callback_data="back2main")],
    )

    msg_text = message_template.Template.MESSAGE.format(
        job_name=JenkinsData.job_name,
        jobURL=job_details["url"],
        lastBuildURL=job_details["lastBuild"]["url"] or None,
        description=job_details["description"] or None,
        paramNum=len(params),
    )

    msg_description = (
        "Press **BUILD NOW** to start build."
        if not job_details["property"]
        else "Select Below listed Parameters to update."
    )
    msg_text = f"{msg_text}{msg_params}{msg_description}"
    try:
        await m.message.edit(text=msg_text, reply_markup=InlineKeyboardMarkup(markup))
    except:
        await m.edit(text=msg_text, reply_markup=InlineKeyboardMarkup(markup))


@JenkinsBot.on_callback_query(filters.regex("^param_[0-9]$"))
async def param_manager(c: JenkinsBot, m: CallbackQuery):
    for button in m.message.reply_markup.inline_keyboard:
        if button[0].callback_data == m.data:
            selected_param = button[0].text
            job_details = get_job_details(jobName=JenkinsData.job_name)
            if not job_details:
                return bool(
                    await m.answer(
                        text="Error Fetching Details...! Try Again.", show_alert=True
                    )
                )
            param_detail = get_param_datas(job_details["property"], selected_param)
            break
    msg = None
    if param_detail["type"] == "ChoiceParameterDefinition":
        markup = [
            [
                InlineKeyboardButton(
                    choice, callback_data=f"pselect_=_{param_detail['name']}_=_{choice}"
                )
            ]
            for id, choice in enumerate(param_detail["choices"])
        ]
    elif param_detail["type"] == "BooleanParameterDefinition":
        markup = [
            [
                InlineKeyboardButton(
                    f"YES {emoji.CHECK_MARK_BUTTON}",
                    callback_data=f"pselect_=_{param_detail['name']}_=_True",
                )
            ],
            [
                InlineKeyboardButton(
                    f"NO {emoji.CROSS_MARK}",
                    callback_data=f"pselect_=_{param_detail['name']}_=_False",
                )
            ],
        ]
    elif param_detail["type"] == "StringParameterDefinition":
        msg = message_template.Template.STRING_PARAM.format(
            description=param_detail["description"], param=param_detail["name"]
        )
        markup = []
    markup.append(
        [InlineKeyboardButton(f"Back {emoji.BACK_ARROW}", callback_data="back2params")]
    )
    msg_text = msg if msg else f"__{param_detail['description']}__"
    await m.message.edit(text=msg_text, reply_markup=InlineKeyboardMarkup(markup))


@JenkinsBot.on_callback_query(filters.regex("^start_build$"))
async def start_buid(c: JenkinsBot, m: CallbackQuery):
    job_details = get_job_details(jobName=JenkinsData.job_name)
    if not job_details:
        return bool(
            await m.answer("Error Fetching Details...! Try Again.", show_alert=True)
        )
    params = get_param_names(job_details["property"]) if job_details["property"] else []
    msg_text = message_template.Template.MESSAGE.format(
        job_name=JenkinsData.job_name,
        jobURL=job_details["url"],
        lastBuildURL=job_details["lastBuild"]["url"] or None,
        description=job_details["description"] or None,
        paramNum=len(params),
    )
    await m.message.edit("Starting **BUILD**....")
    build_info = build.start_build(JenkinsData.job_name, JenkinsData.job_params)
    if not build_info:
        await m.answer(
            "Error Fetching Details To Start The Build. Try Again..!", show_alert=True
        )
        return bool(await m.message.delete())
    await m.message.edit(text=f"{msg_text}\n**BUILD Started.**")
    percentage_old = 0
    while not build.is_finished(JenkinsData.job_name, build_info["build_num"]):
        progressbar = "{}{}"
        eta = build.get_eta(JenkinsData.job_name, build_info["build_num"])
        percentage = build.get_percentage(build_info["start_time"], eta)
        if percentage != percentage_old:
            progressbar = progressbar.format(
                "".join(("█" for _ in range(floor(percentage / 5)))),
                "".join(("░" for _ in range(20 - floor(percentage / 5)))),
            )
            try:
                await m.message.edit(
                    text=f"{msg_text}**BUILD Started.**\n{progressbar} {percentage}%"
                )
            except FloodWait as e:
                sleep(e.x)
            except BadRequest as e:
                pass
        percentage_old = percentage
    else:
        build_finished = build.is_finished(
            JenkinsData.job_name, build_info["build_num"]
        )
        if build_finished == "SUCCESS":
            await m.message.edit(text=msg_text + "**BUILD COMPLETED**")
        elif build_finished == "FAILURE":
            await m.message.edit(text=msg_text + "**BUILD FAILED**")


@JenkinsBot.on_callback_query(filters.regex("^back2main$"))
async def back_to_main(c: JenkinsBot, m: CallbackQuery):
    jobs = get_jobs()
    if not jobs:
        return bool(
            await m.answer(text="Error Fetching Jobs, try again", show_alert=True)
        )
    JenkinsData.jobs = jobs
    jobs = [job["name"] for job in jobs]
    await m.message.edit(
        "Available Jobs",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{id}. {job}", callback_data=f"jobs_{id}")]
                for id, job in enumerate(jobs)
            ]
        ),
    )


@JenkinsBot.on_callback_query(filters.regex("^back2params$"))
async def back_to_params(c: JenkinsBot, m: CallbackQuery):
    await show_jobs(c, m, True)


@JenkinsBot.on_callback_query(filters.regex("^pselect_*"))
async def set_params(c: JenkinsBot, m: CallbackQuery):
    select, param, value = m.data.split("_=_")
    JenkinsData.job_params[param] = value
    await back_to_params(c, m)


@JenkinsBot.on_message(filters.reply & filters.regex("^\w+\s\=\s\w+$"))
async def reply_msg_handler(c: JenkinsBot, m: Message):
    text = m.text.split("=")
    param = text[0].strip()
    value = text[1].strip()
    msg = m
    if param not in JenkinsData.job_params.keys():
        await m.delete()
        new_msg = await c.send_message(
            chat_id=m.chat.id,
            text=f"Hi {m.from_user.mention}, \nInvalid Parameter or Data..!\n\nMessage will be Auto Deleted in 5Secs",
        )
        await asyncio.sleep(5)
        return bool(await new_msg.delete())
    JenkinsData.job_params[param] = value
    await m.delete()
    await back_to_params(c, msg.reply_to_message)