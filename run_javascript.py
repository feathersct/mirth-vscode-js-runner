import argparse
import sys
from mirthpy.mirthService import *
import requests
import json
import os.path
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(
                    prog='Mirth JavaScript Runner',
                    description='Deploys and runs messages through a mirth channel')

parser.add_argument('-i', '--instance', help="Mirth Instance", action="store", default="localhost")
parser.add_argument('-p', '--port', help="Mirth API Port", action="store", default=8443)
parser.add_argument('-usr', '--user', help="Mirth User", action="store", default="admin")
parser.add_argument('-pass', '--password', help="Mirth Password", action="store", default="admin")
parser.add_argument('-cid', '--channelid', help="Channel to Deploy and Send Message", action="store", default="1d50f722-f248-4c99-af97-b9a338480a90")
parser.add_argument('-msg', '--message_location', help="Test Message Location", action="store", default="E:\\Personal\\JavaScriptTutorial\\messages\\tet.txt")

args = parser.parse_args()

instance = args.instance
port = args.port
username = args.user
password = args.password
channel_id = args.channelid

# check if file actually exists
if os.path.isfile(args.message_location):
    with open(args.message_location, 'r') as file:
        message = file.read()
else:
    print(args.message_location + " does not exist. Exiting...")
    sys.exit(-1)

# initialize url for later use
url = f"https://{instance}:{port}/api"

# get the last server log, before running
x = requests.get(url + "/extensions/serverlog?fetchSize=1", auth=(username, password), verify=False, headers={"X-Requested-With": "OpenAPI", "Accept": "application/json"})
logs = json.loads(x.content)

lastLog = logs['list']['com.mirth.connect.plugins.serverlog.ServerLogItem']

if len(lastLog) > 0:
    lastLogId = lastLog['id']
else:
    lastLogId = None

# Deploy the channel
x = requests.post(url + f"/channels/{channel_id}/_deploy", auth=(username, password), verify=False, headers={"X-Requested-With": "OpenAPI"})

if x.status_code > 299:
    print("ERROR!!!! Deploy resulted in " + str(x.status_code) + " exiting...")
    sys.exit(-1)

# Send message into channel
x = requests.post(url + f"/channels/{channel_id}/messages", data=message, auth=(username, password), verify=False, headers={"X-Requested-With": "OpenAPI"})

if x.status_code > 299:
    print("ERROR!!!! Send Message resulted in " + str(x.status_code) + " exiting...")
    sys.exit(-1)

# Fetch all the logs generated from channel
x = requests.get(url + f"/extensions/serverlog?fetchSize=100&lastLogId={lastLogId}", auth=(username, password), verify=False, headers={"X-Requested-With": "OpenAPI", "Accept": "application/json"})
logs = json.loads(x.content)

# if not logs to show
if logs['list'] is None:
    print(f"No logs to show for {channel_id}")
    sys.exit(1)

# if multiple logs
if type(logs['list']['com.mirth.connect.plugins.serverlog.ServerLogItem']) == list:
    channelLogs = [log for log in logs['list']['com.mirth.connect.plugins.serverlog.ServerLogItem'] if channel_id in log['threadName']]

    if channelLogs is None:
        print(f"No logs to show for {channel_id}")
        sys.exit(1)

    for l in channelLogs:
        print(l['message'])
else:
    print(logs['list']['com.mirth.connect.plugins.serverlog.ServerLogItem']['message'])






