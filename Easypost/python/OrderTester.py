
''' 
This script will parse the shipment objects within an order, look for known issues in the parcel and address fomration and 
finally attempt to recreate each shipment while logging rate_errors and messages. Ultimatly the script will return a list of 
rates COMMON to each shipment
'''

import easypost
import json
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
f = open(OUTPUT, "a")

easypost.api_key = TESTKEY

######################################################################################
# import the ORDER JSON. Simply copy and paste the JSON into shipment.json
######################################################################################

JSON = '/Users/madams/Desktop/conf/orders.json'
with open(JSON) as json_file:
    order = json.load(json_file)

######################################################################################
# Iterate through the shipments
######################################################################################

commonRates = {}

for shipment in order["shipments"]:
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

    '''verif = input("Would you like to asset address verifications Y/N:  ")
    if verif == "Y":
        shipment["from_address"]["verify"] = {"0": "delivery"},
        shipment["to_address"]["verify"] = {"0": "delivery"},'''

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

    is_return = "false"
    if shipment["is_return"] == "true":
        is_return = "true"
        print("shipment will be created as a RETURN")

    '''anyKey = input("Press any key to continue or quit now.")
    print("**********************************************************************")

    resp = easypost.Shipment.create(
        to_address = shipment["to_address"],
        from_address = shipment["from_address"],
        parcel = shipment["parcel"],
        customs_info = shipment["customs_info"],
        options = shipment["options"],
        is_return = is_return
    )

    ######################################################################################
    # RETRIEVE SHIPMENT 
    ######################################################################################

    ID = resp["id"]
    shipment = easypost.Shipment.retrieve(str(ID))
    '''

    ######################################################################################
    # GET RATES AND MESSAGES
    ######################################################################################
    #rates = shipment.get_rates()

    ID = shipment["id"]

    f.write("**********************************************************\n")
    f.write("Shipment: "+shipment["id"]+" \n")
    f.write("**********************************************************\n")

    f.write("**********************************************************\n")
    f.write("Rates\n")
    f.write("**********************************************************\n")

    commonRates[ID] = {}
    
    for rate in shipment["rates"]:
        rateid = rate["id"]
        commonRates[ID][rateid] = {}
        carrier = str(rate["carrier"])
        service = str(rate["service"])
        commonRates[ID][rateid]["carrier"] = carrier
        commonRates[ID][rateid]["service"] = service
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

commonRates = json.dumps(commonRates)
f.write(str(commonRates))