from ujson import dumps
from json_minify import json_minify

from .util import *
from httpx import Client
from .headers import Headers
from .exception import CheckExceptions

settingsDict = {
	"sid": None,
	"userId": None,
	"secret": None
}

class sessionClass(Headers):
	def __init__(self, proxies: dict = None, staticDevice: str = None):
		self.proxy = proxies
		self.staticDevice = staticDevice
		
		self.sid = settingsDict['sid']
		self.uid = settingsDict['userId']
		self.secret = settingsDict['secret']

		Headers.__init__(self, header_device = self.staticDevice)
		self.session = Client(proxies = self.proxy if self.proxy else None)

		self.deviceId = self.header_device
		if self.sid: self.updateHeaders(sid = self.sid)

	def settings(self, settingsSid: str = None, settingsUser: str = None, settingsSecret: str = None):
		settingsDict.update({
			"sid": settingsSid,
			"userId": settingsUser,
			"secret": settingsSecret
		})
		self.sid = settingsDict['sid']
		self.uid = settingsDict['userId']
		self.secret = settingsDict['secret']
		
	def postRequest(self, url: str, data: str = None, **kwargs):
		newHeaders = kwargs.get("newHeaders", None)
		webRequest = kwargs.get("web", None)
		minify = kwargs.get("minify", None)
		if newHeaders: self.app_headers.update(newHeaders)

		if not isinstance(data, str): 
			data = json_minify(dumps(data)) if minify else dumps(data)

		req = self.session.post(
				url = webApi(url) if webRequest else api(url), 
				data = data,
				headers = self.web_headers if webRequest else self.updateHeaders(data = data, sid = self.sid)
			)		
		if req.status_code != 200: return CheckExceptions(req.json())
		return req.json()
	
	def getRequest(self, url: str):
		req = self.session.get(url = api(url), headers = self.app_headers)
		if req.status_code != 200: return CheckExceptions(req.json())
		return req.json()
	
	def deleteRequest(self, url: str):
		req = self.session.delete(url = api(url), headers = self.app_headers)
		if req.status_code != 200: return CheckExceptions(req.json())
		return req.json()

