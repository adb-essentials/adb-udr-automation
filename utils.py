import json
import socket
import subprocess

import pandas as pd
import rapidfuzz


def get_az_regions_dict() -> dict:
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


def get_ip_list_whitelist(domain_str: str) -> list:
    # get ip list behind the given domain str
    ip_list = []
    ais = socket.getaddrinfo(domain_str, 0, 0, 0, 0)
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    return ip_list


def compute_whitelist_ips():
    None


def fuzzy_name_matcher(region_scraped: str, region_cli_dict: dict) -> str:
    # matching az region names with web-crawled regions names
    # for each scraped value region, we check from dict and patch the highest partial matched region
    cli_region_vals = region_cli_dict.keys()

    best_match = None
    max_score = 0

    for reg in cli_region_vals:
        test_score = rapidfuzz.fuzz.ratio(region_scraped, reg)
        if test_score >= max_score:
            # update max val and best match
            max_score = test_score
            #best_match = [region_scraped, reg, region_cli_dict[reg]]
            best_match = region_cli_dict[reg]

    return best_match
