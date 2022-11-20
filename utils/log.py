import time

class Log:
    @staticmethod
    def log(tag, msg):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'[{time_str}] {tag}: {msg}')
