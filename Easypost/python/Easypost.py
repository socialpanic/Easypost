import easypost

try:
    with open('/home/devbox/Desktop/conf/conf.txt') as f:
        TESTKEY = str.splitlines(f.readline())
        PRODKEY = str.splitlines(f.readline())
        f.close()
        TESTKEY=TESTKEY[0]
        PRODJEY = PRODKEY[0]
except:
    print('failed to parse conf file for values')

OUTPUT = '/Users/madams/Desktop/CODE/EasyPost/python/output.txt'

easypost.api_key = TESTKEY

'''
Addresses
Address objects are used to represent people, places, and organizations in a number of contexts. For example, a Shipment requires a to_address and from_address to accurately calculate rates and generate postage.

Additionally, EasyPost offers several verification tools that can be used to detect deliverability issues, correct minor errors in spelling/formatting, and determine if an Address is residential or not (which has a significant effect on Shipment rating for many carriers).

Address Object
attribute	            type	                    specification
id	                    string	                    Unique identifier, begins with "adr_"
object	                string	                    "Address"
mode	                string	                    Set based on which api-key you used, either "test" or "production"
street1	                string	                    First line of the address
street2	                string	                    Second line of the address
city	                string	                    City the address is located in
state	                string	                    State or province the address is located in
zip	                    string	                    ZIP or postal code the address is located in
country	                string	                    ISO 3166 country code for the country the address is located in
residential	            boolean	                    Whether or not this address would be considered residential
carrier_facility	    string	                    The specific designation for the address (only relevant if the address is a carrier facility)
name	                string	                    Name of the person. Both name and company can be included
company 	            string	                    Name of the organization. Both name and company can be included
phone	                string	                    Phone number to reach the person or organization
email	                string	                    Email to reach the person or organization
federal_tax_id	        string	                    Federal tax identifier of the person or organization
state_tax_id	        string	                    State tax identifier of the person or organization
verifications	        Verifications	            The result of any verifications requested

Verifications Object
attribute	            type	                    specification
zip4	                Verification	            Only applicable to US addresses - checks and sets the ZIP+4
delivery	            Verification	            Checks that the address is deliverable and makes minor corrections to spelling/format. US addresses will also have
                                                    their "residential" status checked and set.
Verification Object
attribute	            type	                    specification
success	                boolean	                    The success of the verification
errors	                FieldError array	        All errors that caused the verification to fail
details	                VerificationDetails	        Extra data related to the verification

VerificationDetails Object
attribute	            type	                    specification
latitude	            number	                    The latitude
longitude	            number	                    The longitude
time_zone	            TZ(string)	                The time zone the address is located in, IE: America/Los_Angeles

Address Verification by Country
Our address verification service supports 240+ countries. See our full listing to see which verification level is available for each country. We are constantly working to expand our coverage of addresses worldwide.

https://www.easypost.com/docs/address-verification-by-country

Create and Verify Addresses

Depending on your use case an Address can be used in many different ways. Certain carriers allow rating between two zip codes, but full addresses are required to purchase postage. It is recommended to provide as much information as possible during creation and to reuse these objects whenever possible.

Address objects can also be created inline while creating another object, for example during Shipment Creation.

Verify an Address

Verifying an Address before you ship is a great way to reduce issues with delivery.

Creating a verified Address is as simple as including an enumerated list of the verifications you'd like EasyPost to perform in the verify or verify_strict url parameters. If any of the verification checks included in the verify_strict list fail an error will be returned from the API. The example below demonstrates the most common verification: "delivery", which checks that the address is deliverable and sets its residential delivery indicator.

The most effective time to perform address verification is when your customer, or the person entering the delivery address, is present. When designing a shopping cart it is recommended to ask the shopper for their address and verify it on the spot. If verification fails, ask them to double check their input; if they confirm that their data is correct, assume they know their address more correctly than the verification process.

Create Address Request Parameters

param	                example	                            info
street1	            417 Montgomery St	                    First line of the address
street2	            Floor 5	                                Second line of the address
city	            San Francisco	                        Full city name
state	            CA	                                    State or province
zip	                94104	                                ZIP or postal code
country	            US	                                    ISO 3166 country code for the country the address is located in
name	            Hiro Protagonist	                    Name of attention, if person. Both name and company can be included
company	            EasyPost	                            Name of attention, if organization. Both name and company can be included
phone	            415-123-4567	                        Phone number to reach the person or organization
email	            example@example.com	                    Email to reach the person or organization
residential	        false	                                Residential delivery indicator
carrier_facility	ONDC	                                The specific designation for the address (only relevant if the address is a carrier facility)
federal_tax_id	    1234567890	                            Federal tax identifier of the person or organization
state_tax_id	    9876543210	                            State tax identifier of the person or organization
verify	            [delivery, zip4, true]	                The verifications to perform when creating. verify_strict takes precedence. true will perform both delivery 
                                                            and zip4.
verify_strict	    [delivery, zip4, true]	                The verifications to perform when creating. The failure of any of these verifications causes the whole 
                                                            request to fail. true will perform both delivery and zip4



'''
# create address
address = easypost.Address.create(
    #verify=["delivery"],           # Will check for errors in the address
    #verify_strict=["delivery"],    # Will return those errors and refuse to process the shipment
    street1="",
    street2="",
    city="",
    state="",
    zip="",
    country="",
    company="",
    phone=""
)

from_address = easypost.Address.create(
    #verify=["delivery"],           # Will check for errors in the address
    #verify_strict=["delivery"],    # Will return those errors and refuse to process the shipment
    street1="",
    street2="",
    city="",
    state="",
    zip="",
    country="",
    company="",
    phone=""
)

to_address = easypost.Address.create(
    #verify=["delivery"],           # Will check for errors in the address
    #verify_strict=["delivery"],    # Will return those errors and refuse to process the shipment
    street1="",
    street2="",
    city="",
    state="",
    zip="",
    country="",
    company="",
    phone=""
)

# look up address by ID
#address = easypost.Address.retrieve("adr_...")

'''
Parcels
Parcel objects represent the physical container being shipped. Dimensions can be supplied either as length, width, and height dimensions, or a predefined_package string. Only weight is required, but since many carriers charge different rates for packages with large dimensions, we strongly recommend including all dimensions if available.

Weights are in OUNCES (OZ) and go to one decimal point.
Dimensions are in INCHES (IN) and go to one decimal point.

Parcel Object
attribute	                        type	                            specification
id	                                string	                            Unique, begins with "prcl_"
object	                            string	                            "Parcel"
mode	                            string	                            "test" or "production"
length	                            float (inches)	                    Required if width and/or height are present
width	                            float (inches)	                    Required if length and/or height are present
height	                            float (inches)	                    Required if length and/or width are present
predefined_package	                string	                            Optional, one of our predefined_packages
weight	                            float (oz)	                        Always required
created_at	                        datetime	
updated_at	                        datetime	

Predefined Packages
If you provide a predefined_package the associated Shipment will fetch rates from carriers for which that is a valid predefined_package. Some carriers share predefined_package names. If you wish to restrict your rating to a specific carrier, we recommend passing the carrier_accounts field when creating a Shipment.

For most predefined_packages it is not necessary to specify parcel dimensions, only weight.

https://www.easypost.com/usps-rate-chart
https://www.easypost.com/usps-package-restrictions
'''

#Creates a parcel
parcel = easypost.Parcel.create(
  length=20.2,
  width=10.9,
  height=5,
  weight=65.9
)

'''
Retrieve a Parcel
Get a Parcel by its id. In general you should not need to use this in your automated solution. A Parcel's id can be inlined into the creation call to other objects. This allows you to only create one Parcel for each package you will be using.
'''

#Retrieve a parcel by ID
parcel = easypost.Parcel.retrieve("prcl_...")

