# adb_udr_automation

## What's this project about?

Reference documentation:
https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/udr


On Azure Databricks, some control plane services have non-static IP, this project is to automate the job of scraping IP from Azure official doc and to patch Azure firewall network rules.

How to run this:
1. Clone this repo to your local.
2. In the folder, setup your local env by: `make setup`, this will install requirements.txt
3. `make run` will generate csv files in `outputs` folder.
