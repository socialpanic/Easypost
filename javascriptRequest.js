import fetch from 'node-fetch'

let endpoint = "https://api.easypost.com/v2/shipments" /// Set endpoint here

let parms ={}

console.log(parms);
let response = await fetch(endpoint, {
    method: 'POST',                                  /// Set GET or POST here
    body: JSON.stringify(parms),
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + btoa('xxxxxx:')  /// API KEY HERE

    },
});
console.log(response);
