class Template:
    MESSAGE = (
        "**Project Name** : **--[{job_name}]({jobURL})--**  {color}\n\n"
        + "**Description** : __{description}__\n"
        + "**No. of Parameters** : {paramNum}\n"
        + "[Last Build]({lastBuildURL})\n\n"
    )
    STRING_PARAM = (
        "**Description**  : __{description}__\n\n"
        + "You Should Send the Value to this Message Reply In Below Format.\n"
        + "`{param} = value`\n"
        + "(Tap to copy the format.)"
    )

    def generate_param_template(param_data: dict) -> str:
        text_msg = "**--Parameters--**\n"
        params = "`{key} = {value}`\n"
        for key in param_data:
            text_msg += params.format(key=key, value=param_data[key])
        text_msg += "\n"
        return text_msg

    def generate_builds_template(builds_data: list) -> str:
        text_msg = ""
        builds = "**{num}**. [{name}]({url}) ([ConsoleLog]({logurl}))\n"
        for i, build in enumerate(builds_data):
            text_msg += builds.format(
                num=i + 1,
                name=build["name"],
                url=build["url"],
                logurl=f"{build['url']}/console",
            )
        return text_msg
