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

batchShipments = []

def readshipment():
    JSON = '/Users/madams/Desktop/conf/shipment.json'
    with open(JSON) as json_file:
        shipment = json.load(json_file)
    
    return shipment

def readbatch():
    JSON = '/Users/madams/Desktop/conf/batch.json'
    with open(JSON) as json_file:
        batch = json.load(json_file)
    
    return batch

def readorder():
    JSON = '/Users/madams/Desktop/conf/order.json'
    with open(JSON) as json_file:
        order = json.load(json_file)
    
    return order

def cleanShipment(shipment):
    print("Cleaning shipment: "+shipment["id"])
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
    return shipment

######################################################################################
    # Pre-request testing
######################################################################################
def testShipment(shipment):
    print("**********************************************************************")
    print(" testing Shipment: "+shipment["id"])
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
        if shipment["customs_info"] == None:
            print("WARNING; Internaitonal shipment does NOT contain customs_info")
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

def rebuildShipment(shipment):
    is_return = shipment["is_return"]
    print("Is_return = "+str(is_return))
    anyKey = input("Press any key to continue or quit now.")
    print("**********************************************************************")

    newShipment = easypost.Shipment.create(
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
            purchase = newShipment.buy(rate=shipment.lowest_rate(carriers=[originalCarrier], services=[originalService]))
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

    return newShipment

    ######################################################################################
    # RETRIEVE SHIPMENT 
    ######################################################################################

def buyShipment(shipment):
    ID = shipment["id"]
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
    #f.write("Label: " + str(purchase["postage_label"]["label_pdf_url"]+"\n"))
    f.write("Tracking: " + str(purchase["tracking_code"]+"\n"))

    f.close()
    #end of rebuildShipment

def testorder(order):
    commonRates = {}
    for shipment in order["shipments"]:
        ID = shipment["id"]
        commonRates[ID] = {}
        shipment = cleanShipment(shipment)
        shipment = testShipment(shipment)
        if shipment["rates"]:
            for rate in shipment["rates"]:
                rateid = rate["id"]
                commonRates[ID][rateid] = {}
                carrier = str(rate["carrier"])
                service = str(rate["service"])
                commonRates[ID][rateid]["carrier"] = carrier
                commonRates[ID][rateid]["service"] = service
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

def rebuildorder(order):
    from_address = easypost.Address.create(
        name = order["from_address"]["name"],
        street1 = order["from_address"]["street1"],
        street2 = order["from_address"]["street2"],
        city = order["from_address"]["city"],
        state = order["from_address"]["state"],
        zip = order["from_address"]["zip"],
        country = order["from_address"]["country"],
        phone = order["from_address"]["phone"],
        email = order["from_address"]["email"],
        verifications = order["from_address"]["verifications"]
    )

    to_address = easypost.Address.create(
        name = order["to_address"]["name"],
        street1 = order["to_address"]["street1"],
        street2 = order["to_address"]["street2"],
        city = order["to_address"]["city"],
        state = order["to_address"]["state"],
        zip = order["to_address"]["zip"],
        country = order["to_address"]["country"],
        phone = order["to_address"]["phone"],
        email = order["to_address"]["email"],
        verifications = order["to_address"]["verifications"]
    )

    shipments = []

    for shipment in order["shipments"]:

        parcel = {
            "parcel": {
                    "length": shipment["parcel"]["length"],
                    "width": shipment["parcel"]["width"],
                    "height": shipment["parcel"]["height"],
                    "weight": shipment["parcel"]["weight"]
            }}
        shipments.append(parcel)

    neworder = easypost.Order.create(
        to_address=to_address,
        from_address=from_address,
        shipments=shipments
    )

    rates = neworder.get_rates()
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

    buyoption = input("1)To purchase with carrier and service 2) to EXIT: ")
    if buyoption == "1":
        carrier = input("CARRIER: ")
        service = input("SERVICE: ")
        purchase = neworder.buy(carrier=carrier, service=service)
    if buyoption == "2":
        quit()

    print(purchase)

def testbatch(batch):
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

def rebuildbatch(batch):
    batch_id = batch["public_id"]
    batchShipments = {}
    LOGS = Path('/Users/madams/Desktop/LOGS/batches/'+batch_id+'.txt')
    LOGS.touch(exist_ok=True)
    f = open(LOGS, "a")
    
    for shipment in batch["batch_shipments"]:
        ID = shipment["id"]
        shipment = cleanShipment(shipment)
        shipment = testShipment
        shipment = rebuildShipment(shipment)
        batchShipment = {
        "id": ID
        }
        batchShipments.append(batchShipment)
    
    newBatch = easypost.Batch.create(shipments=batchShipments);
    return newBatch