'''
Insurances
An Insurance object represents insurance for packages purchased both via the EasyPost API as well as shipments purchased through third parties and later registered with EasyPost. An Insurance is created automatically whenever you buy a Shipment through EasyPost and pass insurance options during the Buy call or in a later call to Insure a Shipment.

Insurance purchased through the Shipment Buy or Insure endpoints is immediately insured - there is no possibility of rejection based on tracking information, as the package was just created. On the other hand, Insurance purchased on shipments purchased outside of EasyPost requires creation with a tracking code so that EasyPost may confirm the package existence and current shipping status at the time of purchase.

Standalone insurance is created in a pending state to help distinguish it from insurance purchased for an EasyPost Shipment. Both kinds of Insurance use the Tracking system to receive periodic updates, and will report those updates to any appropriate Webhooks on file. Standalone insurance will cancel itself if the tracking information for the given tracking code shows evidence of having been shipped anytime before the insurance was purchased.

Unlike Shipments within EasyPost, Insurance objects register To and From Address objects according to the destination and ship-from locations of the package. This means that a Shipment with "is_return: true" actually ships to the listed From Address. Insurance does not have a concept of "is_return", so all insurance records refer to their true package destination as "to_address", regardless of whether or not the shipment is a return.

Insurance Object
attribute	                            type	                        specification
id	                                    string	                        Unique identifier, begins with "ins_"
object	                                string	                        "Insurance"
mode	                                string	                        "test" or "production"
reference	                            string	                        The unique reference for this Insurance, if any
amount	                                string	                        USD value of insured goods with sub-cent precision
provider	                            string	                        The insurance provider used by EasyPost
provider_id	                            string	                        An identifying number for some insurance providers used by EasyPost
shipment_id	                            string	                        The ID of the Shipment in EasyPost, if postage was purchased via EasyPost
tracking_code	                        string	                        The tracking code of either the shipment within EasyPost, or provided by you during creation
status	                                string	                        The current status of the insurance, possible values are "new", "pending", "purchased", 
                                                                        "failed", or "cancelled"
tracker	                                Tracker	                        The associated Tracker object
to_address	                            Address	                        The associated Address object for destination
from_address	                        Address	                        The associated Address object for origin
fee	                                    Fee	                            The associated InsuranceFee object if any
messages	                            Array of strings	            The list of errors encountered during attempted purchase of the insurance
created_at	                            datetime	
updated_at	                            datetime	

Create an Insurance
An Insurance created via this endpoint must belong to a shipment purchased outside of EasyPost. Insurance for Shipments created within EasyPost must be created via the Shipment Buy or Insure endpoints. When creating Insurance for a non-EasyPost shipment, you must provide to_address, from_address, tracking_code, and amount information. Optionally, you can provide the carrier parameter, which will help EasyPost identify the carrier the package was shipped with. If no carrier is provided, EasyPost will attempt to determine the carrier based on the tracking_code provided. Providing a carrier parameter is recommended, since some tracking_codes are ambiguous and may match with more than one carrier. In addition, not having to auto-match the carrier will significantly speed up the response time.

Create Insurance Request Parameters
param	                                example	                        info
to_address	                            Address	                        The actual destination of the package to be insured
from_address	                        Address	                        The actual origin of the package to be insured
tracking_code	                        9400110898825022579493	        The tracking code associated with the non-EasyPost-purchased package you'd like to insure
reference	                            external-order-493	            Optional. A unique value that may be used in place of ID when doing Retrieve calls for this 
                                                                        insurance
amount	                                "$100.00"	                    The USD value of contents you would like to insure. Currently the maximum is $5000
carrier	                                USPS	                        The carrier associated with the tracking_code you provided. The carrier will get auto-detected 
                                                                        if none is provided

'''

#Create an insurance
insurance = easypost.Insurance.create(
    to_address=to_address,
    from_address=from_address,
    tracking_code="",
    carrier="",
    amount="",
    reference=""
)

'''
Retrieve a list of Insurances
The Insurance List is a paginated list of all Insurance objects associated with the given API Key. It accepts a variety of parameters which can be used to modify the scope. The has_more attribute indicates whether or not additional pages can be requested. The recommended way of paginating is to use either the before_id or after_id parameter to specify where the next page begins.

Retrieve a list of Insurances Request Parameters
param	                                example	                        info
before_id	                            ins_...	                    Optional pagination parameter. Only records created before the given ID will be included. May not 
                                                                    be used with after_id
after_id	                            ins_...	                    Optional pagination parameter. Only records created after the given ID will be included. May not be 
                                                                    used with before_id
start_datetime	                        2016-01-02T00:00:00Z	    Only return records created after this timestamp. Defaults to 1 month ago, or 1 month before a 
                                                                    passed end_datetime
end_datetime	                        2016-01-02T00:00:00Z	    Only return records created before this timestamp. Defaults to end of the current day, or 1 month
                                                                    after a passed start_datetime
page_size	                            30	                        The number of records to return on each page. The maximum value is 100, and default is 20.

'''
#Retrieve a list of insurances
insurances = easypost.Insurance.all(
    page_size = 2,
    start_datetime = "2016-01-02T08:50:00Z"
)

#Get insurance by ID
insurance = easypost.Insurance.retrieve("ins_...")

'''
Shipments
The workhorse of the EasyPost API, a Shipment is made up of a "to" and "from" Address, the Parcel being shipped, and any customs forms required for international deliveries. Once created a Shipment object is used to retrieve shipping Rates and purchase a label.

A Shipment created with a valid to_address, from_address, and parcel will automatically populate its rates attribute.

Note: USPS Commercial Plus Prices will show up in both the Production and Test API.

Shipment Object
attribute	                        type	                        specification
id	                                string	                        Unique, begins with "shp_"
object	                            string	                        "Shipment"
reference	                        string	                        An optional field that may be used in place of id in other API endpoints
mode	                            string	                        "test" or "production"
to_address	                        Address	                        The destination address
from_address	                    Address	                        The origin address
return_address	                    Address	                        The shipper's address, defaults to from_address
buyer_address	                    Address	                        The buyer's address, defaults to to_address
parcel	                            Parcel	                        The dimensions and weight of the package
customs_info	                    CustomsInfo	                    Information for the processing of customs
scan_form	                        ScanForm	                    Document created to manifest and scan multiple shipments
forms	                            Form array	                    All associated Form objects
insurance	                        Insurance	                    The associated Insurance object
rates	                            Rate array	                    All associated Rate objects
selected_rate	                    Rate	                        The specific rate purchased for the shipment, or null if unpurchased or purchased through another
                                                                    mechanism
postage_label	                    PostageLabel	                The associated PostageLabel object
messages	                        Message array	                Any carrier errors encountered during rating, discussed in more depth below
options	                            Options	                        All of the options passed to the shipment, discussed in more depth below
is_return	                        boolean	                        Set true to create as a return, discussed in more depth below
tracking_code	                    string	                        If purchased, the tracking code will appear here as well as within the Tracker object
usps_zone	                        integer	                        The USPS zone of the shipment, if purchased with USPS
status	                            string	                        The current tracking status of the shipment
tracker	                            Tracker	                        The associated Tracker object
fees	                            Fee array	                    The associated Fee objects charged to the billing user account
refund_status	                    string	                        The current status of the shipment refund process. Possible values are "submitted", "refunded", 
                                                                    "rejected".
batch_id	                        string	                        The ID of the batch that contains this shipment, if any
batch_status	                    string	                        The current state of the associated BatchShipment
batch_message	                    string	                        The current message of the associated BatchShipment
created_at	                        datetime	
updated_at	                        datetime	

Form Object
attribute	                        type	                        specification
id	                                string	                        Unique, begins with "form_"
object	                            string	                        "Form"
mode	                            string	                        "test" or "production"
form_type	                        string	                        The type of form that we returned, can be one of "high_value_report", "commercial_invoice", 
                                                                    "cod_return_label", "order_summary", "cn22"
form_url	                        string	                        The address we return the form back at
submitted_electronically	        boolean	                        If we have submitted the form to the carrier on behalf of the customer
created_at	                        datetime	
updated_at	                        datetime	

Create a Shipment
A Shipment is almost exclusively a container for other objects, and thus a Shipment may reuse many of these objects. Additionally, all the objects contained within a Shipment may be created at the same time.

The origin/destination Address and Parcel are required for rating. CustomsInfo is required to rate an international Shipment, this includes when the destination is a US Territory. The associated Tracker, Fees, and Rates are generated by EasyPost and cannot be modified by the user.

You can limit the CarrierAccounts to use for rating by passing the carrier_accounts parameter.

Create Shipment Request Parameters
param	                            example	                        info
reference	                        "my-reference"
to_address	                        <Address>	                    Can be specified by ID or attributes to create a new one, and be verified inline. See Create and
                                                                    Verify Address
from_address	                    <Address>	                    Can be specified by ID or attributes to create a new one, and be verified inline. See Create and 
                                                                    Verify Address
parcel	                            <Parcel>
carrier_accounts	                ["ca_...", ...]                 Carrier Account IDs

'''

'''
# form a shipment from existing objects
shipment = easypost.Shipment.create(
  to_address=to_address,
  from_address=from_address,
  parcel=parcel,
  customs_info=customs_info
)
'''

'''
# OR in one call

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
  customs_info=customs_info
)
'''

'''
Retrieve a list of Shipments
The Shipment List is a paginated list of all Shipment objects associated with the given API Key. It accepts a variety of parameters which can be used to modify the scope. The has_more attribute indicates whether or not additional pages can be requested. The recommended way of paginating is to use either the before_id or after_id parameter to specify where the next page begins.

Retrieve a list of Shipment Request Parameters
param	                    example	                    info
before_id	                shp_...	                    Optional pagination parameter. Only shipments created before the given ID will be included. May not be used 
                                                        with after_id
after_id	                shp_...	                    Optional pagination parameter. Only shipments created after the given ID will be included. May not be used with 
                                                        before_id
start_datetime	            2016-01-02T00:00:00Z	    Only return Shipments created after this timestamp. Defaults to 1 month ago, or 1 month before a passed 
                                                        end_datetime
end_datetime	            2016-01-02T00:00:00Z	    Only return Shipments created before this timestamp. Defaults to end of the current day, or 1 month after a 
                                                        passed start_datetime
page_size	                20	                        The number of Shipments to return on each page. The maximum value is 100
purchased	                true	                    Only include Shipments that have been purchased. Default is true
include_children	        false	                    Also include Shipments created by Child Users. Defaults to false
'''

'''
#Returns a list of shipments based on parameters
shipments = easypost.Shipment.all(
  page_size = 2,
  start_datetime = "2016-01-02T08:50:00Z"
)
'''

'''
Retrieve a Shipment
A Shipment can be retrieved by either its id or reference. However it is recommended to use EasyPost's provided identifiers because uniqueness on reference is not enforced.
'''

