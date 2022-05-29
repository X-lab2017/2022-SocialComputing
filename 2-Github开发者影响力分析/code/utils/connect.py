from odps import ODPS
from odps import options


def connect():
    ACCESS_ID = ''
    SECRET_ACCESS_KEY = ''
    ODPS_PROJECT = ''
    ODPS_ENDPOINT = ''
    # 创建odps实例
    o = ODPS(ACCESS_ID, SECRET_ACCESS_KEY,
             project=ODPS_PROJECT, endpoint=ODPS_ENDPOINT)
    options.tunnel.limit_instance_tunnel = False
    # options.read_timeout = 3600000

    return o
