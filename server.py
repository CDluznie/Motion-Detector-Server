from flask import Flask, Response

class EndpointResponse:

	def __init__(self, response):
		self.response = response

	def __call__(self, *args):
		return self.response

class Server:

	def __init__(self, name, port):
		self.app = Flask(name)
		self.port = port

	def run(self):
		self.app.run(host='0.0.0.0', port=self.port)

	def add_endpoint(self, endpoint, endpointName, response):
		self.app.add_url_rule(endpoint, endpointName, EndpointResponse(response))

