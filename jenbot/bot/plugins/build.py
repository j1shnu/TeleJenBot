from time import sleep
from math import floor
from pyrogram import filters
from asyncio import sleep as aiosleep
from pyrogram.types import CallbackQuery
from pyrogram.errors import FloodWait, BadRequest

from jenbot.bot import JenkinsData, JenkinsBot
from jenbot.helpers import build, message_template
from jenbot.helpers.details import get_job_details, get_param_names


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
    await aiosleep(3)
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
                infoTxt = "\n__(Progress bar may not be 100% accurate.)__"
                await m.message.edit(
                    text=f"{msg_text}**BUILD Started.**\n{progressbar} {percentage}%{infoTxt}"
                )
                await aiosleep(JenkinsData.sleep_time)
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
