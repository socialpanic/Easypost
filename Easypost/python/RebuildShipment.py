import easypost
import json
from pathlib import Path

easypost.api_key = <API KEY>

######################################################################################
# import the shipment JSON. Simply copy and paste the JSON into shipment.json
######################################################################################

JSON = '/a/path/to/shipment.json'
with open(JSON) as json_file:
    shipment = json.load(json_file)

######################################################################################
# create a logfile for the shipment
######################################################################################

LOGS = Path('a/path/for/dumping/logs/'+str(shipment['id'])+'.txt')
LOGS.touch(exist_ok=True)
f = open(LOGS, "a")

######################################################################################
# Clean up order JSON
######################################################################################

shipment["to_address"].pop("id")
shipment["to_address"].pop("mode")
shipment["to_address"].pop("updated_at")
shipment["to_address"].pop("created_at")
shipment["to_address"].pop("carrier_facility")
shipment["from_address"].pop("id")
shipment["from_address"].pop("created_at")
shipment["from_address"].pop("mode")
shipment["from_address"].pop("updated_at")
shipment["parcel"].pop("id")
shipment["parcel"].pop("created_at")
shipment["parcel"].pop("mode")
shipment["parcel"].pop("updated_at")

customs_weight = 0
customs = 'false'
if shipment["customs_info"]:
    customs = 'true'
    shipment["customs_info"].pop("id")
    shipment["customs_info"].pop("created_at")
    #shipment["customs_info"].pop("mode")
    shipment["customs_info"].pop("updated_at")
    for item in shipment["customs_info"]["customs_items"]:
        customs_weight += item["weight"]
        item.pop("id")
        item.pop("created_at")
        item.pop("mode")
        item.pop("updated_at")
        if item["currency"] == 'None':
            item.pop("currency")

if shipment["tracker"]:
  tracker = shipment["tracker"]["public_url"]
  print(tracker)

######################################################################################
# Pre-request testing
######################################################################################

print("**********************************************************************")
print(" PRE-POST TESTS ")
print("**********************************************************************")

from_verif = 'true'
to_verif = 'true'

#Address Verifications
if shipment["from_address"]["verifications"] == {}:
  print("from_address unverified")
  f.write("from_address unverified\n")
  from_verif = 'false'

if shipment["to_address"]["verifications"] == {}:
  print("to_address unverified")
  to_verif = 'false'

verif = input("Would you like to asset address verifications Y/N:  ")
if verif == "Y":
  shipment["from_address"]["verify"] = {"0": "delivery"},
  shipment["to_address"]["verify"] = {"0": "delivery"},

#Is order domestic or international
domestic = "true"
if shipment["from_address"]["country"] == shipment["to_address"]["country"]:
  print("Shipment is a domestic "+shipment["to_address"]["country"]+" shipment")
  print("**********************************************************************")
else:
  print("Shipment appears to be international: "+ shipment["from_address"]["country"] +" to "+ shipment["to_address"]["country"])
  domestic = "false"
  
  #does the international order contain customs_info?
  if customs =="false":
    print("WARNING; Internaitonal shipment does NOT contain customs_info")
    print("**********************************************************************")
  
  #check the weight of the parcel and customs items
  if customs == "true":
    if shipment["parcel"]["weight"] < customs_weight or shipment["parcel"]["weight"] == customs_weight:
      print("WARNING: Total weight of customs_items ("+ str(customs_weight) +") out weigh the Parcel ("+str(shipment["parcel"]["weight"])+")")
      print("**********************************************************************")

#Parcel check
#set up the params to zero just incase the order leaves them blank in favor of a predefined package
height = 0
length = 0
width = 0
weight = 0
girth = 0

if shipment["parcel"]["height"]:
  height = shipment["parcel"]["height"]

if shipment["parcel"]["length"]:
  length = shipment["parcel"]["length"]

if shipment["parcel"]["width"]:
  width = shipment["parcel"]["width"]

if shipment["parcel"]["weight"]:
  weight = shipment["parcel"]["weight"]

girth = (length * 2) + (height * 2)

#USPS TESTING

if weight > 1120 and domestic == "true":
  print("WARNING: parcel weight of "+str(weight)+"onces exceeds the 70-pound threashold for most domestic USPS shipments")

#USPS DIM WEIGHT TEST - The dim weight formulas assume that USPS divide parcel volume by 166 and other carriers by 139 (https://www.stamps.com/usps/dimensional-weight/)
cubic_foot = length * width * height
if cubic_foot > 1728:
  pounds = weight / 16
  print("******************************************WARNING**************************************")
  print("parcel is OVER one cubic foot and Dimensional Weight USPS may be dim weighted at "+str(cubic_foot / 166)+"lbs instead of " +str(pounds)+ " pounds.")
  print("Other carriers may be dim weigh the parcel at "+str(cubic_foot / 139)+"lbs instead of " +str(pounds)+ " pounds.")
  print("Consult the following link for details: "+"https://www.fitshipper.com/freeTools/dimensional-weight-calculator.html?x="+str(length)+"&y="+str(width)+"&z="+str(height)+"&weight="+str(pounds)+"&method="+shipment["selected_rate"]["service"])
  
  #prompt user to change parcel weight based on dim weight findings
  alter_weight = input(">>> DO YOU WANT TO ALTER THE PARCEL WEIGHT Y/N?")
  if alter_weight =="Y":
    new_weight = input(">>> ENTER NEW PARCEL WEIGHT (IN POUNDS): ")
    new_weight = int(new_weight)
    shipment["parcel"]["weight"] = new_weight*16

    print("PARCEL WEIGHT HAS BEEN CHANGED TO: "+str(shipment["parcel"]["weight"])+" ounces")
  print("****************************************************************************************")

