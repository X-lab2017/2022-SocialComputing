import threading

import connect


def download(partition):
    o = connect.connect()
    sql = """
    SELECT actor_id, repo_id, created_at
    FROM ods_github_log
    WHERE  pt=%s
    AND type='PullRequestEvent'
    """ % partition
    filename = '../data/log/log%s.csv' % partition
    with open(filename, 'w') as f:
        f.write('actor_id,repo_id,type,created_at\n')
        with o.execute_sql(sql).open_reader() as reader:
            for i in reader:
                line = (str(i.actor_id) + ','
                        + str(i.repo_id) + ','
                        + str(i.type) + ','
                        + str(i.created_at) + ',' + '\n')
                f.write(line)


class DownloadThread(threading.Thread):
    def __init__(self, partition):
        super(DownloadThread, self).__init__()
        self.partition = partition

    def run(self):
        download(self.partition)


if __name__ == '__main__':
    threads = []
    ptList = ['20210101', '20210201', '20210301', '20210401', '20210501', '20210601',
              '20210701', '20210801', '20210901', '20211001', '20211101', '20211201']
    for pt in ptList:
        thread = DownloadThread(pt)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
