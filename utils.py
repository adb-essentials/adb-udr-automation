import json
import socket
import subprocess

import pandas as pd
import rapidfuzz


def get_az_regions_dict():
    # run any custom command as a string
    custom_command = """az account list-locations --query "[].{azregion_humanread:displayName, azregion_terraform:name}" -o json"""
    # use 'shell = True' as Azure CLI installed on system is accessible from native Shell
    # using 'subprocess.PIPE' will return stderr and stdout to create_app object
    run_custom_command = subprocess.run(
        custom_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # reading output and error
    execute_stdout = run_custom_command.stdout.decode("utf-8")
    stdout_az_regions = json.loads(execute_stdout)

    az_regions_df = pd.DataFrame(stdout_az_regions)
    az_region_dict = az_regions_df.set_index('azregion_humanread')[
        'azregion_terraform'].to_dict()

    return az_region_dict


def get_ip_list_whitelist(domain_str):
    # get ip list behind the given domain str
    ip_list = []
    ais = socket.getaddrinfo(domain_str, 0, 0, 0, 0)
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    return ip_list


def fuzze_name_matcher():
    # matching az region names with web-crawled regions names
    print(rapidfuzz.fuzz.ratio("this is a test", "this is a test!"))
    None
