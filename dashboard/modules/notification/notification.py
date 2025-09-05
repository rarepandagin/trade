
import requests
import os
from traceback import format_exc
from dashboard.views_pages import toolkit as tk

class NotificationClass:
    def __init__(self):
        self.toekn = f"84528{os.getenv('trader_telegram_token')}"
        self.chat_id = f"52149{os.getenv('trader_telegram_chat_id')}"


    def send(self, title, message):
        try:

            payload = f"<b>{title}</b>\n\n{message}"

            print(payload)

            url = f"https://api.telegram.org/bot{self.toekn}/sendMessage?chat_id={self.chat_id}&text={payload}&parse_mode=HTML"
            requests.get(url)


        except:
            try:
                print(format_exc())
                tk.logger.info(format_exc())    
            except:
                pass

if __name__ == "__main__":
    nt = NotificationClass()
    nt.send('ss', 'ss')