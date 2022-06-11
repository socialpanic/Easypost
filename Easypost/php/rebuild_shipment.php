<?php

require("/home/devbox/code/Easypost/Easypost/php/vendor/easypost/easypost-php/lib/easypost.php");

\EasyPost\EasyPost::setApiKey('API KEY HERE');

$data = file_get_contents("/home/devbox/conf/shipments.json", "r") or die("Unable to open shipment file!");
$shipment = json_decode($data, true);

unset($shipment["to_address"]["id"]);
unset($shipment["to_address"]["mode"]);
unset($shipment["to_address"]["updated_at"]);
unset($shipment["to_address"]["created_at"]);
unset($shipment["to_address"]["carrier_facility"]);
unset($shipment["from_address"]["id"]);
unset($shipment["from_address"]["mode"]);
unset($shipment["from_address"]["updated_at"]);
unset($shipment["from_address"]["created_at"]);
unset($shipment["from_address"]["carrier_facility"]);
unset($shipment["parcel"]["id"]);
unset($shipment["parcel"]["mode"]);
unset($shipment["parcel"]["updated_at"]);
unset($shipment["parcel"]["created_at"]);

$customs_weight = 0;
$customs = 'false';

if ($shipment["customs_info"]){
    $customs = 'true';
    unset($shipment["customs_info"]["id"]);
    unset($shipment["customs_info"]["updated_at"]);
    unset($shipment["customs_info"]["created_at"]);
    foreach ($shipment["customs_info"]["customs_items"] as $item) {
        unset($item["id"]);
        unset($item["mode"]);
        unset($item["updated_at"]);
        unset($item["created_at"]);
        if ($item["currency"] == 'None'){
            unset($item["currency"]);
        }
    }
}

$resp = \EasyPost\Shipment::create(array(
    "to_address" => $shipment["to_address"],
    "from_address" => $shipment["from_address"],
    "parcel" => $shipment["parcel"],
    "customs_info" => $shipment["customs_info"],
    "options" => $shipment["options"]
  ));

foreach ($resp["rates"] as $rate) {
    echo "ID: ". $rate["id"]."\n";
    echo "CARRIER: ". $rate["carrier"]."\n";
    echo "SERVICE: ". $rate["service"]."\n";
    echo "RATE: ". $rate["rate"]."\n";
    echo "*******************************\n";
}

if ($resp["messages"]){
    foreach ($resp["messages"] as $msg) {
        echo "CARRIER: ". $msg["carrier"]."\n";
        echo "MESSAGE: ". $msg["message"]."\n";
        echo "*******************************\n";
    }
}


$buyoption = (int)readline("1) To purchase cheapest rate, 2) to purchase by rate ID 3) to purchase with carrier and service 4) to EXIT: ");
if ($buyoption == 1){
    $purchase = $resp ->buy(array('rate'=> $resp->lowest_rate()));
}

if ($buyoption == 2){
    $rateid = (string)readline("Enter rate_id: ");
    $purchase = $resp->buy(array('rate' => array('id' => $rateid)));
}

if ($buyoption == 3){
    $carrier = (string)readline("CARRIER: ");
    $service = (string)readline("SERVICE: ");
    $purchase = $resp->buy($resp->lowest_rate(array($carrier), array($service)));
}

if ($buyoption == 4){
    exit();
}

echo "Selected Rate: ". $purchase["selected_rate"]["id"]."\n";
echo "Carrier: ". $purchase["selected_rate"]["carrier"]."\n";
echo "Service: ". $purchase["selected_rate"]["service"]."\n";
echo "Rate: ". $purchase["selected_rate"]["rate"]."\n";
echo "Label: ". $purchase["postage_label"]["label_url"]."\n";
echo "Tracking: ". $purchase["tracking_code"]."\n";

?>