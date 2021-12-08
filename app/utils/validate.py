import requests
import math
import re

def validate_link(url):
	response = requests.get(url)
	if math.floor(response.status_code/100) in [1, 2, 3]:
		return True
	return False

def validate_email_form(email):
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	return re.fullmatch(regex, email)
