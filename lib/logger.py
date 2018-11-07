from datetime import datetime

def log(*args):
    msg = ""
    for a in args:
        msg += a
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('[' + now + ']: ' + msg)
