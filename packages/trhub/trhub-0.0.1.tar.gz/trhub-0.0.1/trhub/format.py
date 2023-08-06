def kline(item):
    return {
        "time": float(item[0]),
        "open": float(item[1]),
        "low": float(item[2]),
        "high": float(item[3]),
        "close": float(item[4]),
        "volume": float(item[5])}


def minute(item):
    return {
        "time": float(item[0]),
        "close": float(item[1]),
        "volume": float(item[2])
    }


def code(item):
    return {
        "code": item[0],
        "name": item[1],
        "update": float(item[2])
    }


def tradeday(item):
    return {
        "date": item[0],
        "uptime": float(item[1])
    }
