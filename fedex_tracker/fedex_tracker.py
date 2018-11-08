import xml.etree.ElementTree as ET
import requests

KEY, PASSWORD, ACC_NUMBER, MET_NUMBER  = open("sec.txt").read().splitlines()
TEMPLATE = ET.parse("template.xml")

def fedex_tracker(tracking_number):
    request = TEMPLATE
    root = request.getroot()
    root[1][0][0][0][0].text = root[1][0][0][1][0].text = KEY
    root[1][0][0][0][1].text = root[1][0][0][1][1].text = PASSWORD
    root[1][0][1][0].text = ACC_NUMBER
    root[1][0][1][1].text = MET_NUMBER
    root[1][0][4][1][1].text = str(tracking_number)
    xml = ET.tostring(root)
    headers = {'Content-Type': 'application/xml'}
    url = ""
    xml_reply = requests.post('url', data=xml, headers=headers).text
    return 