import yagmail
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
redis_host = os.environ.get("REDIS_HOST")

def send_mail(mail, subject, contents):
	try:
		yag = yagmail.SMTP(user=os.environ.get("EMAIL"), password=os.environ.get('EMAILPASSWORD'))
		yag.send(to=mail, subject=subject, contents=contents)
		return True
	except Exception as e:
		return False

def template_validate_email(user, token):
	#TODO: create email template with html
	from utils import URL_BASE
	return f"""Hello {user.username}
	Validate you email by clicking on the following link:
	{URL_BASE}/user/register/validate/{token}"""

def cache_mail(mail):
	from app import cache
	from app.utils import AWAITING_CONFIRMATION, CACHE_TIMEOUT
	cache.set(mail, AWAITING_CONFIRMATION)

def validate_cached_mail(mail):
	from app import cache
	from app.utils import AWAITING_CONFIRMATION, CACHE_TIMEOUT
	res = (cache.get(mail) == AWAITING_CONFIRMATION)
	if res:
		cache.delete(mail)
	return res

if __name__ == '__main__':
	print(os.environ.get("EMAIL"))
	print(os.environ.get('EMAILPASSWORD'))
	print(send_mail("boudouche.hamza.11@gmail.com", "test", "hello world"))