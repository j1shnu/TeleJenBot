from time import time
from jenbot.helpers import jenkinServer
from jenbot.helpers.details import get_job_details
from jenbot.bot import JenkinsData


def start_build(jobName, params):
    job_details = get_job_details(jobName)
    if not job_details:
        return None
    nextBuildNo = job_details["nextBuildNumber"]
    try:
        jenkinServer.build_job(jobName, parameters=params)
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