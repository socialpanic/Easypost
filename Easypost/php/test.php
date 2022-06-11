<?php

require("/home/devbox/code/Easypost/Easypost/php/vendor/easypost/easypost-php/lib/easypost.php");

\EasyPost\EasyPost::setApiKey('EZTK9a283cc2276d4a068950bbb1cdd135bcxzWxaDgVutJ0chKkdDhxyw');

$shipment = \EasyPost\Shipment::create([
    "from_address" => [
        "company" => "EasyPost",
        "street1" => "118 2nd Street",
        "street2" => "4th Floor",
        "city"    => "San Francisco",
        "state"   => "CA",
        "zip"     => "94105",
        "phone"   => "415-456-7890",
    ],
    "to_address" => [
        "name"    => "Dr. Steve Brule",
        "street1" => "179 N Harbor Dr",
        "city"    => "Redondo Beach",
        "state"   => "CA",
        "zip"     => "90277",
        "phone"   => "310-808-5243",
    ],
    "parcel" => [
        "length" => 20.2,
        "width"  => 10.9,
        "height" => 5,
        "weight" => 65.9,
    ],
]);

$shipment->buy($shipment->lowest_rate());

echo $shipment;

?>