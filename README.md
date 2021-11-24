# adb_udr_automation

## What's this project about?

Reference documentation:
https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/udr


On Azure Databricks, some control plane services have non-static IP, this project is to automate the job of scraping IP from Azure official doc and to patch Azure firewall network rules.

## How to use this project:
1. Clone this repo to your local.
2. In the folder, setup your local env by: `make setup`, this will install requirements.txt
3. `make run` will generate 2 csv files in `outputs` folder.

In `/outputs`, Table 1 contains: 

| region            | attribute                              | value                                    | az_region_to_deploy_fuzzy_match | whitelistips      |
| ----------------- | -------------------------------------- | ---------------------------------------- | ------------------------------- | ----------------- |
| Australia Central | Webapp                                 | 13.75.218.172/32                         | australiacentral                | []                |
| Australia Central | SCC relay (if CC is enabled)           | tunnel.australiaeast.azuredatabricks.net | australiacentral                | ['13.75.164.249'] |
| Australia Central | Control Plane NAT (if SCC is disabled) | 13.70.105.50/32                          | australiacentral                | []                |
| Australia Central | Extended infrastructure                | 20.53.145.128/28                         | australiacentral                | []                |


Table 2 contains:

| region            | attribute                       | value                                                                 | az_region_to_deploy_fuzzy_match | whitelistips      |
| ----------------- | ------------------------------- | --------------------------------------------------------------------- | ------------------------------- | ----------------- |
| Australia Central | Metastore                       | consolidated-australiacentral-prod-metastore.mysql.database.azure.com | australiacentral                | ['20.36.105.0']   |
| Australia Central | Artifact Blob storage primary   | dbartifactsprodaustc.blob.core.windows.net                            | australiacentral                | ['52.239.216.36'] |
| Australia Central | Artifact Blob storage secondary | secondary,dbartifactsprodaustc2.blob.core.windows.net                 | australiacentral                | ['52.239.218.4']  |
| Australia Central | Log Blob storage                | storage,dblogprodausteast.blob.core.windows.net                       | australiacentral                | ['20.150.66.228'] |
| Australia Central | Event Hub endpoint              | prod-australiaeast-observabilityeventhubs.servicebus.windows.net      | australiacentral                | ['13.70.72.2']    |
