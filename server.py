from flask import Flask, Response

class EndpointResponse:

	def __init__(self, response):
		self.response = response

	def __call__(self, *args):
		return self.response

class Server:

	def __init__(self, name):
		self.app = Flask(name)

	def run(self):
		# todo add port constructor 
		self.app.run(host='0.0.0.0', port=80)

	def add_endpoint(self, endpoint, endpointName, response):
		self.app.add_url_rule(endpoint, endpointName, EndpointResponse(response))

