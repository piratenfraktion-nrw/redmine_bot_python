import getpass, imaplib, configparser, requests
from drucksachen_extractor import DrucksachenExtractor
from model.issue import Issue

class DrucksachenOpal():

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.upload = None

        self.redmine_api_key = config['default']['redmine_api_key']
        self.redmine_url = config['default']['redmine_url']

        self.username = config['drucksachen']['username']
        self.password = config['drucksachen']['password']
        self.imaps_server = config['drucksachen']['imaps_server']
        self.imaps_port = config['drucksachen']['imaps_port']
        self.imaps_folder = config['drucksachen']['imaps_folder']
        self.imaps_folder_read = config['drucksachen']['imaps_folder_read']

    def fetch_emails(self):
        imap = imaplib.IMAP4_SSL(self.imaps_server, self.imaps_port)
        imap.login(self.username, self.password)
        imap.select(self.imaps_folder)
        typ, data = imap.search(None, 'SUBJECT', 'Parlamentspapiere')
        for num in data[0].split():
            typ, data = imap.fetch(num, '(RFC822)')
            # print('Message %s\n%s\n' % (num, data[0][1]))
            drucksachen = DrucksachenExtractor(data[0][1]).parse()

            for d in drucksachen:

                f = bytearray()

                r = requests.get(d.link, stream=True)
                '''for chunk in r.iter_content(chunk_size=1024):
                   if chunk: # filter out keep-alive new chunks
                        f += chunk
                '''
                if r.status_code == 200:
                    headers = {'content-type': 'application/octet-stream'}
                    res = requests.post(
                            self.redmine_url + '/uploads.json?key=' + self.redmine_api_key,
                            data = r, headers = headers
                            # files={'file': f}, headers = headers
                        )
                    if res.status_code != 201: # 201 == Created
                        print('requests.post: ', res.status_code)
                        self.upload = None
                    else:
                        token = res.json()['upload']['token']

                        self.upload = [{
                                'token': token,
                                'filename': d.number + '.pdf',
                                'description': d.number,
                                'content': 'application/pdf'
                            }]
                else:
                    self.upload = None

                issue = Issue({
                        'subject': d.number + ":" + d.title ,
                        'project_id': 62, # 'Dokumente'
                        'tracker_id': 11,
                        'description': d.link,
                        'uploads': self.upload
                    })

                res = issue.save()

                if not res:
                    print(issue.subject, '=> ', res)

            status, msg_ids = imap.copy(num, self.imaps_folder_read)
            # TODO: print(status)
            imap.store(num, '+FLAGS', '\\Deleted')

        imap.close()
        imap.logout()
