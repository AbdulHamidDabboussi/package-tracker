"""
ups_tracker:

Tracks UPS pacakages using credentials in sec.txt file.
"""

from json import load, dumps
from requests import post

def json_generator(tracking_number):
    """
    Generates request JSON using the auth info in sec.text and the tracking
    number. 
    """
    template = load(open("template.json", "r"))
    user, password, license_key = open("sec.txt").read().splitlines()

    request = template
    request["UPSSecurity"]["UsernameToken"]["Username"] = user
    request["UPSSecurity"]["UsernameToken"]["Password"] = password
    request["UPSSecurity"]["ServiceAccessToken"]["AccessLicenseNumber"] = license_key
    request["TrackRequest"]["InquiryNumber"] = tracking_number

    return request

def ups_response_parser(response):
    """
    Parses JSON response from ups_tracker().

    If the response is faulty, it will return an error code and description.
    Otherwise, it will return the shipper address, ship-to address, status
    of the delivery (code, description, location).
    """
    if "Fault" in response:
        error = response['Fault']['detail']['Errors']['ErrorDetail']['PrimaryErrorCode']
        return {
            "RESPONSE": False,
            "ERROR_CODE": error['Code'],
            "ERROR_DESCRIPTION": error['Description']}

    package = response["TrackResponse"]["Shipment"]["Package"]
    shipment_address = response["TrackResponse"]["Shipment"]["ShipmentAddress"]

    return {
        "RESPONSE": True,
        "TRACKING_NUMBER": package["TrackingNumber"],
        "SHIPPER_ADDRESS": {
            "CITY": shipment_address[0]["Address"]["City"],
            "STATE": shipment_address[0]["Address"]["StateProvinceCode"],
            "POSTAL_CODE": shipment_address[0]["Address"]["PostalCode"],
            "COUNTRY_CODE": shipment_address[0]["Address"]["CountryCode"]},
        "SHIPTO_ADDRESS": {
            "CITY": shipment_address[1]["Address"]["City"],
            "STATE":shipment_address[1]["Address"]["StateProvinceCode"],
            "POSTAL_CODE": shipment_address[1]["Address"]["PostalCode"],
            "COUNTRY_CODE": shipment_address[1]["Address"]["CountryCode"]
        },
        "STATUS": {
            "CODE": package["Activity"][0]["Status"]["Type"],
            "DESCRIPTION": package["Activity"][0]["Status"]["Description"],
            "LOCATION": {
                "CITY": package["Activity"][0]["ActivityLocation"]["Address"]["City"],
                "STATE": package["Activity"][0]["ActivityLocation"]["Address"]["StateProvinceCode"],
                "POSTAL_CODE": package["Activity"][0]["ActivityLocation"]["Address"]["PostalCode"],
                "COUNTRY_CODE": package["Activity"][0]["ActivityLocation"]["Address"]["CountryCode"]
            }
        }
    }

def ups_tracker(tracking_number):
    """
    Uses json_generator to generate request, sends it, then parses response 
    using ups_response_parser()
    """
    request = json_generator(tracking_number)

    url = "https://onlinetools.ups.com/rest/Track"
    response = post(url, data=dumps(request)).json()

    return ups_response_parser(response)
