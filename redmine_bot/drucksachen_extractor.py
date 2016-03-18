# -*- coding: utf-8 -*-

import bs4
import re
import os

class Drucksache():
    type = ''
    number = ''
    title = ''
    link = ''
    link_html = ''

class DrucksachenExtractor():

    def __init__(self, msg):
        self.drucksachen = []
        self.msg = msg

    def parse(self):
        soup = bs4.BeautifulSoup(self.msg, 'html.parser')
        pdf = soup.find_all('a',
                href=re.compile('^http://opal.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/.*\.pdf'))

        for f in pdf:
            d = Drucksache()
            d.link = f.get('href')
            pre, ext = os.path.splitext(d.link)
            d.link_html = pre + '.html'

            d.number = ''.join(pre.rsplit('/', 1)[-1:])
            d.title = f.text

            self.drucksachen.append(d)

        return self.drucksachen
