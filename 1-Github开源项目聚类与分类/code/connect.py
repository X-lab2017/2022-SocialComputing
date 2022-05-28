from select import select
from odps import ODPS
from odps import options
from odps.df import DataFrame
import pandas as pd
import numpy as np

def get_odps(ACCESS_ID = '',
             SECRET_ACCESS_KEY = '',
             ODPS_PROJECT = 'OpenDigger_prod_dev',
             ODPS_ENDPOINT = 'http://service.cn-shanghai.maxcompute.aliyun.com/api'):

    # 创建odps实例
    o = ODPS(ACCESS_ID, SECRET_ACCESS_KEY,
             project=ODPS_PROJECT, endpoint=ODPS_ENDPOINT)
    options.tunnel.limit_instance_tunnel = False
    # options.read_timeout = 3600000

    users = DataFrame(o.get_table('ods_github_users'))
    print(users.dtypes)

    github_log = DataFrame(o.get_table('ods_github_log'))
    print(github_log.dtypes)
    
    return o

if __name__ == "__main__":
    o = get_odps()
    sql = "SELECT count(*) FROM ods_github_log WHERE pt>='20150101' and pt <'20160101';"
    with o.execute_sql(sql).open_reader() as reader:
        for record in reader:
            for r in record:
                print(r)
