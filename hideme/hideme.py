#!venv/bin/python3.9

import subprocess
import json


def get_running_services():
    command = """systemctl list-units |grep hide\.me |grep -v "system-hide" |awk '{ print $1" " $4}'"""
    return list(filter(None,subprocess.check_output(command, shell=True).decode("UTF-8").split("\n")))


