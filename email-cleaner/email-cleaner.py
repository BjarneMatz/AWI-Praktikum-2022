import imaplib
import json


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


    def login(self):

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


if __name__ == "__main__":
    log = Log()
    log.enable()
    log.print("Starting logging module")
    clean = Cleaner()
