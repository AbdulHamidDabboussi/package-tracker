"""
usps_tracker

Tracks USPS pacakages.
"""
import requests

def make_template(tracking_number):
    template = open("template.xml","r").read()

    user = open("sec.txt").read().splitlines()[0]

    template = template.format(user, tracking_number)

    return template

def usps_tracker(tracking_number):
    request_xml = make_template(tracking_number)
    
    url = f"https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML={request_xml}"

    request = requests.post(url)

    return request.text