#shipment = easypost.Shipment.retrieve("shp_...")

'''
Buy a Shipment
To purchase a Shipment you only need to specify the Rate to purchase. This operation populates the tracking_code and postage_label attributes. The default image format of the associated PostageLabel is PNG. To change this default see the label_format option.

Additionally, insurance may be added during the purchase. To specify an amount to insure, pass the insurance attribute as a string. The currency of all insurance is USD.

Note: USPS Commercial Plus Prices will show up in both the Production and Test API.

Buy Shipment Request Parameters
param	            example
rate	            <Rate>
insurance	        "100.00"
'''

#Buys the lowest rate from carriers and insures it for 249.99
#shipment.buy(rate=shipment.lowest_rate(), insurance=249.99)

'''
Buy a Shipment without rating (One-Call Buy)
There is an alternative way to purchase shipments that is known as the "one-call buy" method. This method is often used if you have a flat-rate set with a mail carrier for a given service level OR if you know your desired service level without needing to see the rate first.

Utilizing the "one-call buy" method can improve the performance of your integration, because it cuts out an API call from our standard "create shipment" then "buy shipment" workflow. In order to achieve this behavior all you have to do is add a single carrier account and service level name to your "Create Shipment" call.

One-Call Buy Shipment Request Parameters
param	                example	                    info
reference	            "my-reference"
to_address	            <Address>	                Can be specified by ID or attributes to create a new one, and be verified inline. See Create and Verify Address
from_address	        <Address>	                Can be specified by ID or attributes to create a new one, and be verified inline. See Create and Verify Address
parcel	                <Parcel>
carrier_accounts	    ["ca_..."]
service	                "Priority"
'''

'''
# Reusing Easypost Objects

shipment = easypost.Shipment.create(
  carrier_accounts={‘0’: ‘ca_…’},
  service=’NextDayAir’,
  to_address=to_address,
  from_address=from_address,
  parcel=parcel
)
'''
'''
# OR creating Easypost objects in one call

shipment = easypost.Shipment.create(
  carrier_accounts={‘0’: ‘ca_…’},
  service=’NextDayAir’,
  to_address={
    "name": 'Dr. Steve Brule',
    "street1": '179 N Harbor Dr',
    "city": 'Redondo Beach',
    "state": 'CA',
    "zip": '90277',
    "country": 'US',
    "phone": '4153334444',
    "email": 'dr_steve_brule@gmail.com'
  },
  from_address={
    "name": 'EasyPost',
    "street1": '417 Montgomery Street',
    "street2": '5th Floor',
    "city": 'San Francisco',
    "state": 'CA',
    "zip": '94104',
    "country": 'US',
    "phone": '4153334444',
    "email": 'support@easypost.com'
  },
  parcel={
    "length": 20.2,
    "width": 10.9,
    "height": 5,
    "weight": 65.9
  }
)
'''

'''
Convert the Label format of a Shipment
A Shipment's PostageLabel can be converted from PNG to other formats. If the PostageLabel was originally generated in a format other than PNG it cannot be converted.
'''

#convert a label
#shipment.label(file_format="ZPL")

'''
Options
Shipments can have a variety of additional options which you can specify when creating a shipment. The Options object can be populated with the keys below.

Carrier specific support for each option is added as needed. To request support for a specific carrier option please email us at support@easypost.com.
Options Object
attribute	                type	                                         specification
additional_handling	        boolean	Setting this option to true, will add an additional handling charge. An Additional Handling charge may be applied to the following:
                                    Any article that is encased in an outside shipping container made of metal or wood.
                                    Any item, such as a barrel, drum, pail or tire, that is not fully encased in a corrugated cardboard shipping container.
                                    Any package with the longest side exceeding 60 inches or its second longest side exceeding 30 inches.
                                    Any package with an actual weight greater than 70 pounds.
address_validation_level	string	Setting this option to "0", will allow the minimum amount of address information to pass the validation check. Only for USPS 
                                    postage.
alcohol	                    boolean	Set this option to true if your shipment contains alcohol.
                                    UPS - only supported for US Domestic shipments
                                    FedEx - only supported for US Domestic shipments
                                    Canada Post - Requires adult signature 19 years or older. If you want adult signature 18 years or older, instead use    
                                                  delivery_confirmation: ADULT_SIGNATURE
bill_receiver_account	    string	*This field is deprecated. Use the 'payment' option object instead.
bill_receiver_postal_code	string	*This field is deprecated. Use the 'payment' option object instead.
bill_third_party_account	string	*This field is deprecated. Use the 'payment' option object instead.
bill_third_party_country	string	*This field is deprecated. Use the 'payment' option object instead.
bill_third_party_postal_code string	*This field is deprecated. Use the 'payment' option object instead.
by_drone	                boolean	 Setting this option to true will indicate to the carrier to prefer delivery by drone, if the carrier supports drone delivery.
carbon_neutral	            boolean	Setting this to true will add a charge to reduce carbon emissions.
cod_amount	                string	Adding an amount will have the carrier collect the specified amount from the recipient.
cod_method	                string	Method for payment. "CASH", "CHECK", "MONEY_ORDER"
cod_address_id	            string	The ID of the Address to which the COD payment should be returned. Defaults to the origin address. Only available on FedEx 
                                    shipments.
currency	                string	Which currency this shipment will show for rates if carrier allows.
delivery_confirmation	    string	If you want to request a signature, you can pass "ADULT_SIGNATURE" or "SIGNATURE". You may also request "NO_SIGNATURE" to leave the 
                                    package at the door.
                                    All - some options may be limited for international shipments
                                    FedEx - "INDIRECT_SIGNATURE" is also an option
                                    USPS - additional options
                                            "ADULT_SIGNATURE_RESTRICTED"
                                            "SIGNATURE_RESTRICTED"
                                    Canada Post - "DO_NOT_SAFE_DROP"
dropoff_type	            string	Method the customer will use to transfer the package to the carrier. "REGULAR_PICKUP", "SCHEDULED_PICKUP", "RETAIL_LOCATION", 
                                    "STATION" or "DROP_BOX". Supported carriers and their corresponding carrier dropoff codes:
                                        FedEx
                                        "REGULAR_PICKUP" - "REGULAR_PICKUP" (default)
                                        "SCHEDULED_PICKUP" - "REQUEST_COURIER"
                                        "RETAIL_LOCATION" - "BUSINESS_SERVICE_CENTER"
                                        "STATION" - "STATION"
                                        "DROP_BOX" - "DROP_BOX"
dry_ice	                    boolean	Package contents contain dry ice.
                                        UPS - Need dry_ice_weight to be set
                                        UPS MailInnovations - Need dry_ice_weight to be set
                                        FedEx - Need dry_ice_weight to be set
dry_ice_medical	            string	If the dry ice is for medical use, set this option to true.
                                        UPS - Need dry_ice_weight to be set
                                        UPS MailInnovations - Need dry_ice_weight to be set
                                        dry_ice_weight	string	Weight of the dry ice in ounces.
                                        UPS - Need dry_ice to be set
                                        UPS MailInnovations - Need dry_ice to be set
                                        FedEx - Need dry_ice to be set
endorsement	                string	Possible values "ADDRESS_SERVICE_REQUESTED", "FORWARDING_SERVICE_REQUESTED", "CHANGE_SERVICE_REQUESTED", 
                                    "RETURN_SERVICE_REQUESTED", "LEAVE_IF_NO_RESPONSE"
freight_charge	            double	Additional cost to be added to the invoice of this shipment. Only applies to UPS currently.
handling_instructions	    string	This is to designate special instructions for the carrier like "Do not drop!".
hazmat	                    string	Dangerous goods indicator. Possible values are "PRIMARY_CONTAINED", "PRIMARY_PACKED", "PRIMARY", "SECONDARY_CONTAINED", 
                                    "SECONDARY_PACKED", "SECONDARY", "ORMD", "LIMITED_QUANTITY", "LITHIUM". Applies to USPS, FedEx and DHL eCommerce.
hold_for_pickup	            boolean	Package will wait at carrier facility for pickup.
incoterm	                string	Incoterm negotiated for shipment. Supported values are "EXW", "FCA", "CPT", "CIP", "DAT", "DAP", "DDP", "FAS", "FOB", "CFR", and 
                                    "CIF". Setting this value to anything other than "DDP" will pass the cost and responsibility of duties on to the recipient of the package(s), as specified by Incoterms rules
invoice_number	            string	This will print an invoice number on the postage label.
label_date	                string	Set the date that will appear on the postage label. Accepts ISO 8601 formatted string including time zone offset. EasyPost stores 
                                    all dates as UTC time.
label_format	            string	Supported label formats include "PNG", "PDF", "ZPL", and "EPL2". "PNG" is the only format that allows for conversion.
machinable	                boolean	Whether or not the parcel can be processed by the carriers equipment.
payment	                    object	Setting payment type to bill the correct account for purchasing postage.
                                        type - (string) Supported values are "SENDER", "THIRD_PARTY", "RECEIVER", "COLLECT". Defaults to SENDER.
                                        account - (string) Setting account number. Required for RECEIVER and THIRD_PARTY.
                                        country - (string) Setting country code that the account is based in. Required for THIRD_PARTY.
                                        postal_code - (string) Setting postal code that the account is based in. Required for RECEIVER and THIRD_PARTY.
print_custom_1	            string	You can optionally print custom messages on labels. The locations of these fields show up on different spots on the carrier's 
                                    labels.
print_custom_2	            string	An additional message on the label. Same restrictions as print_custom_1
print_custom_3	            string	An additional message on the label. Same restrictions as print_custom_1
print_custom_1_barcode	    boolean	Create a barcode for this custom reference if supported by carrier.
print_custom_2_barcode	    boolean	Create a barcode for this custom reference if supported by carrier.
print_custom_3_barcode	    boolean	Create a barcode for this custom reference if supported by carrier.
print_custom_1_code	        string	Specify the type of print_custom_1.
                                    FedEx
                                        (null) - If print_custom_1_code is not provided it defaults to Customer Reference
                                        PO - Purchase Order Number
                                        DP - Department Number
                                        RMA - Return Merchandise Authorization
                                    UPS
                                        AJ - Accounts Receivable Customer Account
                                        AT - Appropriation Number
                                        BM - Bill of Lading Number
                                        9V - Collect on Delivery (COD) Number
                                        ON - Dealer Order Number
                                        DP - Department Number
                                        3Q - Food and Drug Administration (FDA) Product Code
                                        IK - Invoice Number
                                        MK - Manifest Key Number
                                        MJ - Model Number
                                        PM - Part Number
                                        PC - Production Code
                                        PO - Purchase Order Number
                                        RQ - Purchase Request Number
                                        RZ - Return Authorization Number
                                        SA - Salesperson Number
                                        SE - Serial Number
                                        ST - Store Number
                                        TN - Transaction Reference Number
                                        EI - Employer’s ID Number
                                        TJ - Federal Taxpayer ID No.
print_custom_2_code	        string	See print_custom_1_code.
print_custom_3_code	        string  See print_custom_1_code.
saturday_delivery	        boolean Set this value to true for delivery on Saturday. When setting the saturday_delivery option, you will only get rates for services 
                                    that are eligible for saturday delivery. If no services are available for saturday delivery, then you will not be returned any rates. You may need to create 2 shipments, one with the saturday_delivery option set on one without to get all your eligible rates.
special_rates_eligibility	string	This option allows you to request restrictive rates from USPS. Can set to 'USPS.MEDIAMAIL' or 'USPS.LIBRARYMAIL'.
smartpost_hub	            string	You can use this to override the hub ID you have on your account.
smartpost_manifest	        string	The manifest ID is used to group SmartPost packages onto a manifest for each trailer.
billing_ref	                string	A reference ID for aggregating DHL eCommerce billing data.
certified_mail	            boolean	Certified Mail provides the sender with a mailing receipt and, upon request, electronic verification that an article was delivered 
                                    or that a delivery attempt was made.
registered_mail	            boolean	Registered Mail is the most secure service that the USPS offers. It incorporates a system of receipts to monitor the movement of 
                                    the mail from the point of acceptance to delivery
registered_mail_amount	    double	The value of the package contents
return_receipt	            boolean	An electronic return receipt may be purchased at the time of mailing and provides a shipper with evidence of delivery (to whom the 
                                    mail was delivered and date of delivery), and information about the recipient's actual delivery address. Only applies to the USPS.
'''

