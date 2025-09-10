from datetime import datetime
import os


class logger_model:
    def __init__(self):
        self.file_name = os.path.join("./logs.txt")


    def info(self, message):
        from dashboard.views_pages import toolkit as tk



        content = f"{str(datetime.now())} - {message}\n"

        with open(self.file_name, 'a') as f:
            f.write(content)

        print(content)

        tk.send_message_to_frontend_dashboard(topic='logger_to_frontend', payload=message)
