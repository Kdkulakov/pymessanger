from ruamel import yaml
import json
import logging
import os
from socket import socket
from argparse import ArgumentParser

from protocol import validate_request, make_response
from resolvers import resolver

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8001,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

host, port = (default_config.get('host'), default_config.get('port'))

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

LOGS_DIR = os.path.exists(os.path.dirname('./logs'))

if not LOGS_DIR:
    os.makedirs('logs')

handler = logging.FileHandler('logs/main.log')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


try:
    try:
        sock = socket()
        sock.bind((host, port,))
        sock.listen(5)
    except Exception as err:
        print("ERRORO in bind server port: " + str(err))
        logger.info(f'ERRORO in bind server port: {str(err)}')

    logger.info(f'Server was started with {host}:{port}')
    print(f'Server was started with {host}:{port}')

    while True:
        try:
            client, address = sock.accept()
            logger.info(f'Clietn was connected with {address[0]}:{address[1]}')
        except Exception as err:
            print("Error: " + str(err))
            break

        b_request = client.recv(default_config.get('buffersize'))
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolver(action_name)
            if controller:
                try:
                    logger.debug(f'Controller {action_name} resolved with request: {request}')

                    response = controller(request)
                except Exception as err:
                    logger.critical(f'Controller {action_name} error: {err}')
                    response = make_response(request, 500, 'Internal server error')
            else:
                logger.error(f'Controller {action_name} not found')

                response = make_response(request, 404, f'Action with name {action_name} not supported')
        else:
            logger.error(f'Controller wrong request: {request}')

            response = make_response(request, 400, 'wrong request format')

        client.send(
            json.dumps(response).encode()
        )

        client.close()

except KeyboardInterrupt:
    logger.info('Server shutdown')
    print('Server shutdown')