'''
#Create a shipoment with options

to_address = easypost.Address.create(...)
from_address = easypost.Address.create(...)
parcel = easypost.Parcel.create(...)

shipment = easypost.Shipment.create(
    to_address=to_address,
    from_address=from_address,
    parcel=parcel,
    options={'address_validation_level': 0}
)
'''

'''
Rates
After a Shipment is successfully created, it will automatically fetch Rates. You can limit the CarrierAccounts to use for rating by passing the carrier_accounts parameter upon Shipment creation.

There are three rate types: the actual rate that will be purchased, rate and currency, the published non-discounted rate, list_rate and list_currency, and the rate if purchased from the post office, retail_rate and retail_currency.

Rate Object
attribute	                type	                    specification
id	                        string	                    unique, begins with 'rate_'
object	                    string	                    "Rate"
mode	                    string	                    "test" or "production"
service	                    string	                    service level/name
carrier	                    string	                    name of carrier
carrier_account_id	        string	                    ID of the CarrierAccount record used to generate this rate
shipment_id	                string	                    ID of the Shipment this rate belongs to
rate	                    string	                    the actual rate quote for this service
currency	                string	                    currency for the rate
retail_rate	                string	                    the retail rate is the in-store rate given with no account
retail_currency	            string	                    currency for the retail rate
list_rate	                string	                    the list rate is the non-negotiated rate given for having an account with the carrier
list_currency	            string	                    currency for the list rate
delivery_days	            integer	                    delivery days for this service
delivery_date	            string	                    date for delivery
delivery_date_guaranteed	boolean	                    indicates if delivery window is guaranteed (true) or not (false)
est_delivery_days*	        integer	                    *This field is deprecated and should be ignored.
created_at	                datetime	
updated_at	                datetime	

'''

'''
Regenerate Rates for a Shipment
You can update the Rates of a Shipment at any time. This operation respects the carrier_accounts attribute.
'''
#Generate rates for a shipment
#shipment.get_rates()

'''
Messages
When rating a Shipment or Pickup, some carriers may fail to generate rates. These failures are returned as part of the Shipment or Pickup as part of their messages attribute, and follow a common object structure.

It is important to note that the message value for any member of this list comes directly from the carrier, not from EasyPost. This means that if you see an authentication or other non-shipping error here, it is not an issue between you and EasyPost, it is an issue between you and the carrier, or an issue with the given data.

Message Object
attribute	        type	            specification
carrier	            string	            the name of the carrier generating the error, e.g. "UPS"
type	            string	            the category of error that occurred. Most frequently "rate_error"
message	            string	            the string from the carrier explaining the problem
carrier_account_id	string	            the account id of the carrier. Useful if you have multiple accounts with the same carrier

SmartRate
The SmartRate API provides shippers with highly accurate, Shipment-level transit time predictions which can be used to save money, improve on-time delivery, and provide end customers with reliable delivery estimates.

The SmartRate API accepts a Shipment ID and returns predicted transit days across a variety of percentiles for each carrier service being evaluated for the Shipment. The transit time predictions in the response are based off of a sophisticated model using actual historical data for the shipping lane in question.

To make a request to the SmartRate API, first create a Shipment, then make the SmartRate call. Using the response, you can now make better data-driven decisions about which Rate to select when purchasing a label.

Time in Transit Object
attribute	        type	        specification
percentile_50	    integer	    expected transit days at the 50th percentile
percentile_75	    integer	    expected transit days at the 75th percentile
percentile_85	    integer	    expected transit days at the 85th percentile
percentile_90	    integer	    expected transit days at the 90th percentile
percentile_95	    integer	    expected transit days at the 95th percentile
percentile_97	    integer	    expected transit days at the 97th percentile
percentile_99	    integer	    expected transit days at the 99th percentile
'''
'''
Retrieve Time in Transit statistics across all Rates for a Shipment
The SmartRate API returns a Time in Transit object with transit days across a variety of percentiles for every Rate for a given Shipment. Transit days are calculated as the number of business days between the first time the carrier acknowledges possession of the Shipment and the first out-for-delivery attempt.
'''
#Retrieves a list of time in transit stats
#shipment.get_smartrates()

'''
Shipping Insurance
Insuring your Shipment is as simple as sending us the value of the contents. We charge 0.5% of the value, with a 50 cent minimum, and handle all the claims. All our claims are paid out within 10 days.

To buy insurance, first purchase the Shipment, then make the insurance call before the package begins being handled by the carrier.
'''
#Buy insurance on a PURCHASED shipment
#purchased_shipment.insure(amount=888.50)

'''
Refunds
USPS shipping labels can be refunded if requested within 30 days of generation. The processing time is at least 15 days, after which the funds will return to your EasyPost balance. EasyPost fees will also be refunded. To qualify, a shipment must not have been scanned by the USPS.

UPS and FedEx shipping labels may be refunded within 90 days of creation.
'''

'''
Refund a Shipment
Refunding a Shipment is available for many carriers supported by EasyPost. Once the refund has been submitted, refund_status attribute of the Shipment will be populated with one of the possible values: "submitted", "refunded", "rejected". The most common initial status is "submitted". Many carriers require that the refund be processed before the refund_status will move to "refunded". The length of this process depends on the carrier, but no greater than 30 days.

Refunds created very shortly after a label is generated may be improperly flagged as invalid, but you may retry a refund with the "rejected" status by submitting the same request again. Carriers that are bill-on-scan tend to have refunds attempts return as "not_applicable", which will not change with multiple retries.
'''
#shipment.refund()

'''
Returns
If you are shipping merchandise or other frequently-returned products, you may wish to generate return labels to include with your shipment, for you customer's convenience. EasyPost offers a simple way to submit the same parameters as your initial shipment, but with an additional flag set, that will generate you a return label to receive any return shipments at your original from address.

It's important for some carriers, with different return billing, to specify a return label even if it's not a return label for an earlier Shipment.

If doing more than 10,000 USPS Returns in a year, please contact EasyPost for the USPS scan-based return program, which we also offer.
'''

'''
Create Return for a Shipment
You can easily create return labels. All you need to do is set the is_return parameter to "true", leave the addresses the same as the initial Shipment's creation request and we switch the To and From Addresses for the return Shipment.

param	        example
is_return	    true
to_address	  the original Shipment's to_address
from_address	the original Shipment's from_address
'''

