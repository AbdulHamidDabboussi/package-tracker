"""
usps_tracker

Tracks USPS pacakages.
"""
import xml.etree.ElementTree as ET
import requests

def make_template(tracking_number):
    """
    Generates XML template necessary for request.
    Contains:
        * username (from sec.txt)
        * tracking number (input)
    """
    template = open("template.xml", "r").read()

    user = open("sec.txt").read().splitlines()[0]

    template = template.format(user, tracking_number)

    return template

def usps_response_parser(response):
    """
    Parses the response received from USPS.
    Returns a dictionary with tracking and number and status, USPS isn't fancy.
    """
    response_xml = ET.fromstring(response)

    return {
        "TRACKING_NUMBER": response_xml[0].attrib['ID'],
        "STATUS": response_xml[0][0].text
    }

def usps_tracker(tracking_number):
    """
    Tracks USPS package. Uses make_template to generate XML request and then
    parses it using usps_response_parser.
    """
    request_xml = make_template(tracking_number)

    url = f"https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML={request_xml}"

    response = requests.post(url).text

    return usps_response_parser(response)
