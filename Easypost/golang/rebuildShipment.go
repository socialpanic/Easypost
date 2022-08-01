package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/EasyPost/easypost-go"
)

func main() {

	var apiKey = ""

	client := easypost.New(apiKey)
	// IMPORT FROM FILE

	JSON, err := ioutil.ReadFile("") // the file is inside the local directory
	if err != nil {
		fmt.Println("Err")
	}

	//UNMARSHAL
	var shipment easypost.Shipment      // set shipment var to Shipment struct defined in easypost import
	_ = json.Unmarshal(JSON, &shipment) // marry the JSON file with the Shipment struct via the json.UNMARSHAL

	//is order domestic or international
	var domestic = "true"
	if shipment.ToAddress.Country == shipment.FromAddress.Country {
		fmt.Println("Shipment is ", shipment.ToAddress.Country, " domestic")
	}

	if shipment.ToAddress.Country != shipment.FromAddress.Country {
		fmt.Println("Shipment is ", shipment.FromAddress.Country, " to ", shipment.ToAddress.Country)
		domestic = "false"
	}

	//verify the weight of the customers object and the parcel object
	var height, length, width, weight = 0.0, 0.0, 0.0, 0.0

	if shipment.Parcel.Height != 0 {
		height = shipment.Parcel.Height
	}

	if shipment.Parcel.Length != 0 {
		height = shipment.Parcel.Length
	}

	if shipment.Parcel.Width != 0 {
		height = shipment.Parcel.Width
	}

	if shipment.Parcel.Weight != 0 {
		height = shipment.Parcel.Weight
	}

	//girth = (length * 2) + (height * 2)

	//USPS
	if weight > 1120 && domestic == "true" {
		fmt.Println("WARNING: Parcel Weight of ", weight, " onces exceeds the 70lb threashold for most domestic USPS shipments")
	}
	//UPS
	var cubic_foot = length * width * height
	if cubic_foot > 1728 {
		var pounds = weight / 16
		fmt.Println("********************WARNING*******************************")
		fmt.Println("parcel is OVER one cubic foot and Dimensional Weight USPS may be dim weighted at ", cubic_foot/166, " lbs instead of ", pounds, " pounds.")
		fmt.Println("Other carriers may be dim weigh the parcel at ", cubic_foot/139, " lbs instead of ", pounds, " pounds.")
	}

	//form shipment

	newShipment, err := client.CreateShipment(
		&easypost.Shipment{
			ToAddress: &easypost.Address{
				Name:    shipment.ToAddress.Name,
				Street1: shipment.ToAddress.Street1,
				Street2: shipment.ToAddress.Street2,
				City:    shipment.ToAddress.City,
				State:   shipment.ToAddress.State,
				Zip:     shipment.ToAddress.Zip,
				Country: shipment.ToAddress.Country,
				Company: shipment.ToAddress.Company,
				Phone:   shipment.ToAddress.Phone,
			},
			FromAddress: &easypost.Address{
				Name:    shipment.FromAddress.Name,
				Street1: shipment.FromAddress.Street1,
				Street2: shipment.FromAddress.Street2,
				City:    shipment.FromAddress.City,
				State:   shipment.FromAddress.State,
				Zip:     shipment.FromAddress.Zip,
				Country: shipment.FromAddress.Country,
				Company: shipment.FromAddress.Company,
				Phone:   shipment.FromAddress.Phone,
			},
			Parcel: &easypost.Parcel{
				Length: shipment.Parcel.Length,
				Width:  shipment.Parcel.Width,
				Height: shipment.Parcel.Height,
				Weight: shipment.Parcel.Weight,
			},
		},
	)
	if err != nil {
		fmt.Fprintln(os.Stderr, "error creating shipment:", err)
		os.Exit(1)
		return
	}

	//return rates
	//var newShipID = newShipment.ID
	for _, rate := range newShipment.Rates {
		fmt.Println("ID: ", rate.ID)
		fmt.Println("CARRIER: ", rate.Carrier)
		fmt.Println("SERVICE: ", rate.Service)
		fmt.Println("RATE: ", rate.Rate)
		fmt.Println("****************************")
	}

	//select rate
	var rate_selection string
	fmt.Printf("Please enter a Rate ID: ")
	fmt.Scanln(&rate_selection)

	newShipment, err = client.BuyShipment(newShipment.ID, &easypost.Rate{ID: rate_selection}, "")
	if err != nil {
		fmt.Fprintln(os.Stderr, "error buying shipment:", err)
		os.Exit(1)
	}

	//return selected rate and label
	prettyJSON, err := json.MarshalIndent(newShipment.PostageLabel, "", "    ")
	fmt.Printf("%s \n", string(prettyJSON))

}
