#!/usr/bin/python
from requests import get
import string
import requests


def main(doc1, doc2):
	sss_url = "http://swoogle.umbc.edu/StsService/GetStsSim"
	doc2List = doc2.split("\n^",1)
	doc2 = doc2List[0]
	doc2 = filter(lambda x: x in string.printable, doc2)
	try:
		s = requests.Session()
		s.mount("http://", requests.adapters.HTTPAdapter(max_retries=5))
		s.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
		response = s.get(sss_url, params={'operation':'api', 'phrase1':doc1, 'phrase2': doc2, 'type': '0'})
		return float(response.text.strip())
	except:
		return float(0.0)
	