#Create a return shipment
'''
to_address = easypost.Address.create(...)
from_address = easypost.Address.create(...)
parcel = easypost.Parcel.create(...)

shipment = easypost.Shipment.create(
  to_address=to_address,
  from_address=from_address,
  parcel=parcel,
  is_return=True
)
'''

'''
TaxIdentifiers
TaxIdentifiers are identifying numbers or IDs that are used to charge a specific party when dealing with the importing or exporting of good across international borders.

TaxIdentifiers is a list of TaxIdentifier objects, which allows you to supply up to 8 Tax Identification numbers. The fields for the TaxIdentifier object are outlined below.

TaxIdentifier Object
attribute	        type	      specification
entity	          string	      Which entity the tax id belongs to ("SENDER" or "RECEIVER")
tax_id	          string	      The actual tax id number
tax_id_type	      string	      The type of tax id that is being used with the shipment (see possible types by carrier here)
issuing_country	  string	      The issuing country of the tax id number
'''

#Create a shipment with tax identifier object
'''
to_address = easypost.Address.create(...)
from_address = easypost.Address.create(...)
parcel = easypost.Parcel.create(...)
customs_info = easypost.CustomsInfo.create(...)

shipment = easypost.Shipment.create(
  to_address=to_address,
  from_address=from_address,
  parcel=parcel,
  customs_info=customs_info,
  tax_identifiers=[{
    "entity": "SENDER",
    "tax_id": "GB123456789",
    "tax_id_type": "IOSS",
    "issuing_country": "GB",
  }]
)
'''

'''
Trackers
A Tracker object contains all of the tracking information for a package. A Tracker is created automatically whenever you buy a Shipment through EasyPost; if you don’t use EasyPost to purchase your shipping labels, you can still track packages through our API by creating a Tracker object directly. Each Tracker is continually updated in the background as the package moves through its life cycle, regardless of whether or not the label was purchased through EasyPost.

After creation, a Tracker object will be updated periodically based on when the carrier provides EasyPost with new tracking information. This information can be consumed by using our webhooks infrastructure. Every time a Tracker is updated a webhook Event will be sent.

The Tracker object contains both the current information about the package as well as previous updates. All of the previous updates are stored in the tracking_details array. Each TrackingDetail object contains the status, the message from the carrier, and a TrackingLocation.

The TrackingLocation contains city, state, country, and zip information about the location where the package was scanned. The information each carrier provides is different, so some carriers may not make use of all of these fields.

Some Tracker objects may also contain a CarrierDetail, which stores some additional information about the Tracker that the carrier has made available to EasyPost. The CarrierDetail object contains the service and container_type of the package. Additionally, it also stores the est_delivery_date_local and est_delivery_time_local, which provide information about the local delivery time.

It's worth noting that tracking_codes are not globally unique. Each carrier promises uniqueness for a given tracking_code for a certain period of time, but the length of time varies greatly based on the specific carrier and service level. The carriers do eventually recycle tracking_codes, and for this reason enforcing uniqueness on the tracking_code field is not recommended. EasyPost does, however, prevent the creation of duplicate Trackers based on tracking_code and carrier; duplicate requests by the same User will simply return the original Tracker.

Tracker Object
attribute	          type	          specification
id	              string	          Unique identifier, begins with "trk_"
object	          string	          "Tracker"
mode	            string	          "test" or "production"
tracking_code	    string	          The tracking code provided by the carrier
status	          string	          The current status of the package, possible values are "unknown", "pre_transit", "in_transit", "out_for_delivery", "delivered", 
                                    "available_for_pickup", "return_to_sender", "failure", "cancelled" or "error"
signed_by	        string	          The name of the person who signed for the package (if available)
weight	          float	            The weight of the package as measured by the carrier in ounces (if available)
est_delivery_date	datetime	        The estimated delivery date provided by the carrier (if available)
shipment_id	      string	          The id of the EasyPost Shipment object associated with the Tracker (if any)
carrier	          string	          The name of the carrier handling the shipment
tracking_details	TrackingDetail    array	Array of the associated TrackingDetail objects
carrier_detail	  CarrierDetail	    The associated CarrierDetail object (if available)
public_url	      string	          URL to a publicly-accessible html page that shows tracking details for this tracker
fees	            Fee array	        Array of the associated Fee objects
created_at	      datetime	
updated_at	      datetime

TrackingDetail Object
attribute	        type	          specification
object	          string	        "TrackingDetail"
message	          string	        Description of the scan event
status	          string	        Status of the package at the time of the scan event, possible values are "unknown", "pre_transit", "in_transit", "out_for_delivery", 
                                  "delivered", "available_for_pickup", "return_to_sender", "failure", "cancelled" or "error"
datetime  	      datetime	      The timestamp when the tracking scan occurred
source	          string	        The original source of the information for this scan event, usually the carrier
tracking_location	TrackingLocation	The location associated with the scan event

TrackingLocation Object
attribute	        type	          specification
object	          string	        "TrackingLocation"
city	            string	        The city where the scan event occurred (if available)
state	            string	        The state where the scan event occurred (if available)
country	          string	        The country where the scan event occurred (if available)
zip	              string	        The postal code where the scan event occurred (if available)

CarrierDetail Object
attribute	                    type	            specification
object	                      string	          "CarrierDetail"
service	                      string	          The service level the associated shipment was shipped with (if available)
container_type	              string	          The type of container the associated shipment was shipped in (if available)
est_delivery_date_local	      date	            The estimated delivery date as provided by the carrier, in the local time zone (if available)
est_delivery_time_local	      time	            The estimated delivery time as provided by the carrier, in the local time zone (if available)
origin_location	              string	          The location from which the package originated, stringified for presentation (if available)
origin_tracking_location	    TrackingLocation	The location from which the package originated, broken down by city/state/country/zip (if available)
destination_location	        string	          The location to which the package is being sent, stringified for presentation (if available)
destination_tracking_location	TrackingLocation	The location to which the package is being sent, broken down by city/state/country/zip (if available)
guaranteed_delivery_date	    datetime	        The date and time the carrier guarantees the package to be delivered by (if available)
alternate_identifier	        string	          The alternate identifier for this package as provided by the carrier (if available)
initial_delivery_attempt	    datetime	        The date and time of the first attempt by the carrier to deliver the package (if available)

Testing Specific Tracking States
Sometimes you may want to simulate specific tracking statuses (e.g. "out_for_delivery") within your application to test how your application responds. EasyPost has a set of test tracking_codes that, when sent to the API, respond with specific tracking statuses and send a webhook Event to your test mode URL. The tracking updates that are sent by these tracking_codes will contain canned information, but it will be similar in form to the information normally provided by the carrier you selected.

Test Tracking Codes
tracking_code	      status
EZ1000000001	      pre_transit
EZ2000000002	      in_transit
EZ3000000003	      out_for_delivery
EZ4000000004	      delivered
EZ5000000005	      return_to_sender
EZ6000000006	      failure
EZ7000000007	      unknown

Carrier Tracking Strings
Carrier	      String Representation
AmazonMws	              AmazonMws
APC	                    APC
Asendia	                Asendia
Asendia USA	            AsendiaUsa
Australia Post	        AustraliaPost
AxlehireV3	            AxlehireV3
Better Trucks	          BetterTrucks
Bond	                  Bond
Cainiao	                Cainiao
Canada Post	            CanadaPost
Canpar	                Canpar
CDL Last Mile Solutions	ColumbusLastMile
Chronopost	            Chronopost
CloudSort	              CloudSort
Courier Express	        CourierExpress
CouriersPlease	        CouriersPlease
Dai Post	              DaiPost
Deutsche Post	          DeutschePost
Deutsche Post UK	      DeutschePostUK
DHL eCommerce Asia	    DHLEcommerceAsia
DHL eCommerce Solutions	DhlEcs
DHL Express	            DHLExpress
DPD	                    DPD
DPD UK	                DPDUK
ePost Global	          ePostGlobal
Estafeta	              Estafeta
Fastway	                Fastway
FedEx	                  FedEx
FedEx Cross Border	    FedExCrossBorder
FedEx Mailview	        FedExMailview
FedEx SameDay City	    FedExSameDayCity
FedEx SmartPost	        FedexSmartPost
FirstMile	              FirstMile
Globegistics	          Globegistics
GSO	                    GSO
Hermes	                Hermes
Interlink Express	      InterlinkExpress
JP Post	                JPPost
Kuroneko Yamato	        KuronekoYamato
La Poste	              LaPoste
LaserShip	              LaserShipV2
Loomis Express	        LoomisExpress
LSO	                    LSO
Newgistics	            Newgistics
OnTrac	                OnTrac
Osm Worldwide	          OsmWorldwide
Parcelforce	            Parcelforce
Passport	              PassportGlobal
PCF Final Mile	        PcfFinalMile
PostNL	                PostNL
Purolator	              Purolator
Royal Mail	            RoyalMail
SEKO OmniParcel     	  OmniParcel
SF Express	            SFExpress
Spee-Dee	              SpeeDee
StarTrack	              StarTrack
TForce	                TForce
UDS	                    UDS
UPS	                    UPS
UPS i-parcel	          UPSIparcel
UPS Mail Innovations	  UPSMailInnovations
USPS	                  USPS
Veho	                  Veho
Yanwen	                Yanwen
'''