#UPS TESTING

if weight > 2400:
  print("WARNING: parcel weight of "+str(weight)+"onces exceeds the 150-pound threashold for UPS shipments")

if length > 108:
  print("WARNING: parcel length of "+str(length)+" inches exceeds the 108-inch threashold for UPS shipments")

if girth > 165:
  print("WARNING: parcel girth of "+str(girth)+" inches exceeds the 165-inch threashold for UPS shipments")

######################################################################################
# FORM shipping request
######################################################################################

is_return = shipment["is_return"]
print("Is_return = "+str(is_return))
anyKey = input("Press any key to continue or quit now.")
print("**********************************************************************")

resp = easypost.Shipment.create(
  to_address = shipment["to_address"],
  from_address = shipment["from_address"],
  parcel = shipment["parcel"],
  customs_info = shipment["customs_info"],
  options = shipment["options"],
  is_return = is_return
)

if shipment["selected_rate"]:
  originalService = shipment["selected_rate"]["service"]
  originalCarrier = shipment["selected_rate"]["carrier"]
  print("Original Shipment contains a selected rate consisting of carrier: "+originalCarrier+" and service "+originalService)
  rebuy = input("Do you want to purchase a rate based off this carrier and service Y/N.")
  if rebuy == "Y":
    D = resp["id"]
    shipment = easypost.Shipment.retrieve(str(ID))
    purchase = shipment.buy(rate=shipment.lowest_rate(carriers=[originalCarrier], services=[originalService]))
    f.write("**********************************************************\n")
    f.write("Label\n")
    f.write("**********************************************************\n")
    f.write("Selected Rate: " + str(purchase["selected_rate"]["id"]+"\n"))
    f.write("Carrier: " + str(purchase["selected_rate"]["carrier"]+"\n"))
    f.write("Service: " + str(purchase["selected_rate"]["service"]+"\n"))
    f.write("Rate: " + str(purchase["selected_rate"]["rate"]+"\n"))
    f.write("Label: " + str(purchase["postage_label"]["label_pdf_url"]+"\n"))
    f.write("Tracking: " + str(purchase["tracking_code"]+"\n"))
    quit()

######################################################################################
# RETRIEVE SHIPMENT 
######################################################################################

ID = resp["id"]
shipment = easypost.Shipment.retrieve(str(ID))

######################################################################################
# GET RATES AND MESSAGES
######################################################################################
rates = shipment.get_rates()

f.write("**********************************************************\n")
f.write("Shipping Object\n")
f.write("**********************************************************\n")
f.write(str(shipment))

f.write("**********************************************************\n")
f.write("Rates\n")
f.write("**********************************************************\n")

for rate in rates["rates"]:
    print("ID: " + str(rate["id"]))
    f.write("ID: " + str(rate["id"]+"\n"))
    print("CARRIER: " + str(rate["carrier"]))
    f.write("CARRIER: " + str(rate["carrier"]+"\n"))
    print("SERVICE: " + str(rate["service"]))
    f.write("SERVICE: " + str(rate["service"]+"\n"))
    print("RATE: " + str(rate["rate"]))
    f.write("RATE: " + str(rate["rate"]+"\n"))
    print("******************************************")
    f.write("******************************************\n")
f.write("**********************************************************\n")
f.write("Messages\n")
f.write("**********************************************************\n")

if shipment["messages"]:
  for msg in shipment["messages"]:
    print("CARRIER: " + str(msg["carrier"]))
    f.write("CARRIER: " + str(msg["carrier"]+"\n"))
    print("SERVICE: " + str(msg["message"]))
    f.write("SERVICE: " + str(msg["message"]+"\n"))
    print("******************************************")
    f.write("******************************************\n")

#Address Verification Report

'''if shipment["to_address"]["verifications"]:
  print(shipment["to_address"]["verifications"]["success"])
  if shipment["to_address"]["verifications"]["errors"]:
    print(shipment["to_address"]["verifications"]["errors"])'''
    

######################################################################################
# REFUND ELEGIBILITY
######################################################################################


######################################################################################
# PURCHASE LABEL
######################################################################################

print("Admin URL: https://easypost-admin.easypo.net/easy_post~shipment/"+str(ID))

buyoption = input("1) To purchase cheapest rate, 2) to purchase by rate ID 3) to purchase with carrier and service 4) to EXIT: ")
if buyoption == "1":
    purchase = shipment.buy(rate=shipment.lowest_rate())
if buyoption == "2":
    rateid = input("Enter rate_id: ")
    purchase = shipment.buy(rate={'id': str(rateid)})
if buyoption == "3":
    carrier = input("CARRIER: ")
    service = input("SERVICE: ")
    purchase = shipment.buy(rate=shipment.lowest_rate(carriers=[carrier], services=[service]))
if buyoption == "4":
    quit()

######################################################################################
# Dump responce into output file for future reference
######################################################################################

f.write("**********************************************************\n")
f.write("Label\n")
f.write("**********************************************************\n")
f.write("Selected Rate: " + str(purchase["selected_rate"]["id"]+"\n"))
f.write("Carrier: " + str(purchase["selected_rate"]["carrier"]+"\n"))
f.write("Service: " + str(purchase["selected_rate"]["service"]+"\n"))
f.write("Rate: " + str(purchase["selected_rate"]["rate"]+"\n"))
f.write("Label: " + str(purchase["postage_label"]["label_pdf_url"]+"\n"))
f.write("Tracking: " + str(purchase["tracking_code"]+"\n"))

f.close()
