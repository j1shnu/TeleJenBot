from jenbot import logging
from jenbot.helpers import jenkinServer


def get_version():
    return jenkinServer.get_version()


def get_jobs():
    """Returns available jobs or None"""
    try:
        return jenkinServer.get_jobs()
    except Exception as e:
        logging.error(f"Error getting jobs, {e}")
        return None


def get_job_details(jobName):
    """Returns the details of a job or None"""
    try:
        return jenkinServer.get_job_info(jobName)
    except Exception as e:
        logging.error(f"Error getting job details, {e}")
        return None


def get_param_names(datas) -> list:
    """Return the parameter names"""
    names = []
    for data in datas:
        if "parameterDefinitions" in data.keys():
            for name in data["parameterDefinitions"]:
                names.append(name["name"])
            return names


def get_param_datas(datas, param):
    """Returns the parameter details"""
    for data in datas:
        if "parameterDefinitions" in data.keys():
            for i in data["parameterDefinitions"]:
                if i["name"] == param:
                    return i


def get_default_value(datas, param):
    """Return the default value of a parameter"""
    param_data = get_param_datas(datas, param)
    return param_data["defaultParameterValue"]["value"]


def get_running_builds() -> list:
    builds = jenkinServer.get_running_builds()
    if not builds:
        return []
    output = []
    for build in builds:
        output.append(
            {"name": build["name"], "url": build["url"], "number": build["number"]}
        )
    return output


def is_buildable(job_name) -> str:
    running_builds = get_running_builds()
    if running_builds:
        for build in running_builds:
            if build["name"] == job_name:
                return "Building.."
    return "Ready to Build"
