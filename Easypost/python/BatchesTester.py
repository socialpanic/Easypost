import re
import easypost
import json
from pathlib import Path

#this block of code reads API key from a textfile. Either alter your file structure accordingly or define it statically
try:
    with open('/Users/madams/Desktop/conf/conf.txt') as f:
        TESTKEY = str.splitlines(f.readline())
        USERID = str.splitlines(f.readline())
        PRODKEY = str.splitlines(f.readline())
        f.close()
        TESTKEY=TESTKEY[0]
        USERID=USERID[0]
        PRODKEY = PRODKEY[0]
except:
    print('failed to parse conf file for values')

OUTPUT = '/Users/madams/Desktop/CODE/EasyPost/python/output.txt'

easypost.api_key = TESTKEY

f = open(OUTPUT, "a")

######################################################################################
# import the batch JSON. Simply copy and paste the JSON into batch.json
######################################################################################

JSON = '/Users/madams/Desktop/conf/batch.json'
with open(JSON) as json_file:
    batch = json.load(json_file)

######################################################################################
# create a logfile for the shipment
######################################################################################
batch_id = batch["public_id"]

LOGS = Path('/Users/madams/Desktop/LOGS/batches/'+batch_id+'.txt')
LOGS.touch(exist_ok=True)
f = open(LOGS, "a")

user_id = batch["user"]["public_id"]
scanf_id = batch["scan_form"]["id"]
scanf_status = batch["scan_form"]["status"]
scanf_msg = batch["scan_form"]["message"]

if scanf_msg == "Unable to create a ScanForm from shipments bought from this carrier.":
    print(scanf_msg)
    print("Attempting to generate scanform by ID")
    batch.create_scan_form();
    user_id = batch["user"]["public_id"]
    scanf_id = batch["scan_form"]["id"]
    scanf_status = batch["scan_form"]["status"]
    scanf_msg = batch["scan_form"]["message"]
    print("============SCANFORM==============")
    print(batch["scan_form"])



print("===========================================")
f.write("=========================================\n")
print("Public_id: "+ batch_id)
f.write("Public_id: "+ batch_id+"\n")
print("User: "+ user_id)
f.write("User: "+ user_id+"\n")
print("Scanform: "+ scanf_id)
f.write("Scanform: "+ scanf_id+"\n")
print("Status: "+ scanf_status)
f.write("Status: "+ scanf_status+"\n")
print("Msgs: "+ scanf_msg)
f.write("Msgs: "+ scanf_msg+"\n")
print("===========================================")
f.write("=========================================\n")

print("Number of Shipments: "+ str(batch["num_shipments"]))
f.write("Number of Shipments: "+ str(batch["num_shipments"])+"\n")
print("Number Purchased: "+ str(batch["status"]["postage_purchased"]))
f.write("Number Purchased: "+ str(batch["status"]["postage_purchased"])+"\n")


for shipment in batch["batch_shipments"]:
    print("Shipment: "+ shipment["shipment_public_id"])
    f.write("Shipment: "+ shipment["shipment_public_id"]+"\n")
    print("Status: "+ shipment["status"])
    f.write("Status: "+ shipment["status"]+"\n")
    print("URL: https://easypost-admin.easypo.net/easy_post~shipment/"+ shipment["shipment_public_id"])
    f.write("URL: https://easypost-admin.easypo.net/easy_post~shipment/"+ shipment["shipment_public_id"]+"\n")
    print("===========================================")
    f.write("=========================================\n")


f.close()
