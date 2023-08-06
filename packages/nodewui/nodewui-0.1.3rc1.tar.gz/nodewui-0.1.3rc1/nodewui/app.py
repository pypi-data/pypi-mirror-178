#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import json
import requests
import configparser
import argparse

import cherrypy

__version__ = "0.1.3rc1"

# Default listening port
default_port = 8080

parser = argparse.ArgumentParser(
                    prog = 'NodeWUI',
                    description = 'Gets simple information from bitcoin node, provided a config file',
                    epilog = 'For more information check: https://gitlab.com/uak/nodewui/')

parser.add_argument('config_file', help='Path to bitcoin.conf file')           # positional argument
parser.add_argument('-a', '--address', help='IP address and port of this app. (e.g.: 0.0.0.0:8081 or 192.168.1.254:8085, default: 127.0.0.1:8080)  ')           # option that takes a value
parser.add_argument('-t', '--test', help='Name of the custom section  with rpc port settings (e.g.: "test4", "chipnet")')      # option that takes a value

# Store arguments in a variable
args = parser.parse_args()

# Configpraser does not recognize files without sectsions, so we add one
with open(args.config_file, 'r') as f:
    config_string = '[main]\n' + f.read()

# Use configparser to process configuration file    
config = configparser.ConfigParser()
config.read_string(config_string)


# Get rpc url from enviroment variable or use default
rpc_url = os.getenv('rpc_url', "http://127.0.0.1")

# Try to get the ip:port value from CLI argument
try:
    listening_ip, web_port = args.address.split(':')
    cherrypy.log(f"Using custom IP: {listening_ip} and port: {web_port}")
except:
    web_port = os.getenv('web_port', default_port)
    listening_ip = os.getenv('listening_ip', "127.0.0.1")
    cherrypy.log(f"Using default or ENV IP: {listening_ip} and port: {web_port}")


# Get rpc user and password from configuration file
rpc_password = config["main"]["rpcpassword"]
rpc_user = config["main"]["rpcuser"]


# If testnet is chosen and config file have that section, use it
try:
    rpc_port = config[args.test]["rpcport"]
    cherrypy.log(f"Reading RPC port {rpc_port} from {args.test} section of config file")
except:
    rpc_port = config["main"]["rpcport"]
    cherrypy.log(f"Using RPC port {rpc_port} from config file")


# Create full RPC URL from url + port
url = rpc_url + ":" + rpc_port + "/"


cherrypy.log(f"RPC URL: {url}")


# Cherrypy: Location of media dir
# ~ MEDIA_DIR = os.path.join(os.path.abspath("."), u"media")
this_dir, this_filename = os.path.split(__file__)

MEDIA_DIR = os.path.join(this_dir, u"media")



def call_rpc(payload):
    """
    Function to call RPC with a provided method
    """ 
    cherrypy.log(f"payload: {payload}")
    # Headers to be provided in requests function query
    headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
    # log headers using cherrypy log, useful for debuging
    cherrypy.log(f'headers: {headers}')
    # Try to call RPC and show exceptions if there is an issue
    try:
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=(rpc_user, rpc_password)
            )
        # The function will return the response of the request in json format
        return json.loads(response.text)
    # If there is an issue related to Request it will report request issue
    except requests.exceptions.RequestException as e:
        cherrypy.log(f"Request issue: {e}")
    # If there is an issue it will report it
    except Exception as e:
        cherrypy.log(f"Error: {e}")


class BlockchainRPC(object):
    @cherrypy.expose
    def index(self):
        """Index page of the app"""
        return open(os.path.join(MEDIA_DIR, 'index.html'))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get(self, **params):
        """
        Construct payload from provided method in json format 
        """
        if not params.get("params"):
            _params = []
            cherrypy.log("empty parameters list")
        elif type(params.get("params")) != list:
            _params = [params.get("params")]
            cherrypy.log("type is not list")
        else:
            _params = params.get("params")
            cherrypy.log("anything else")
        payload = json.dumps({"method": params["method"], "params": _params}) # have the method in 
        cherrypy.log(payload)
        return call_rpc(payload)     


config = {
    'media':
        {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': MEDIA_DIR,
        },
}

# Option to set the port of the server
cherrypy.config.update(
        {
        'server.socket_port': int(web_port),
        # ~ 'log.access_file': 'access.log',
        # ~ 'log.error_file': 'error.log',
        }
    )

# Set server to listen on a listening_ip
cherrypy.server.socket_host = listening_ip

# Run the application 
def run():
    cherrypy.quickstart(BlockchainRPC(), '/', config=config)
