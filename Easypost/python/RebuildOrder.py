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

easypost.api_key = TESTKEY


######################################################################################
# import the shipment JSON. Simply copy and paste the JSON into shipment.json
######################################################################################

JSON = '/Users/madams/Desktop/conf/orders.json'
with open(JSON) as json_file:
    order = json.load(json_file)

######################################################################################
# create a logfile for the shipment
######################################################################################

LOGS = Path('/Users/madams/Desktop/LOGS/orders/'+str(order['public_id'])+'.txt')
LOGS.touch(exist_ok=True)
f = open(LOGS, "a")


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

order = easypost.Order.create(
    to_address=to_address,
    from_address=from_address,
    shipments=shipments
)

print(json.dumps(shipments, indent=4, sort_keys=True))

rates = order.get_rates()
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
    purchase = order.buy(carrier=carrier, service=service)
if buyoption == "2":
    quit()

print(purchase)