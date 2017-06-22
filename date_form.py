import time
def date_form():
    #returns the current date in the YYYY-MM-DD HH:MM:SS required by the datetime data type in mysql
    full_dt = time.localtime()
    year = str(full_dt[0])
    month = leading_zero(full_dt[1],2)
    day = leading_zero(full_dt[2], 2)
    hour = leading_zero(full_dt[3],2)
    minutes = leading_zero(full_dt[4], 2)
    seconds = leading_zero(full_dt[5],2)
    date_time = "{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, minutes, seconds)
    return date_time
def leading_zero(x, length):
    if len(str(x)) < length:
        return "0" + str(x)
    else:
        return str(x)