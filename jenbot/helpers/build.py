from time import time, sleep

from jenbot import logging
from jenbot.bot import JenkinsData
from jenbot.helpers import jenkinServer
from jenbot.helpers.details import get_job_details


def start_build(jobName, params):
    job_details = get_job_details(jobName)
    if not job_details:
        return None
    nextBuildNo = job_details["nextBuildNumber"]
    try:
        jenkinServer.crumb = None  # Removing current crumb to get new one(will auto generate on build start).
        jenkinServer.build_job(jobName, parameters=params)
        sleep(10)
        while jenkinServer.get_queue_info():
            pass
        started_time = round(time())
        build_info = jenkinServer.get_build_info(jobName, nextBuildNo)
        return {
            "url": build_info["url"],
            "start_time": started_time,
            "build_num": nextBuildNo,
        }
    except Exception as e:
        logging.error(e)
        return None


def get_eta(jobName, buildNum) -> int:
    build_info = jenkinServer.get_build_info(jobName, buildNum)
    return round(build_info["estimatedDuration"] / 1000)


def is_finished(jobName, buildNum):
    build_info = jenkinServer.get_build_info(jobName, buildNum)
    return build_info["result"]


# https://stackoverflow.com/a/5723075
def get_percentage(started: int, eta: int) -> int:
    now = round(time())
    if now > started + eta:
        eta = now + eta
        JenkinsData.sleep_time += 2
    else:
        eta = started + eta
    return round((now - started) / (eta - started) * 100)
