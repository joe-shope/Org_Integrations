import requests
import json
import argparse
import os

parser = argparse.ArgumentParser(description='group: input the group id for which you would like to update all orgs within.')
parser.add_argument("--group")
args = parser.parse_args()
group_id = args.group


if "SNYK_TOKEN" in os.environ:
    snyk_token = os.environ['SNYK_TOKEN']
else:
    print("Enter your Snyk API Token") 
    snyk_token = input()

if group_id != '':
    print("Enter your Group ID")
    group_id = input()

print('Type the integration you would like to query: ex. azure-repos, bitbucket-connect-app, bitbucket-cloud, github, github-enterprise, github-cloud-app, gitlab')
integration = input()

org_response = requests.get(f'https://api.snyk.io/rest/groups/{group_id}/orgs?version=2024-03-12%7Eexperimental', headers={'Authorization': f'Token {snyk_token}'})
org_res = org_response.json()
od = org_res['data']

for i in od:
    org_id = i['id']
    org_name = i['attributes']['name']
    integration_response = requests.get(f'https://api.snyk.io/v1/org/{org_id}/integrations', headers={'Authorization': f'Token {snyk_token}', 'Content-Type': 'application/json; charset=utf-8'})
    int_res = integration_response.json()
    if f'{integration}' in int_res:
        print(org_name)
