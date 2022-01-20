import datetime
import email
import email.utils
import imaplib
import json
from datetime import timedelta


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
        self.scananddelete()
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
                log.print("Setting user credentials and server information...")
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

    def scananddelete(self):
        # select no specific folder
        self.imap.select()
        log.print("Removed folder selection...")
        # set date til mails get removed
        now = datetime.datetime.today()
        log.print("Set date to now...")
        with open('account.json', encoding='utf-8') as f:
            account = json.load(f)
            maxtime = account['max-time-in-days']
            log.print("Loaded max duration from json...")
        then = now - timedelta(days=int(maxtime))
        then = then.date()
        testtime = then.strftime('%d-%b-%Y')
        log.print("Calculated max duration...")
        log.print(testtime)

        _, mails = self.imap.search(None, f'before "{testtime}"')
        log.print("Mail search completed...")
        print("Mail IDs : {}\n".format(mails[0].decode().split()))  # print all mail ids that have been found

        for mail_id in mails[0].decode():
            log.print(f"Decoding mail id {mail_id}...")
            response, mail_data = self.imap.fetch(mail_id, '(RFC822)')
            self.message = email.message_from_bytes(mail_data[0][1])
            subject = (self.message.get("subject"))
            log.print(f"Found {subject}...")
            print("Deleting", subject)
            self.imap.store(mail_id, "+FLAGS", "\\Deleted")
            log.print(f"Flagged {mail_id} as deleted...")
        log.print("Looped through all mails successfully...")
        # delete all mails that are flagged as \\Deleted as set above
        self.imap.expunge()
        log.print("Deleted all mails flagged as deleted...")
        log.print("Exiting now...")


if __name__ == "__main__":
    log = Log()
    log.enable()
    log.print("Starting logging module")
    clean = Cleaner()
