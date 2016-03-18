# -*- coding: utf-8 -*-

import configparser
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource import formats

config = configparser.ConfigParser()
config.read('./config.ini')

redmine_api_key = config['default']['redmine_api_key']
redmine_url = config['default']['redmine_url']

class Issue(ActiveResource):
    _headers = { 'X-Redmine-API-Key': redmine_api_key }
    _site = redmine_url
    # _format = formats.XMLFormat

