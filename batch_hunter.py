import easypost
import json
from pathlib import Path

######################################################################################
# Script for troubleshooting vague DHLEcs errors regarding previously manifested shipments.
# 1.) Copy and paste the json from the problem batch into one text file
# 2.) Using admin console and the format below to compile an array of previously manifested batches
# 3.) Configure the script to pull in batches from these files(lines:27 and 31) and configure your LOG file (line: 35)
# 4.) Run the script
######################################################################################

# Use the format below to setup your batch objects in the batch1 file
'''
[
  {batch JSON 1},
  {batch JSON 2},
  {batch JSON 3},
  {batch JSON 4}
]
'''

######################################################################################
# import the batch JSON
######################################################################################

batch1 = 'PATH TO FILE'                     #This is the file that you will dump batch JSON into. Use Schema on line 13 to setup file
with open(batch1) as json_file:
    old_batches = json.load(json_file)

batch2 = 'PATH TO FILE'                     #Use this file to dump the JSON from the batch getting errros
with open(batch2) as json_file:
    current_batch = json.load(json_file)

LOGS = Path('PATH\TO\DIRECTORY\'+str(current_batch['public_id'])+'.txt')        #This is file is where the script dumps its report if it finds anything
LOGS.touch(exist_ok=True)
f = open(LOGS, "a")

######################################################################################
# create a logfile for the shipment
######################################################################################

bad_batch = []
past_batches = []

#Pull in shipping IDs from the the batch that is recieving errors
for shipment in current_batch["batch_shipments"]:
    id = shipment["shipment_public_id"]
    bad_batch.append(id)

#iterate over the shipping IDs in previous batches to see if we get a match
#for batch in old_batches:

for batt in old_batches:
  batch_ID = batt["public_id"]
  for shipment in batt["batch_shipments"]:
    id = shipment["shipment_public_id"]
    past_batches.append(id)
  
  results = set(bad_batch).intersection(past_batches)

  if results == None:
    print("No Conflicts Found")

  count = 0
  f.write("#########################################################################\n")
  f.write(batch_ID+"\n")
  f.write("#########################################################################\n")
  for ship in results:
    #print("FOUND: " + ship)
    f.write(ship+"\n")
    count +=1

  print(str(count) +" shipments found in "+str(batch_ID))
