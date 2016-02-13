from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import requests
import json
from dateutil.relativedelta import relativedelta
import datetime

class GroupRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        dario_bot = '9af5b2ffe7a277e4f9f108f8f7'
        post_url = 'https://api.groupme.com/v3/bots/post'

        length = int(self.headers['Content-Length'])
        request = self.rfile.read(length)
        json_request = json.loads(request)

        if json_request['sender_type'] == 'user':

            if json_request['text'].lower().strip().replace(".", "") == 'spring break':

                today = datetime.datetime.today()
                rd = relativedelta(datetime.datetime(2016, 3, 5, 0, 0, 0, 0), today)
                response = { }
                response['text'] = str(rd.months)  + ' months ' + \
                                   str(rd.days)    + ' days ' + \
                                   str(rd.hours)   + ' hours ' + \
                                   str(rd.minutes) + ' minutes ' + \
                                   str(rd.seconds) + ' seconds'
                response['bot_id'] = dario_bot 
                requests.post(post_url, data=response)

            if re.search("not no", json_request['text'], flags = 0):
                response = { }
                response['text'] = "not no = yes"
                response['bot_id'] = dario_bot
                requests.post(post_url, data=response)


# hosting the server
HandlerClass = SimpleHTTPRequestHandler
protocol     = 'HTTP/1.0'

HandlerClass.protocol_version = protocol
port_number = 54322
server_address = ('129.22.150.55', port_number)
httpd = HTTPServer(server_address, GroupRequestHandler)
print('http server is starting')

print('http server is runnning on 129.22.150.55:{value}'.format(value=port_number))
httpd.serve_forever()
