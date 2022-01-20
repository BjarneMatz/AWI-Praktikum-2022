import imaplib
import json
import datetime
from datetime import timedelta
import email
import email.utils
import time

class Log:
    def __init__(self):
        self.debugging = False

    def print(self, logmessage):
        if self.debugging:
            print(logmessage)

    def enable(self):
        self.debugging = True

    def disable(self):
        self.debugging = False


class Cleaner:
    def __init__(self):
        self.login()
        self.scan()
        self.imap.close()
        self.imap.logout()


    def login(self):
        """Login to mailserver in account.json"""
        with open('account.json', encoding='utf-8') as f:
            account = json.load(f)
            try:
                self.username = account['user']
                self.password = account['password']
                self.server = account['server']
                self.port = account['port']
            except:
                log.print("You need to set your login credentials in account.json!")
            log.print(f"Logging in as {self.username} on {self.server}...")
            try:
                self.imap = imaplib.IMAP4(host=self.server, port=self.port)
                self.imap.login(self.username, self.password)
                log.print("Login Successful!")
            except Exception as ex:
                log.print("Login failed!")
                log.print(ex)
    def scan(self):
        """List all possible folders of target client"""
        self.imap.select()

        now = datetime.datetime.today()
        then = now - timedelta(days=90)
        then = then.date()
        print(then)
        testtime = then.strftime('%d-%b-%Y')
        print(testtime)

        _, mails = self.imap.search(None, f'before "{testtime}"')
        print("Mail IDs : {}\n".format(mails[0].decode().split())) # print all mail ids that have been found

        for mail_id in mails[0].decode():
            response, mail_data = self.imap.fetch(mail_id, '(RFC822)')
            self.message = email.message_from_bytes(mail_data[0][1])


            subject = (self.message.get("subject"))
            print("Deleting", subject)
            #self.imap.store(mail_id, "+FLAGS", "\\Deleted")


if __name__ == "__main__":
    log = Log()
    log.enable()
    log.print("Starting logging module")
    clean = Cleaner()
