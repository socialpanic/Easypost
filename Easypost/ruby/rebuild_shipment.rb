require 'easypost'
require 'json'

EasyPost.api_key = 'EZTK9a283cc2276d4a068950bbb1cdd135bcBlydiiRGJiWOzJXdvWQ3qA'

data  = File.read('/home/devbox/Desktop/conf/shipment.json')
shipment = JSON.parse(data)

shipment["to_address"].delete("id")
shipment["to_address"].delete("mode")
shipment["to_address"].delete("updated_at")
shipment["to_address"].delete("created_at")
shipment["to_address"].delete("carrier_facility")
shipment["from_address"].delete("id")
shipment["from_address"].delete("created_at")
shipment["from_address"].delete("mode")
shipment["from_address"].delete("updated_at")
shipment["parcel"].delete("id")
shipment["parcel"].delete("created_at")
shipment["parcel"].delete("mode")
shipment["parcel"].delete("updated_at")

customs_weight = 0
customs = 'false'
if shipment["customs_info"]
    customs = 'true'
    shipment["customs_info"].delete("id")
    shipment["customs_info"].delete("created_at")
    #shipment["customs_info"].pop("mode")
    shipment["customs_info"].delete("updated_at")
    for item in shipment["customs_info"]["customs_items"] do
        customs_weight += item["weight"]
        item.delete("id")
        item.delete("created_at")
        item.delete("mode")
        item.delete("updated_at")
        if item["currency"] == 'None'
            item.delete("currency")
        end
    end
end

if shipment["tracker"]
  tracker = shipment["tracker"]["public_url"]
  puts tracker
end

newShipment = EasyPost::Shipment.create(
    :to_address => shipment['to_address'],
    :from_address => shipment['from_address'],
    :parcel => shipment['parcel'],
    :customs_info => shipment['customs_info'],
    :options => shipment['options']
  )

for rate in newShipment["rates"] do
    puts "ID: "+rate['id']
    puts "CARRIER: "+rate['carrier']
    puts "SERVICE: "+rate['service']
    puts "RATE: "+rate['rate']
    puts "******************************************"
end


if newShipment['messages']
  for msg in shipment['messages'] do
    puts "CARRIER: " + msg['carrier']
    puts "MESSGAE: " + msg['message']
    puts "******************************************"
  end
end


puts "1) To purchase cheapest rate, 2) to purchase by rate ID 3) to purchase with carrier and service 4) to EXIT: "
buyoption = gets.chomp
if buyoption == "1"
    purchase = newShipment.buy(:rate => newShipment.lowest_rate)
end
if buyoption == "2"
    puts "Enter rate_id: "
    rateid = gets.chomp
    purchase = newShipment.buy(rate: {id: rateid})
end
if buyoption == "3"
    puts "CARRIER: "
    carrier = gets.chomp
    puts "SERVICE: "
    service = gets.chomp
    purchase = newShipment.buy(rate: newShipment.lowest_rate(carriers = [carrier], services = [service]))
end
if buyoption == "4"
    abort("You have selected not to purchase this shipment")
end

puts "Selected Rate: " + purchase["selected_rate"]["id"]
puts "Carrier: " + purchase["selected_rate"]["carrier"]
puts "Service: " + purchase["selected_rate"]["service"]
puts "Rate: " + purchase["selected_rate"]["rate"]
puts "Label: " + purchase["postage_label"]["label_url"]
puts "Tracking: " + purchase["tracking_code"]
