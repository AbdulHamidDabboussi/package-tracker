import xml.etree.ElementTree as ET
import requests

KEY, PASSWORD, ACC_NUMBER, MET_NUMBER  = open("sec.txt").read().splitlines()
TEMPLATE = ET.parse("template.xml")