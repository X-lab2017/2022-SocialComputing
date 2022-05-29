import pandas as pd

def create_tmp_table(o):
    TEMP_TABLE_NAME = "tmp_10195501411"
    TYPE_LIST = ('IssuesEvent', 'PullRequestEvent', 'PullRequestReviewCommentEvent', 'WatchEvent', 'ForkEvent')
    drop_sql = """
        DROP TABLE IF EXISTS {TEMP_TABLE_NAME};
        CREATE TABLE IF NOT EXISTS {TEMP_TABLE_NAME}
        (
        repo_id BIGINT,
        actor_id BIGINT,
        actor_login STRING,
        type STRING,
        action STRING,
        pull_merged INT
        );
    """.format(TEMP_TABLE_NAME=TEMP_TABLE_NAME)

    o.execute_sql(drop_sql, hints = {"odps.sql.submit.mode" : "script"})

    tmp_sql = """
        insert into {TEMP_TABLE_NAME}
        select repo_id, actor_id, actor_login, type, action, pull_merged from ods_github_log
        WHERE pt>='20190101' and pt <'20200101'
        and type in {TYPE_LIST}
        limit 100000;
    """.format(TEMP_TABLE_NAME=TEMP_TABLE_NAME, TYPE_LIST = TYPE_LIST)

    o.execute_sql(tmp_sql)
    
def get_dataframe(o):
    data = []
    TEMP_TABLE_NAME = "tmp_10195501411"
    check_sql = """
        select * from {TEMP_TABLE_NAME}
    """.format(TEMP_TABLE_NAME = TEMP_TABLE_NAME)
    
    with o.execute_sql(check_sql).open_reader() as reader:
        
        df = pd.DataFrame(reader)
    print(df.head())
    
    return df