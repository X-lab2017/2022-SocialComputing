from select import select
from odps import ODPS
from odps import options
from odps.df import DataFrame
import pandas as pd
import numpy as np


ACCESS_ID = 'LTAI5tHDArybZRnXaPS3pdkJ'
SECRET_ACCESS_KEY = 'lXXLM2U1dB3ExgKquGUwdGb88WHqkN'
ODPS_PROJECT = 'OpenDigger_prod_dev'
ODPS_ENDPOINT = 'http://service.cn-shanghai.maxcompute.aliyun.com/api'

o = ODPS(ACCESS_ID, SECRET_ACCESS_KEY,
         project=ODPS_PROJECT, endpoint=ODPS_ENDPOINT)
options.tunnel.limit_instance_tunnel = False

#统计开发者对某一项目的贡献度   计算结果保存在SYZ_CQK_Temptable1表中
SQL1 = '''CREATE Table SYZ_CQK_Temptable1 AS     
              SELECT  SUM(t.score ) as score,actor_id, repo_id
              FROM (Select case when type = 'IssueCommentEvent' THEN 1
              when type = 'IssuesEvent' THEN 2
              when type = 'PullRequestEvent' THEN 3
              when type = 'PullRequestReviewCommentEvent' THEN 4
              ELSE 0 END as score ,actor_id,repo_id
              FROM ods_github_log
              WHERE pt>'20211001' and pt <= '20211201'
              ) t
              GROUP BY actor_id,repo_id'''


# print(SQL1)
# result = o.execute_sql(SQL1,hints={'odps.sql.allow.fullscan': 'true'})

#计算项目与项目之间的协作关联度  结果保存在SYZ_CQK_TempResult表中
SQL2 = '''CREATE Table SYZ_CQK_TmpResult AS
            SELECT s1.actor_id,s1.score * s2.score / (s1.score + s2.score) 
            AS new_score,s1.repo_id,s2.repo_id,s2.score 
            FROM (SELECT * FROM SYZ_CQK_Temptable1)  s1 JOIN (SELECT * FROM SYZ_CQK_Temptable1) s2 
            ON s1.actor_id = s2.actor_id AND s1.repo_id != s2.repo_id
'''

# result = o.execute_sql(SQL2,hints={'odps.sql.allow.fullscan': 'true'})

SQL3 = '''SELECT * FROM ods_github_log'''
result = o.execute_sql(SQL3, hints={'odps.sql.allow.fullscan': 'true'})

with result.open_reader() as reader:
    for record in reader:
        print(record)

# #读取SQL执行结果。
# with result.open_reader() as reader:
# github_log = DataFrame(o.get_table('ods_github_log'))
# print(github_log.dtypes)