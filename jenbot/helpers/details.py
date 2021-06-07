from jenbot.helpers import jenkinServer


def get_version():
    return jenkinServer.get_version()


def get_jobs():
    """ Returns available jobs or None """
    try:
        return jenkinServer.get_jobs()
    except:
        return None


def get_job_details(jobName):
    """ Returns the details of a job or None """
    try:
        return jenkinServer.get_job_info(jobName)
    except:
        return None


def get_param_names(data) -> list:
    """ Return the parameter names """
    names = []
    for name in data[0]["parameterDefinitions"]:
        names.append(name["name"])
    return names


def get_param_datas(data, param):
    """ Returns the parameter details """
    for i in data[0]["parameterDefinitions"]:
        if i["name"] == param:
            return i