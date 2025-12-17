from logger import log_error

try:
    lst = [10, 20, 30]
    value = lst[10]
except Exception as e:
    log_error(e)
