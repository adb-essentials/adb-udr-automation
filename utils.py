import json
import socket
import ipaddress
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

def get_srvc_tag_cidrs():
    cidr_ranges = []
    custom_command = "az network list-service-tags --location eastus --query \"values[?contains(name, 'Databricks')].[properties.addressPrefixes][][]\""
    run_custom_command = subprocess.run(
       custom_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # reading output and error
    execute_stdout = run_custom_command.stdout.decode("utf-8")
    cidr_ranges_raw = json.loads(execute_stdout)
    for cidr in cidr_ranges_raw:
        try:
            ipaddress.IPv4Network(cidr)
        except:
            print("Tags : " + cidr + " is not a valid V4 ip")
        else:
            cidr_ranges.append(cidr)
    return cidr_ranges

def get_srvc_tag_count(cidrs: list, srvctags: list):
    cidr_count = 0
    cidr_count_raw = len(cidrs)
    if cidr_count_raw == 0 : 
        return "n/a"

    is_srvctag = 'no'
    for cidr in cidrs:
        for srvctag_ip in srvctags:
            n1 = ipaddress.IPv4Network(cidr)
            n2 = ipaddress.IPv4Network(srvctag_ip)
            if n1.overlaps(n2) :
                cidr_count = cidr_count + 1 

    #if cidr_count > 0 : 

    if cidr_count == cidr_count_raw :
        is_srvctag = 'yes'

    return is_srvctag

def get_ip_list_whitelist(domain_str: str, table_num: int) -> list:
    # get ip list behind the given domain str
    ip_list = []
    ip_list_raw = []

    for dom in domain_str.split(' and ') :
        try:
            ais = socket.getaddrinfo(dom, 0, 0, 0, 0)
            for result in ais:
                ip_list.append(result[-1][0] + '/32')
            ip_list_raw = list(set(ip_list))
        except:
            ip_list_raw.append(dom)
            
    ip_list = []        
    for cidr in ip_list_raw:
        try:
            ipaddress.IPv4Network(cidr)
        except:
            print("Lookup : " + cidr + " did not resolve a valid ip")
        else:
            ip_list.append(cidr)
    
    return ip_list


def fuzzy_name_matcher(region_scraped: str, region_cli_dict: dict) -> str:
    # matching az region names with web-crawled regions names
    # for each scraped value region, we check from dict and patch the highest partial matched region
    # in most cases scraped value will find a very close / exact match from azcli results, we put a min_score to check and exclude 21vianet operated regions (China regions)
    # thus we can set a very high min_score in config
    cli_region_vals = region_cli_dict.keys()

    best_match = None
    max_score = 0

    for reg in cli_region_vals:
        test_score = rapidfuzz.fuzz.ratio(region_scraped, reg)
        # china regions operated by 21vianet
        if "china" in str(region_scraped).lower():
            return None
        else:
            if test_score >= max_score:
                # update max val and best match
                max_score = test_score
                best_match = region_cli_dict[reg]
    return best_match