'''
Create a Tracker
A Tracker can be created with only a tracking_code. Optionally, you can provide the carrier parameter, which indicates the carrier the package was shipped with. If no carrier is provided, EasyPost will attempt to determine the carrier based on the tracking_code provided. Providing a carrier parameter is recommended, since some tracking_codes are ambiguous and may match with more than one carrier. In addition, not having to auto-match the carrier will significantly speed up the response time.

In an effort to reduce wasted resources, EasyPost prevents the creation of duplicate Trackers. A Tracker is considered to be a duplicate if another Tracker with the same tracking_code and carrier was created by the same User in the last three months. In the case where a duplicate request is submitted, the original Tracker will be returned.

Create Tracker Request Parameters
param	            example	                    info
tracking_code	9400110898825022579493	    The tracking code associated with the package you'd like to track
carrier	          USPS	                  The carrier associated with the tracking_code you provided. The carrier will get auto-detected if none is provided
'''

#Creates a tracker
'''
tracker = easypost.Tracker.create(
    tracking_code="9400110898825022579493",
    carrier="USPS"
)
'''

'''
Batches
The Batch object allows you to perform operations on multiple Shipments at once. This includes scheduling a Pickup, creating a ScanForm and consolidating labels. Operations performed on Batches are asynchronous and take advantage of our webhook infrastructure.

Batch Object
attribute	          type	              specification
id	                string	            Unique, begins with "batch_"
reference	          string	            An optional field that may be used in place of ID in some API endpoints
object	            string	            "Batch"
mode	              string	            "test" or "production"
state	              string	            The overall state. Possible values are "creating", "creation_failed", "created", "purchasing", "purchase_failed", "purchased", 
                                        "label_generating", and "label_generated"
num_shipments	      integer	            The number of shipments added
shipments	          BatchShipment array	
status	            object	            A map of BatchShipment statuses to the count of BatchShipments with that status. Valid statuses are "postage_purchased", 
                                        "postage_purchase_failed", "queued_for_purchase", and "creation_failed"
label_url	          string	            The label image url
scan_form	          ScanForm	          The created ScanForm
pickup	            Pickup	            The created Pickup
created_at	        datetime	
updated_at	        datetime	

BatchShipment Object
attribute	          type	              specification
id	              string	              The id of the Shipment. Unique, begins with "shp_"
reference	        string	              An optional field that may be used in place of ID in some API endpoints
batch_status	    string	              The current status. Possible values are "postage_purchased", "postage_purchase_failed", "queued_for_purchase", and 
                                        "creation_failed"
batch_message	    string	              A human readable message for any errors that occurred during the Batch's life cycle
'''

'''
Create a Batch
A Batch can be created with or without Shipments. When created with Shipments the initial state will be creating. Once the state changes to created a webhook Event will be sent. When created with no Shipments the initial state will be created and webhook will be sent.
'''

#create a batch and enter shipments by ID
'''
batch = easypost.Batch.create(
  shipments=[{"id": "shp_..."}]
);
'''

#Retreieve a batch and add an array of shipments
'''
batch = easypost.Batch.retrieve('batch_...')
batch.add_shipments(shipments=[
  {'id': 'shp_...'},
  {'id': 'shp_...'}
])
'''

'''
Remove Shipments from a Batch
There could be times when a Shipment needs to be removed from the Batch during its life cycle. Removing a Shipment does not remove it from the consolidated label or ScanForm.
'''
#Remove shipments from a batch
'''
batch.remove_shipments(shipments=[
  {'id': 'shp_...'}
])
'''

'''
Buy a Batch
Once you have added all of your Shipments to a Batch, issue a buy request to enqueue a background job to purchase the shipments and generate all necessary labels.

Purchasing may take anywhere from a few seconds to an hour, depending on the size of the batch, the carrier, and Internet weather.

Buy Batch Request Parameters
This endpoint takes no parameters.
'''

#buy a batch
#batch.buy()

'''
Batch Labels
One of the advantages of processing Shipments in batches is the ability to consolidate the PostageLabel into one file. This can only be done once for each batch and all Shipments must have a status of postage_purchased.

Available label formats are 'pdf', 'zpl' or 'epl2' format. Like converting a PostageLabel format, if this process will change the format of the labels they must have been created as PNGs.
'''
#Generate a batch label and format
#batch.label(file_format = 'epl2')

#Generate a Scanform/Manifest for a Batch
#batch.create_scan_form();

'''
CustomsInfos
CustomsInfo objects contain CustomsItem objects and all necessary information for the generation of customs forms required for international shipping.

Please see the Shipments documentation for examples of including a CustomsInfo object in a shipment.

CustomsInfo Object
attribute	            type	                      specification
id	                  string	            Unique, begins with 'cstinfo_'
object	              string	            'CustomsInfo'
eel_pfc	              string	            "EEL" or "PFC" value less than $2500: "NOEEI 30.37(a)"; value greater than $2500: see Customs Guide
contents_type	        string	            "documents", "gift", "merchandise", "returned_goods", "sample", or "other"
contents_explanation	string              (max 255 characters) Human readable description of content. Required for certain carriers and always required if 
                                          contents_type is "other"
customs_certify	      boolean	            Electronically certify the information provided
customs_signer	      string	            Required if customs_certify is true
non_delivery_option	  string	            "abandon" or "return", defaults to "return"
restriction_type	    string	            "none", "other", "quarantine", or "sanitary_phytosanitary_inspection"
restriction_comments	string	            Required if restriction_type is not "none"
customs_items	        CustomItem array	  Describes to products being shipped
created_at	          datetime	
updated_at	          datetime	
'''

'''
Create a CustomsInfo
A CustomsInfo object contains all administrative information for processing customs, as well as a list of CustomsItems. When creating a CustomsInfo, you may store the ID from the response for use later in shipment creation.

Create CustomsInfo Request Parameters
param	              example
customs_certify	    true
customs_signer	    "Steve Brule"
contents_type	      "merchandise"
restriction_type	  "none"
eel_pfc	            "NOEEI 30.37(a)"
customs_items	      [<CustomsItem>,<CustomsItem>,...]
'''

#Create a customs_info example
'''
customs_item = easypost.CustomsItem.create(...)

customs_info = easypost.CustomsInfo.create(
  eel_pfc='NOEEI 30.37(a)',
  customs_certify=True,
  customs_signer='Steve Brule',
  contents_type='merchandise',
  contents_explanation='',
  restriction_type='none',
  restriction_comments='',
  non_delivery_option='abandon',
  customs_items=[customs_item, {
    'description': 'Sweet shirts',
    'quantity': 2,
    'weight': 11,
    'value': 23,
    'hs_tariff_number': '654321',
    'origin_country': 'US'
  }]
)
'''

'''
CustomsItems
A CustomsItem object describes goods for international shipment and should be created then included in a CustomsInfo object.

CustomsItem Object
attribute	              type	                    specification
id	                  string	                    Unique, begins with 'cstitem_'
object	              string	                    'CustomsItem'
description	          string	                    Required, description of item being shipped
quantity	            float	                      Required, greater than zero
value	                float (USD)	                Required, greater than zero, total value (unit value * quantity)
weight	              float (oz)	                Required, greater than zero, total weight (unit weight * quantity)
hs_tariff_number	    string	                    Harmonized Tariff Schedule, e.g. "6109.10.0012" for Men's T-shirts
code	                string	                    SKU/UPC or other product identifier
origin_country	      string	                    Required, 2 char country code
currency	            string	                    3 char currency code, default USD
created_at	          datetime	
updated_at	          datetime	
'''

'''
Create a CustomsItem
A CustomsItem contains information relating to each product within the package. When creating a customs item, you may store the ID from the response for use later in CustomsInfo creation.

Create CustomsItem Request Parameters
param	                  example
description	            "T-Shirt"
quantity	              1
weight	                5
value	                  10
hs_tariff_number	      "123456"
origin_country	        "US"
'''

#Create a Customs_items
'''
customs_item = easypost.CustomsItem.create(
  description='T-shirt',
  quantity=1,
  value=10,
  weight=5,
  hs_tariff_number='123456',
  origin_country='us'
)
'''

