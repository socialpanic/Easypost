<?php

require_once("../vendor/autoload.php");
\EasyPost\EasyPost::setApiKey(getenv('API_KEY'));

// Parcel: create
$params = [
    "length" => 20.2,
    "width"  => 10.9,
    "height" => 5,
    //"predefined_package" => null,
    "weight" => 14.8
];
$parcel = \EasyPost\Parcel::create($params);

$params = [
    "predefined_package" => 'SmallFlatRateBox',
    "weight"             => 38.1
];
$parcel = \EasyPost\Parcel::create($params);

// retrieve
$retrieved = \EasyPost\Parcel::retrieve($parcel->id);
print_r($retrieved);

// all
$all = \EasyPost\Parcel::all();
//print_r($all);
/*
for($i = 0, $k = count($all); $i < $k; $i++) {
  print_r(\EasyPost\Parcel::retrieve($all[$i]->id));
}
*/
