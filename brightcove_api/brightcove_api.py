import time

import requests
import base64

from helpers import tidy_dates, handle_leap_year, month_days, get_yesterday_string, get_end_of_last_month

ENDPOINTS_DATA = {		
}

class StatInvalidEndpoint(Exception):
	pass	


class StatRequestError(Exception):
	pass


class StatResponseError(Exception):
	pass


class InvalidParameters(Exception):
	pass


class StatTimeoutException(Exception):
	pass


class Brightcove(object):
	""" An object for getting data from the Brightcove API"""

	def __init__(self, client_id, client_secret):

		self.base_url = self._make_base_url()
		self.client_id = client_id
		self.client_secret = client_secret
		self.access_token = None
		self.access_expiration = None

	def _make_base_url(self):
		return "https://analytics.api.brightcove.com"

	def _make_api_request_url(self, endpoint):
		return self.base_url + endpoint

	def _do_request(self, url, **kwargs):
		if (not (self.access_token and self.access_expiration > time.time())):
			self._login()

		headers = {"Authorization":"Bearer "+ self.access_token}
		r = requests.get(url, params=kwargs['data'], headers=headers)
		status_code = r.status_code
		if status_code == 400:
			raise StatRequestError("Bad request")
		elif status_code == 401:
			print(r.request.headers)
			print(r.request.url)
			raise StatRequestError("Unauthorized API key")
		elif status_code == 403:
			raise StatRequestError("Usage Limit Exceeded")
		elif status_code == 404:
			raise StatRequestError("Not Found")
		elif status_code == 500:
			raise StatRequestError("Internal Server Error")	
		response_data = r.json()	
		return response_data

	def _login(self):

		url = "https://oauth.brightcove.com/v4/access_token"

		authstring = self.client_id + ":" + self.client_secret
		authstring = base64.b64encode(authstring)

		headers = {
			"Authorization":"Basic " + authstring,
			"Content-Type":"application/x-www-form-urlencoded"
		}

		data = (('grant_type',"client_credentials"),)

		r = requests.post(url, headers=headers, data=data)

		status_code = r.status_code
		if status_code == 400:
			raise StatRequestError("Bad request")
		elif status_code == 401:
			raise StatRequestError("Unauthorized API key")
		elif status_code == 403:
			raise StatRequestError("Usage Limit Exceeded")
		elif status_code == 404:
			raise StatRequestError("Not Found")
		elif status_code == 500:
			raise StatRequestError("Internal Server Error")

		response_data = r.json()

		if 'access_token' not in response_data or 'expires_in' not in response_data:
			raise StatResponseError(response_data)

		self.access_expiration = time.time() + (int(response_data['expires_in']) - 5)
		self.access_token = response_data['access_token']

	def get_video_data(self, accounts, dimensions, fields, video_id, from_date, to_date=get_end_of_last_month(), **kwargs):
		if (not (self.access_token and time.time() < self.access_expiration)):
			self._login()

		endpoint = "/v1/data"

		data=(("accounts",accounts),
		("dimensions",dimensions),
		("fields",fields),
		("where","video=={0}".format(video_id)),
		("from",from_date),
		("to",to_date))

		url = self._make_api_request_url(endpoint)

		return self._do_request(url, data=data)