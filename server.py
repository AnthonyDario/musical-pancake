from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import requests
import json
from dateutil.relativedelta import relativedelta
import datetime

class GroupRequestHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		post_url = 'https://api.groupme.com/v3/bots/post'
		length = int(self.headers['Content-Length'])
		request = self.rfile.read(length)
		print(request)
		json_request = json.loads(request)
		if json_request['sender_type'] == 'user' and \
		   json_request['text'].lower().strip().replace(".", "") == 'spring break':

			today = datetime.datetime.today()
			rd = relativedelta(datetime.datetime(2016, 3, 5, 0, 0, 0, 0), today)
			response = { }
			response['text'] = str(rd.months) + ' months ' + str(rd.days) + ' days ' + str(rd.hours) + ' hours ' + str(rd.minutes) + ' minutes ' + str(rd.seconds) + ' seconds'
			response['bot_id'] = '26d1e43f3942fcab2aa1cc68b1'
			requests.post(post_url, data=response)

#request = requests.get('https://api.groupme.com/v3/groups/:group_id/likes?period=<day|week|month>')
token = "5f22d5a0b4ba0133affd089a73c6b9e5"
request = requests.get('https://api.groupme.com/v3/groups?token=' + token)
print(request)


# hosting the server
HandlerClass = SimpleHTTPRequestHandler
protocol     = 'HTTP/1.0'

HandlerClass.protocol_version = protocol
port_number = 55555
server_address = ('129.22.150.55', port_number)
httpd = HTTPServer(server_address, GroupRequestHandler)
print('http server is starting')

print('http server is runnning on 129.22.150.55:{value}'.format(value=port_number))
httpd.serve_forever()
