#!/usr/bin/python
import requests
import sys
import csv
import ConfigParser
import xml.etree.ElementTree as ET


# Read campus parameters
config = ConfigParser.RawConfigParser()
config.read(sys.argv[1])
apikey = config.get('Params', 'apikey')
baseurl = config.get('Params','baseurl')
campuscode =  config.get('Params', 'campuscode')
id_type_to_swap = config.get('Params', 'id_type_to_swap')
new_id_type = config.get('Params','new_id_type')

# CSV file of items to be checked in
items_file = sys.argv[2]
query = '?op=scan' + '&library=' + library + '&circ_desk=' + circdesk


f = open(items_file, 'rt')
try:
    reader = csv.reader(f)
    reader.next() #skip header line
    for row in reader:
    	if row[0] != 'end-of-file':
			apicall = createurl(row)
			url =  baseurl + apicall + query
			print url
			response = requests.post(url, data={'apikey' : apikey})
			print response.content
finally:
    f.close()
	







