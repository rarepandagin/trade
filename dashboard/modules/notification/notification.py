
import requests
import os
from traceback import format_exc
from dashboard.views_pages import toolkit as tk

class NotificationClass:
    def __init__(self):
        self.token = f"{os.getenv('trader_telegram_token')}"
        self.chat_id = f"{os.getenv('trader_telegram_chat_id')}"


    def send(self, title, message):
        try:

            payload = f"<b>{title}</b>\n\n{tk.epoch_to_datetime(tk.get_epoch_now())}\n\n{message}"

            print(payload)

            url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={payload}&parse_mode=HTML"
            ret=requests.get(url)
            d=3

        except:
            # try:

            tk.logger.info(format_exc())    
            # except:
            #     pass

if __name__ == "__main__":
    nt = NotificationClass()
    nt.send('ss', 'ss')