import easypost
easypost.api_key = ''

#This script is used to generate shipments for merging into batches or orders later

shipment = easypost.Shipment.create(
  to_address={
    "name": '',
    "street1": '',
    "city": '',
    "state": '',
    "zip": '',
    "country": '',
    "phone": '',
    "email": ''
  },
  from_address={
    "name": '',
    "street1": '',
    "street2": '',
    "city": '',
    "state": '',
    "zip": '',
    "country": '',
    "phone": '',
    "email": ''
  },
  parcel={
    "length": 20.2,
    "width": 10.9,
    "height": 5,
    "weight": 65.9
  },
)


shipment = easypost.Shipment.retrieve("shp_...")
shipment.get_rates()