#!/usr/bin/python
import requests
import sys
import csv
import re
import ConfigParser
import xml.etree.ElementTree as ET


# Read campus parameters
config = ConfigParser.RawConfigParser()
config.read(sys.argv[3])
apikey = config.get('Params', 'apikey')
baseurl = config.get('Params','baseurl')
campuscode =  config.get('Params', 'campuscode')
id_type_to_swap = config.get('Params', 'id_type_to_swap')
new_id_type = config.get('Params','new_id_type')

limit = 10
offset = sys.argv[1]
total_patrons = sys.argv[2] # always 5000


for i in range(0,int(total_patrons)):
	if i % limit == 0: # Now we want to increment i by 100
		i += limit
	url = baseurl + '/almaws/v1/users?apikey=' + apikey + '&limit=' + str(limit) + '&offset=' + str(offset) # get batch of 100 users 
	response = requests.get(url)
	users = ET.fromstring(response.content)
	
	for user in users:
		primary_id = user.find('primary_id').text
		if len(primary_id) > 0  and not re.search('[ ;%&$#]', primary_id):
			user_url = baseurl + '/almaws/v1/users/' + primary_id + '?apikey=' + apikey;
			response = requests.get(user_url);
			patron_xml = ET.fromstring(response.content)
			print primary_id
			for identifiers in patron_xml.findall('user_identifiers/user_identifier'):
				id_type = identifiers.find('id_type').text
				if id_type == id_type_to_swap: # check if id has the id type we want to remove
					print id_type
					# Remove ID node
				







