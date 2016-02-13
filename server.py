from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from dateutil.relativedelta import relativedelta
import requests, datetime, json, re, time

class GroupRequestHandler(BaseHTTPRequestHandler):

    group_id    = '19764573' 
    dario_bot   = '9af5b2ffe7a277e4f9f108f8f7'
    base_url    = 'https://api.groupme.com/v3'
    dario_token = '9dae11a0b4b50133affd089a73c6b9e5'

    def do_POST(self):


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
                response['bot_id'] = self.dario_bot 
                requests.post(base_url + '/bots/post', data=response)

            if re.search("not no", json_request['text'].lower(), flags = 0):

                # say a message
                response = { }
                response['text'] = "You're the worst. You need a timeout"
                response['bot_id'] = self.dario_bot
                requests.post(self.base_url + '/bots/post', data=response)

                # remove the person
                sender_id = json_request['sender_id']
                self.remove(sender_id, None)
                time.sleep(10)

                # add the person back with a dumb name
                self.add(sender_id, "Silly Silly")
                print response

            statement = re.search('banish (\w+) for (\d+)', json_request['text'].lower())
            if statement:
                # remove the person

                # wait for appropriate amount of time
                sleep(int(statement.group(2)))

                # add the person back

    def remove(self, sender_id, name):

        group_info = requests.get(self.base_url + '/groups/' + self.group_id + \
                                  '?token=' + self.dario_token).json()
        if sender_id:

            for member in group_info['response']['members']:
                if member['user_id'] == sender_id:
                    remove_id = member['id']

        elif name:
           
           for member in group_info['response']['members']:
               if member['nickname'] == name:
                   remove_id = member['id']

        url = self.base_url + '/groups/' + \
              self.group_id + '/members/' + \
              remove_id + '/remove?token=' + \
              self.dario_token
      
        response = requests.post(url)

    def add(self, user_id, nickname):

        url = self.base_url + '/groups/' + \
              self.group_id + '/members/add?token=' + \
              self.dario_token

        person = {'nickname': nickname, 'user_id': str(user_id)}
        data   = {'members': [person]}

        response = requests.post(url, data=json.dumps(data))
        

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
