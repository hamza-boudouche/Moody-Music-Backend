import yagmail
import os
from dotenv import load_dotenv, find_dotenv
from app import cache
from app.utils import AWAITING_CONFIRMATION, CACHE_TIMEOUT

load_dotenv(find_dotenv())
redis_host = os.environ.get("REDIS_HOST")

def send_mail(mail, subject, contents):
	try:
		yag = yagmail.SMTP(user=os.environ.get("EMAIL"), password=os.environ.get('EMAILPASSWORD'))
		yag.send(to=mail, subject=subject, content=contents)
		return True
	except:
		return False

def template_validate_email(user, token):
	#TODO: create email template with html
	pass

def cache_mail(mail):
	cache.set(mail, AWAITING_CONFIRMATION, CACHE_TIMEOUT)

def validate_cached_mail(mail):
	res = cache.get(mail) == AWAITING_CONFIRMATION
	if res:
		cache.delete(mail)
	return res
