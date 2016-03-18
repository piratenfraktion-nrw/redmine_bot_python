#/bin/python
# -*- coding: utf-8 -*-

"""redmine_bot.

Usage:
    redmine_bot.py mode (renew|umlauf|unhold|inventarcheck|inventarmails|drucksachen_opal) [--issue_id=<id>]
    redmine_bot.py (-h|--help)
    redmine_bot.py --version
Options:
    -h --help       Show this screen.
    --version       Show version.

"""

from docopt import docopt
from drucksachen_opal import DrucksachenOpal

def main(mode):
    if arguments['renew']:
        renew()
    elif arguments['umlauf']:
        umlauf()
    elif arguments['unhold']:
        unhold()
    elif arguments['inventarcheck']:
        inventarcheck()
    elif arguments['inventarmails']:
        inventarmails()
    elif arguments['drucksachen_opal']:
        DrucksachenOpal().fetch_emails()
    else:
        print('unsupported mode')

    # return {
    #     'renew': renew()
    # }.get(mode, print('unsupported mode'))

if __name__ == "__main__":
    arguments = docopt(__doc__, version='redmine_bot 0.1')
    # print(arguments)
    main(arguments)
