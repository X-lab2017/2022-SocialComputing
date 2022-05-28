from select import select
from odps import ODPS
from odps import options
from odps.df import DataFrame
import pandas as pd
import numpy as np

def get_odps(ACCESS_ID = 'LTAI5t9uwJrh5eJ7Q5E37D1s',
             SECRET_ACCESS_KEY = 'NCFHOAnvqfnTrpypgR4b3cNawP8fnB',
             ODPS_PROJECT = 'OpenDigger_prod_dev',
             ODPS_ENDPOINT = 'http://service.cn-shanghai.maxcompute.aliyun.com/api'):

    # ACCESS_ID = 'LTAI5tSjrYp6JDW2bbiTdegU'
    # SECRET_ACCESS_KEY = 'OE6JbSqOZUey5fzr9Wg6fuYYKvslZx'
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
