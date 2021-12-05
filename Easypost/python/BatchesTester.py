import re
import easypost
import json
from pathlib import Path

easypost.api_key = TESTKEY

######################################################################################
# import the batch JSON. Simply copy and paste the JSON into batch.json
######################################################################################

JSON = '/a/directory/containing/batch.json'
with open(JSON) as json_file:
    batch = json.load(json_file)

######################################################################################
# create a logfile for the shipment
######################################################################################
batch_id = batch["public_id"]

LOGS = Path('/a/directory/for/dumping/batch/logs/'+batch_id+'.txt')
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
