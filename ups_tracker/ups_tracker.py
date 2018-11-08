import json
import requests
from pprint import pprint

TEMPLATE = json.load(open("template.json"))
USER, PASSWORD, LICENSE = open("sec.txt").read().splitlines()
URL = "https://onlinetools.ups.com/rest/Track"

def ups_tracker(tracking_number):
    request = TEMPLATE
    request["UPSSecurity"]["UsernameToken"]["Username"] = USER
    request["UPSSecurity"]["UsernameToken"]["Password"] = PASSWORD
    request["UPSSecurity"]["ServiceAccessToken"]["AccessLicenseNumber"] = LICENSE
    request["TrackRequest"]["InquiryNumber"] = tracking_number

    r = requests.post(URL, data=json.dumps(request))

    response = r.json()

    if "Fault" in response:
        return {"RESPONSE": False, 
                "ERROR_CODE": response['Fault']['detail']['Errors']['ErrorDetail']['PrimaryErrorCode']['Code'],
                "ERROR_DESCRIPTION": response['Fault']['detail']['Errors']['ErrorDetail']['PrimaryErrorCode']['Description']}
    
    return {
                "TRACKING_NUMBER": tracking_number,
                "SHIPPER_ADDRESS": response["TrackResponse"]["Shipment"]["ShipmentAddress"][0]["Address"],
                "SHIPTO_ADDRESS": 
                    {"CITY": response["TrackResponse"]["Shipment"]["ShipmentAddress"][1]["Address"]["City"],
                    "STATE":response["TrackResponse"]["Shipment"]["ShipmentAddress"][1]["Address"]["StateProvinceCode"],
                    "POSTAL_CODE": response["TrackResponse"]["Shipment"]["ShipmentAddress"][1]["Address"]["PostalCode"],
                    "COUNTRY_CODE": response["TrackResponse"]["Shipment"]["ShipmentAddress"][1]["Address"]["CountryCode"]}
                "STATUS": 
                {
                    "CODE": response["TrackResponse"]["Shipment"]["Package"]["Activity"]["Status"]["Type"],
                    "DESCRIPTION": response["TrackResponse"]["Shipment"]["Package"]["Activity"]["Status"]["Description"]}
    }

pprint(ups_tracker("1Z1A97Y80323171528"))