from os import linesep


class Template:
    MESSAGE = (
        "**Project Name** : **--[{job_name}]({jobURL})--**\n\n"
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
