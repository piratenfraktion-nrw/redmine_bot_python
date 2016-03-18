# -*- coding: utf-8 -*-

from pyactiveresource.activeresource import ActiveResource
from pyactiveresource import formats

class User(ActiveResource):
    _site = 'https://redmine.piratenfraktion-nrw.de/'
    _format = formats.XMLFormat
