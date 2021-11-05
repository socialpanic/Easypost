require('babel-polyfill');
const EasyPost = require('@easypost/api');

const api = new EasyPost('');

const shipment = new api.Shipment({
  to_address: {
    name: 'Dr. Steve Brule',
    street1: '179 N Harbor Dr',
    city: 'Redondo Beach',
    state: 'CA',
    zip: '90277',
    country: 'US',
    phone: '4155559999',
  },
  from_address: {
    street1: '417 MONTGOMERY ST',
    street2: 'FLOOR 5',
    city: 'SAN FRANCISCO',
    state: 'CA',
    zip: '94104',
    country: 'US',
    company: 'EasyPost',
    phone: '415-123-4567',
  },
  parcel: {
    length: 8,
    width: 5,
    height: 5,
    weight: 5
  },
  customs_info: {
    eel_pfc: 'NOEEI 30.37(a)',
    customs_certify: true,
    customs_signer: 'Steve Brule',
    contents_type: 'merchandise',
    contents_explanation: '',
    restriction_type: 'none',
    restriction_comments: '',
    non_delivery_option: 'abandon',
    declaration: 'Here is a bunch of information...',

    customs_items: [
      new api.CustomsItem({
        'description': 'Sweet shirts 1',
        'quantity': 2,
        'weight': 11,
        'value': 23,
        'hs_tariff_number': '654321',
        'origin_country': 'US',
        'code': '123'
      }),
    ]
  }
});

shipment.save().then(s => s.buy(shipment.lowestRate()).then(console.log).catch(console.log))
