#!/usr/bin/python
import requests
import sys
import csv
import re
import logging
import ConfigParser
import xml.etree.ElementTree as ET


"""
	Creates new user_identier node, with old primary ID value
"""
def addidentifier(xml,primary_id,new_id_type):
	ids = xml.findall("user_identifiers")[0]
	id = ET.Element("user_identifier")
	id.set("segment_type","External")
	id_type = ET.SubElement(id,"id_type")
	id_type.text = new_id_type
	id_type.set('desc','Additional ID 3')
	value = ET.SubElement(id,"value")
	value.text = primary_id
	status = ET.SubElement(id,"status")
	status.text = "ACTIVE"
	ids.append(id)
	return xml	 
	
"""
	Removes all user roles from the user record, so that existing issues with user roles don't prevent the user commit
"""	
def removeroles(patron):
	for user_roles in patron.findall("user_roles"):
		patron.remove(user_roles)
	return patron

# Read campus parameters
logging.basicConfig(filename='status.log',level=logging.DEBUG)

config = ConfigParser.RawConfigParser()
config.read(sys.argv[3])
apikey = config.get('Params', 'apikey')
baseurl = config.get('Params','baseurl')
campuscode =  config.get('Params', 'campuscode')
id_type_to_swap = config.get('Params', 'id_type_to_swap')
new_id_type = config.get('Params','new_id_type')

limit = 1
offset = sys.argv[1]
total_patrons = sys.argv[2] # always 5000



for i in range(0,int(total_patrons)):
	if i % limit == 0: # Now we want to increment i by 100
		i += limit
	url = baseurl + '/almaws/v1/users?apikey=' + apikey + '&limit=' + str(limit) + '&offset=' + str(offset) # get batch of 100 users 
	response = requests.get(url)
	rstatus = response.status_code
	if rstatus == 200:
		users = ET.fromstring(response.content)
		for user in users:
		swap = False
		primary_id = user.find('primary_id').text

		if len(primary_id) > 0  and not re.search('[ ;%&$#]', primary_id):
			user_url = baseurl + '/almaws/v1/users/' + primary_id + '?apikey=' + apikey;
			print user_url
			response = requests.get(user_url);
			patron = ET.fromstring(response.content)
			for ids in patron.findall("user_identifiers"):
				# only swap when there is one possible ID of the swap type
				count = len(ids.findall("./user_identifier/[id_type='"+id_type_to_swap+"']"))
				if ids is not None and count == 1: 
					for id in ids:
						if id.find('id_type').text == id_type_to_swap:
							new_primary = id.find('value').text
							print new_primary
							ids.remove(id)
							swap = True
			if swap == True:
				#put
				headers = {"Content-Type": "application/xml"}
				patron = removeroles(patron)
				r = requests.put(user_url,data=ET.tostring(patron),headers=headers)
				if r.status_code == 200:
					# update primary ID
					response = requests.get(user_url)
					updated_user = ET.fromstring(response.content)
					updated_user.find('primary_id').text = new_primary
					#put
					updated_user = removeroles(updated_user)
					r = requests.put(user_url,data=ET.tostring(updated_user),headers=headers)
					if r.status_code == 200:
						# Add new additional ID value 
						new_url = baseurl + '/almaws/v1/users/' + new_primary + '?apikey=' + apikey;
						response = requests.get(new_url)
						final_user = ET.fromstring(response.content)
						final = addidentifier(final_user,primary_id,new_id_type)
						final = removeroles(final)
						r = requests.put(new_url,data=ET.tostring(final),headers=headers)
						logging.info('Successful id swap for old id:' + primary_id + ', new primary: ' + new_primary)
					else:
						logging.info('Failed to replace primary id for:' + primary_id + ', new id:' + new_primary)
						logging.info(r.content)
				else:
					logging.info(r.content)
	offset += limit
	