'''
Events
Webhook Events are triggered by changes in objects you've created via the API. Every time an Event related to one of your objects is created, EasyPost guarantees at least one POST request will be sent to each of the webhook URLs set up for your account. For this reason, we strongly encourage your webhook handler to be idempotent. See the webhooks guide for more information.

Possible Event Types

Batch
A "batch.created" Event is created when the initial creation of a Batch object is complete.
A "batch.updated" Event is created whenever the status of a Batch object changes.

Insurance
An "insurance.purchased" Event is created whenever a standalone Insurance completes purchasing and reporting to the insurer.
An "insurance.cancelled" Event is created whenever a standalone Insurance fails purchasing, is refunded to your account balance, and is not reported to the insurer.

Payment
A "payment.created" Event is created whenever a Bank Account or Credit Card is successfully charged. For credit card charges, this event indicates that the charge is complete and your account balance has already been updated. For bank account transfers (ACH) this indicates the beginning of the transfer process, which may still later fail.
A "payment.completed" Event is created when a Bank Account transfer is successfully completed and credited to your account balance. This event indicates that the accounting for that transfer is now complete.
A "payment.failed" Event is created when a Bank Account transfer or Credit Card charge has an issue and cannot be completed. For bank account transfers that fail your account balance may see a failure deduction and an EasyPost could possibly need to get in contact with you about your account status.

Refund
A "refund.successful" Event is created whenever a non-instantaneous Refund request is completed. USPS is the best example of this, as USPS postage takes 15+ days to be refunded after the initial refund creation.

Report
A "report.new" Event is created when a Report object is initially created. The report won't be immediately ready for download.
A "report.available" Event is created when a Report becomes available to download.
A "report.failed" Event is created when a Report fails to generate.

Scan Form
A "scan_form.created" Event is created when the initial creation of a ScanForm object is complete.
A "scan_form.updated" Event is created whenever the status of a ScanForm object changes.

Shipment Invoice
A "shipment.invoice.created" Event is created when a ShipmentInvoice object is initially created.
A "shipment.invoice.updated" Event is created if a ShipmentInvoice is adjusted and updated.

Tracker
A "tracker.created" Event is created when the initial creation of a Tracker object is complete.
A "tracker.updated" Event is created whenever a Tracker object gets successfully updated.

Event Object
attribute	                type	                    specification
object	                  string	                    "Event"
id	                      string	                    Unique identifier, begins with "evt_"
mode	                    string	                    "test" or "production"
description	              string	                    Result type and event name, see the "Possible Event Types" section for more information
previous_attributes	      object	                    Previous values of relevant result attributes
result	                  object	                    The object associated with the Event. See the "object" attribute on the result to determine its specific type. 
                                                      This field will not be returned when retrieving events directly from the API
status	                  string	                    The current status of the event. Possible values are "completed", "failed", "in_queue", "retrying", or "pending" 
                                                      (deprecated)
pending_urls	            string array	              Webhook URLs that have not yet been successfully notified as of the time this webhook event was sent. The URL 
                                                      receiving the Event will still be listed in pending_urls, as will any other URLs that receive the Event at the same time
completed_urls	          string array	              Webhook URLs that have already been successfully notified as of the time this webhook was sent
created_at	              datetime	
updated_at	              datetime
'''

'''
Fees
Fee objects are used to represent the breakdown of charges made when purchasing an item on EasyPost. Shipments and Trackers both have associations to Fee objects.

Each Shipment object will have a Fee of type "LabelFee" to represent the label fee charged by EasyPost for the service. Shipments with postage collected by EasyPost (as opposed to shipments with postage collected directly by the carrier) will have a "PostageFee" according to the postage amount. Insurance on a Shipment will add an "InsuranceFee" with the insurance premium (not the covered value) for the amount. Tracker objects will have a "TrackerFee" with the price, even when a Tracker is free.

Fee Object
attribute	              type	                        specification
object	                string	                      "Fee"
type	                  string	                      The name of the category of fee. Possible types are "LabelFee", "PostageFee", "InsuranceFee", and "TrackerFee"	
amount	                string	                      USD value with sub-cent precision
charged	                boolean	                      Whether EasyPost has successfully charged your account for the fee
refunded	              boolean	                      Whether the Fee has been refunded successfully
'''

'''
Orders
The Order object represents a collection of packages and can be used for Multi-Piece Shipments. Like a single Shipment each Order consists of a "to" and "from" Address to be used for each Shipment within the Order. These Addresses will be copied to each Shipment so there is no need to specify them multiple times. Each Shipment must then specify its Parcel, Options, and CustomsInfo.

An Order created with valid Address Objects and Parcel data nested within the Order's Shipment object will automatically retrieve available shipping Rate options.

Order Object
attribute	                type	                        specification
id	                      string	                      Unique, begins with "order_"
object	                  string	                      "Order"
reference	                string	                      An optional field that may be used in place of id in other API endpoints
mode	                    string	                      "test" or "production"
to_address	              Address	                      The destination address
from_address	            Address	                      The origin address
return_address	          Address	                      The shipper's address, defaults to from_address
buyer_address	            Address	                      The buyer's address, defaults to to_address
shipments	                Shipment array              	All associated Shipment objects. Maximum of 100.
rates	                    Rate array	                  All associated Rate objects
messages	                Message array	                Any carrier errors encountered during rating
is_return	                boolean	                      Set true to create as a return
created_at	              datetime	
updated_at	              datetime	
'''

'''
Create an Order
An Order is almost exclusively a container for other objects, and thus an Order may reuse many of these objects. Alternatively, all the objects contained within an Order may be created at the same time.

You can limit the CarrierAccounts to use for rating by passing the carrier_accounts parameter.

Create Order Request Parameters
param	                  example	                        info
reference	              "my-reference"
to_address	            <Address>	                  Can be specified by ID or attributes to create a new one, and be verified inline. See Create and Verify Address
from_address	          <Address>	                  Can be specified by ID or attributes to create a new one, and be verified inline. See Create and Verify Address
shipments	              [<Shipment>, <Shipment>, ...]
carrier_accounts	      [{"id": "ca_..."}, ...]
'''
#Creating an order
'''
order = easypost.Order.create(
    to_address=to_address,
    from_address=from_address,
    shipments=[
        {
            "parcel": {
                "predefined_package": "FedExBox",
                "weight": 10.2
            }
        },
        {
            "parcel": {
                "predefined_package": "FedExBox",
                "weight": 17.5
            }
        }
    ]
)
'''

#Retrieve an Order
#order = easypost.Order.retrieve("order_...")

#Buy an Order
#order.buy(carrier="FedEx", service="FEDEX_GROUND") #Buys an order by carrier and service

'''
Pickups
The Pickup object allows you to schedule a pickup from your carrier from your customer's residence or place of business. Supported carriers include:

Asendia Europe
Canada Post
Canpar
DHL Express
Endicia
FedEx
GSO
Lasership
LSO
Ontrac
Purolator
UPS
USPS
After a Pickup is successfully created, it will automatically fetch PickupRates for each CarrierAccount specified that supports scheduled pickups. Then a PickupRate must be selected and purchased before the pickup can be successfully scheduled.

Pickup Object
attribute	                      type	                          specification
id	                            string	                        unique, begins with "pickup_"
object	                        string	                        "Pickup"
reference	                      string	                        An optional field that may be used in place of ID in some API endpoints
mode	                          string	                        "test" or "production"
status	                        string	                        One of: "unknown", "scheduled", or "canceled"
min_datetime	                  datetime	                      The earliest time at which the package is available to pick up
max_datetime	                  datetime	                      The latest time at which the package is available to pick up. Must be later than the min_datetime
is_account_address	            boolean	                        Is the pickup address the account's address?
instructions	                  string	                        Additional text to help the driver successfully obtain the package
messages  	                  Message array	                    A list of messages containing carrier errors encountered during pickup rate generation
confirmation	                  string	                        The confirmation number for a booked pickup from the carrier
shipment	                      Shipment	                      The associated Shipment
address	                        Address	                        The associated Address
carrier_accounts	          CarrierAccount array	              The list of carriers (if empty, all carriers were used) used to generate pickup rates
pickup_rates	                PickupRate array	                The list of different pickup rates across valid carrier accounts for the shipment
created_at	                  datetime	
updated_at	                  datetime	

PickupRate Object
attribute	                      type	                          specification
id	                            string	                        unique, begins with 'pickuprate_'
object	                        string	                        "PickupRate"
mode	                          string	                        "test" or "production"
service	                        string	                        service name
carrier	                        string	                        name of carrier
rate	                          string	                        the actual rate quote for this service
currency	                      string	                        currency for the rate
pickup_id	                      string	                        the ID of the pickup this is a quote for
created_at	                    datetime	
updated_at	                    datetime	
'''

'''
Create a Pickup
Creating a Pickup will automatically fetch rates for the given time frame and location.

Pickups work with existing shipments or a batch and either a fully-specified Address object or id. The examples below assume that a shipment and address have both already been created.

Create Pickup Request Parameters
param	                      example
address	                    <Address>
shipment                  	<Shipment> (if no batch)
batch	                      <Batch> (if no shipment)
carrier_accounts	         [<CarrierAccount>,<CarrierAccount>,...]
instructions	              "Knock loudly"
reference	                  "my-custom-pickup"
is_account_address	        true
min_datetime	              2014-10-21 10:30:00
max_datetime	              2014-10-22 10:30:00
'''

#Create a pickup
'''
pickup = easypost.Pickup.create(
  address=address,
  shipment=shipment,
  reference="my-first-pickup",
  min_datetime="2014-10-21 10:30:00",
  max_datetime="2014-10-22 10:30:00",
  is_account_address=False,
  instructions="Special pickup instructions"
)
'''

#Retrieve a pickup by ID
#pickup = easypost.Pickup.retrieve("pickup_...")

#Buy a pickup
#pickup.buy(carrier="UPS", service="Same-day Pickup")

#Cancel a pickupo
#pickup.cancel()

