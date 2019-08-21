from ruamel import yaml
from socket import socket
from argparse import ArgumentParser
import json
import datetime
parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Please set config file'
)

args = parser.parse_args()

host = 'localhost'
port = 8001

if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host', host)
        port = config.get('port', port)

sock = socket()
sock.connect((host, port))

print(f'CLient was started')

action = input('Enter action: ')
data = input('Enter message: ')

request = {
    'action': action,
    'data': data,
    'time': datetime.datetime.now().timestamp()
}

s_request = json.dumps(request)

sock.send(s_request.encode())
print(f'Client send  {data}')
b_response = sock.recv(1024)
print(b_response.decode())