import datetime


def log_tracking(message):
    print('[' + str(datetime.datetime.now()) + ']' + ' [LOG] ' + message)


def error_tracking(message):
    print('[' + str(datetime.datetime.now()) + ']' + ' [ERROR] ' + message)