'''
Reports
A Report contains a csv that is a log of all the objects created within a certain time frame.

Reports can be generated using the Reports Endpoint. You can create and view Reports created between any time frame defined between the start_date and end_date.

The Report api can be categorized into several types. These types determine which EasyPost Object to produce a Report for, and should be passed as the type in our libraries:
        payment_log
        refund
        shipment
        shipment_invoice
        tracker

Report Object
attribute	            type	                        specification
id	                  string	                      Unique, begins with "cfrep_" (Cash Flow Report), "plrep_" (Payment Log Report), "refrep_" (Refund Report), 
                                                    "shprep_" (Shipment Report), "shpinvrep_" (Shipment Invoice Report), or "trkrep_" (Tracker Report)
object	              string	                      "CashFlowReport", "PaymentLogReport", "RefundReport", "ShipmentReport", "ShipmentInvoiceReport", or "TrackerReport"
mode	                string	                      "test" or "production"
status	              string	                      "new", "available", "failed", or null
start_date	          string	                      A date string in YYYY-MM-DD form eg: "2016-02-02"
end_date	            string	                      A date string in YYYY-MM-DD form eg: "2016-02-03"
include_children	    boolean	                      Set true if you would like to include Refunds /Shipments /Trackers created by child users
url	                  string	                      A url that contains a link to the Report. Expires 30 seconds after retrieving this object
url_expires_at	      datetime                  	  Url expiring time
send_email	          boolean	                      Set true if you would like to send an email containing the Report
created_at	          datetime	
updated_at	          datetime	
'''

'''
Create a Report
To create a Report, provide a start_date and end_date that are less than 31 days apart along with any other optional parameter that you would like to specify. A detailed list of Report Object attributes are provided below.

The expiry on url is 30 seconds. The default status on each new Report is "new". It changes to "available" if the csv file is created successfully or to "failed" when csv creation is unsuccessful. Additionally, null could also be a status.

When a Report's status changes, a webhook will be created. See our Webhooks Guide for help on Event handling.

Report Regeneration
A Report will regenerate if new shipments or payment logs are created after the Report is generated the first time (i.e end_date is later than or same as the Report updated date). You will receive an error if consecutive requests are made to create a Report. This does not hold true for tracker Reports as it is set to always regenerate each time a request is placed.

Create Report Request Parameters
param	              example
start_date	        2016-11-02
end_date	          2016-12-02
send_email	        true
'''

#Creating example reports
'''
payment_log_report = easypost.Report.create(
  start_date="2016-10-01",
  end_date="2016-10-31",
  type="payment_log"
)

refund_report = easypost.Report.create(
  start_date="2016-10-01",
  end_date="2016-10-31",
  type="refund"
)

shipment_report = easypost.Report.create(
  start_date="2016-10-01",
  end_date="2016-10-31",
  type="shipment"
)

tracker_report = easypost.Report.create(
  start_date="2016-10-01",
  end_date="2016-10-31",
  type="tracker"
)
'''

'''
Retrieve a list of Reports
The Report List is a paginated list of all Report objects associated with the given API Key. It accepts a variety of parameters which can be used to modify the scope. The has_more attribute indicates whether or not additional pages can be requested. The recommended way of paginating is to use either the before_id or after_id parameter to specify where the next page begins.

Retrieve a list of Report Request Parameters
param	          example
start_date	    2016-01-02	                  Only return Reports created after this date. Report range defaults to 30 days from this date if end_date isn't passed
end_date	      2016-01-31	                  Only return Reports created before this date. Report range defaults to 30 days before this date if start_date isn't 
                                              passed
before_id	      shprep_c8e0edb5efebb28	      Optional pagination parameter. Only Reports created before the given ID will be included. May not be used with after_id
after_id	      shprep_c8e0edbz5zebb4c	      Optional pagination parameter. Only Reports created after the given ID will be included. May not be used with before_id
page_size	      30	                          The number of Reports to return on each page. The maximum value is 100
'''

#Example of retrieving a list of reports
'''
payment_log_reports = easypost.Report.all(
    type='payment_log',
    page_size=4,
    start_date='2016-01-02'
)

refund_reports = easypost.Report.all(
    type='refund',
    page_size=4,
    start_date='2016-01-02'
)

shipment_reports = easypost.Report.all(
    type='shipment',
    page_size=4,
    start_date='2016-01-02'
)

tracker_reports = easypost.Report.all(
    type='tracker',
    page_size=4,
    start_date='2016-01-02'
)
'''

#Retrieve a report by ID
'''
payment_log_report = easypost.Report.retrieve(
  public_id="plrep_..."
)

refund_report = easypost.Report.retrieve(
  public_id="refrep_..."
)

shipment_report = easypost.Report.retrieve(
  public_id="shprep_..."
)

tracker_report = easypost.Report.retrieve(
  public_id="trkrep_..."
)
'''

'''
ScanForms
A ScanForm can be created to speed up and simplify the carrier pickup process. The ScanForm is one document that can be scanned to mark all included tracking codes as "Accepted for Shipment" by the carrier. The following criteria must met before creation:

    Refunded Shipments cannot be added
    Each Shipment must have the same origin address
    Shipments must all be dated (using the label_date option) on or after the date the form is generated
    Shipments cannot be added to more than one ScanForm
    Existing ScanForms may not be updated with additional Shipments. If a ScanForm already exists, and new Shipments need to be added, a new ScanForm must be created.
    Shipments should be provided in the form of an array

ScanForm Object
attribute	                type	                    specification
id	                      string	                    Unique, begins with "sf_"
object	                  string	                    "ScanForm"
status	                  string	                    Current status. Possible values are "creating", "created" and "failed"
message	                  string	                    Human readable message explaining any failures
address	                  Address	                    Address that the Shipments will be shipped from
tracking_codes	          string array	              Tracking codes included on the ScanForm
form_url	                string	                    Url of the document
form_file_type	          string	                    File format of the document
batch_id	                string	                    The id of the associated Batch. Unique, starts with "batch_"
created_at	              datetime	
updated_at	              datetime	
'''
'''
Create a ScanForm
A ScanForm can be created in two ways:

Add Shipments to a Batch and create a ScanForm for a Batch of Shipments
Create a scan-form for shipments directly without adding shipments to a batch

Note: A Batch is created in the background for Shipments as an intermediate process to creating ScanForms. You can create a ScanForm for 1 or a group of Shipments.

Create ScanForm Request Parameters
param	          example
shipments	      [<Shipment>,<Shipment>,...]
'''

#Creating a scanform
'''
scan_form = easypost.ScanForm.create(
  shipments=[shipment]
)
'''

'''
Retrieve a list of ScanForms
The ScanForm List is a paginated list of all ScanForm objects associated with the given API Key. It accepts a variety of parameters which can be used to modify the scope. The has_more attribute indicates whether or not additional pages can be requested. The recommended way of paginating is to use either the before_id or after_id parameter to specify where the next page begins.

Retrieve a list of ScanForms Request Parameters
param	                  example	                  info
before_id	              sf_...	              Optional pagination parameter. Only ScanForms created before the given ID will be included. May not be used with after_id
after_id	              sf_...	              Optional pagination parameter. Only ScanForms created after the given ID will be included. May not be used with before_id
start_datetime	        2016-01-02T00:00:00Z	Only return ScanForms created after this timestamp. Defaults to 1 month ago, or 1 month before a passed end_datetime
end_datetime	          2016-01-02T00:00:00Z	Only return ScanForms created before this timestamp. Defaults to end of the current day, or 1 month after a passed 
                                              start_datetime
page_size	              20	                  The number of ScanForms to return on each page. The maximum value is 100
'''

#Retrieve a list of scanforms
#scan_forms = easypost.ScanForm.all(page_size=2)

#Retrieve a scanform by ID
#scan_form = easypost.ScanForm.retrieve("sf_...")

'''
Webhooks
Each Webhook contains the url which EasyPost will notify whenever an object in our system updates. Several types of objects are processed asynchronously in the EasyPost system, so whenever an object updates, an Event is sent via HTTP POST to each configured webhook URL. The Webhook object provides CRUD operations for all Webhooks.

Currently, our recommended best practice for securing Webhooks involves using basic authentication and HTTPS on your endpoint. This will help prevent any altering of any information communicated to you by EasyPost, prevent any third parties from seeing your webhooks in transit, and will prevent any third parties from masquerading as EasyPost and sending fraudulent data. EasyPost performs certificate validation and requires any TLS-enabled (HTTPS) webhook recipients to have a certificate signed by a public trusted certification authority. We do not support sending webhooks to over SSLv2, SSLv3, or any connection using so-called export-grade ciphers. For documentation on how to set up your server with TLS, we recommend Mozilla's guide to Server-Side TLS and Qualys's SSL/TLS deployment best practices guide.

In general, a Webhook's endpoint should return a status code of 2XX. A 200 is preferred, but any 2XX status will indicate to our system that the Webhook request was successful. Endpoints that return a large volume and rate of failures over a period of time will get automatically disabled by the system; a disabled Webhook can be re-enabled using the Webhook update endpoint.

Webhook Object
attribute	                  type	                  specification
id	                        string	                Unique, begins with "hook_"
object	                    string	                "Webhook"
mode	                      string	                "test" or "production"
url	                        string	                http://example.com
disabled_at	                datetime	              the timestamp at which the webhook was most recently disabled (if any)
'''

#Creating a webhook
#webhook = easypost.Webhook.create(url="example.com")

#Retrieve a list of webhooks
#webhooks = easypost.Webhook.all()

#Retrieve a webhook by ID
#webhook = easypost.Webhook.retrieve("hook_...")

#Update a webhook
#webhook.update()

#Delete a webhook
#webhook.delete()

