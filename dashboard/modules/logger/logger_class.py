from datetime import datetime
import os


class logger_model:
    def __init__(self):
        self.file_name = os.path.join("./logs.txt")


    def info(self, message):

        content = f"{str(datetime.now())} - {message}\n"

        with open(self.file_name, 'a') as f:
            f.write(content)

        print(content)
