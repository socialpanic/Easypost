import easypost
easypost.api_key = ''

'''
Step 1: Creating a Batch of Shipments
A Batch is a collection of Shipments that you purchase and generate labels for together. When creating a Batch, you can either:

Create and purchase the Shipment objects ahead of time and pass Shipment IDs.
Pass us the information needed to create Address, Parcel, and Shipment objects as well as tell us which Carrier and Service you want to use for that Shipment.
When you create a Batch, the Shipments within the Batch are created asynchronously. When you first POST to create the Batch, we will send a webhook to your app 
that the Batch object is being created. ("state":"creating") It will take on average 1 minute to process 1,000 Shipments.

Once all are created, we will send another webhook to your application telling you it is complete ("state":"created"). If there are any errors for the Batch object, 
we will tell you about them in the webhook ("state":"creation_failed"). Step 2 of this tutorial will show you how to fix any errors that arise. There is more information 
on webhooks later in the tutorial.
'''

from_address = easypost.Address.create(
  {
    "name": '',
    "street1": '',
    "city": '',
    "state": '',
    "zip": '',
    "country": '',
    "phone": '',
    "email": ''
  }
)
parcel = easypost.Parcel.create(
  {
    "length": 20.2,
    "width": 10.9,
    "height": 5,
    "weight": 65.9
    } 
)

batch = easypost.Batch.create(shipment = [
  {
    'from_address': from_address,
    'to_address': {
      'name': 'Stan Marsh',
      'street1': '706 Main St',
      'city': 'Fairplay',
      'state': 'CO',
      'zip': '80440'
    },
    'parcel': parcel,
    'carrier': 'USPS',
    'service': 'Priority',
  },
  {
    'from_address': from_address,
    'to_address': {
      'name': 'Kenny McCormick',
      'street1': '640 Hathaway St',
      'city': 'Fairplay',
      'state': 'CO',
      'zip': '80440'
    },
    'parcel': parcel,
    'carrier': 'USPS',
    'service': 'Priority',
  },
  {
    'from_address': from_address,
    'to_address': {
      'name': 'Eric Cartman',
      'street1': '575 5th St',
      'city': 'Fairplay',
      'state': 'CO',
      'zip': '80440'
    },
    'parcel': parcel,
    'carrier': 'USPS',
    'service': 'Priority',
  },
  {
    'from_address': from_address,
    'to_address': {
      'name': 'Kyle Broflovski',
      'street1': '517 Hathaway St',
      'city': 'Fairplay',
      'state': 'CO',
      'zip': '80440'
    },
    'parcel': parcel,
    'carrier': 'USPS',
    'service': 'Priority',
  }
]);

'''
# retrieve a batch from an ID and add shipments via ID
batch = easypost.Batch.retrieve('{BATCH_ID}')
batch.add_shipments(shipments=[
  {'id': '{SHIPMENT_ID}'},
  {'id': '{SHIPMENT_ID}'}
])
'''

'''
The next step is to purchase and create all labels for the shipments in your batch. All you need to do is issue a buy on the particular Batch object you’re 
ready to buy. When you buy the batch, we kick off an asynchronous process to create all the labels you need.

The initial response from buying a Batch will not have the URL of a label. Because we support up to 10,000 shipments in a Batch, it takes a little time to 
create all the labels. For 100 labels, it takes about 1 minute.

Once we’ve purchased and created all the labels for a batch, we’ll send a webhook to your application letting you know that it has completed. When completed, 
the “state” of the Batch object will be “purchased”. If there are any errors, the state of the Batch object will be "purchase_failed". You will need to fix or 
remove any of the shipments that failed before proceeding to the next step of creating the Batch Label.

Here's a code example of buying a Batch:
'''
#batch.buy();

'''
Step 4: Creating a Batch Label
Once you have received the webhook that your Batch has been purchased, the final step is to create and retrieve all the shipping labels in a single Batch Label. 
All the labels for the Batch will be in a single file that you download. A Batch Label can be retrieved in either PDF, EPL2, or ZPL format.
'''
#batch.label(file_format = 'pdf')

'''
Step 5: Using Webhooks for a Batch
When using Batches, webhooks are useful at three points:

Creating a Batch (Step 1 in the tutorial)
Purchasing and creating labels for a Batch (Step 3 in the tutorial)
Creating and retrieving a Batch label (Step 4 in the tutorial)
Webhooks are required because these processes are completed asynchronously. You will receive a webhook both on the initial POST to EasyPost and once the given 
action has reached a final state. If there are any errors, we will pass them back in the webhook.

When evaluating Events that hit your webhook URL, you’ll know it is a Batch event because the object “type” is “Event” and the "description" is “batch.created” 
or "batch.updated". As part of this Event, we will also pass you back the Batch object. The value of the Event’s "result" attribute will contain the Batch object.

We recommend you evaluate the “state” of the Batch object to check if your Batch was successfully processed. If there is an error (eg “creation failed” or 
“purchase_failed” ), you can then inspect the individual Shipment objects we return to see which one caused the issue. Each Shipment will have a “batch_status” 
that will let you know which Shipment needs to be fixed. We also provide a summary of successes and failure so you know how many Shipments need attention.
'''

