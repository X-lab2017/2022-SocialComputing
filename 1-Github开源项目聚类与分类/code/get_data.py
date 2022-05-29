import os
import threading
import time
import sys

def delete_output(dir_name):
    if not os.path.exists(dir_name):
        print('Directory not exist')
        return
    C = 0
    for f in os.listdir(dir_name):
        fn = '/'.join((dir_name, f))
        try:
            os.remove(fn)
            C += 1
        except:
            print('Fail to delete file {fn}'.format(fn = fn))
    print('Complete deleting {C} files in directory {DIR}'.format(C = C, DIR = dir_name))
        
def get_data(o):
    dir_path = "data"
    separator = "\n<" + "-" * 10 + ">\n"

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    issue_data = []
    TEMP_TABLE_NAME = "tmp_10195501411"
    
    t1 = thread()
    t1.start()
    
    get_data_sql = """
        select repo_id, collect_list(issue_body) from ods_github_log
        where pt >= 20190101 and pt < 20200101
        and repo_id in (select repo_id from {TEMP_TABLE_NAME})
        and type = 'IssuesEvent'
        group by repo_id
        having count(*) > 0
    """.format(TEMP_TABLE_NAME=TEMP_TABLE_NAME)
    
    with o.execute_sql(get_data_sql).open_reader() as reader:
        for record in reader:
            issue_data.append(list(record))
    
    delete_output('data')
    
    for t, (y, X) in enumerate(issue_data):
        y, X = str(y[1]), X[1]
        txt_idx = t // 1000
        file = "/".join((dir_path, "-".join(("data", str(txt_idx) + ".txt"))))
        f = open(file, 'a+', encoding = 'utf-8')
        f.write(y + "\n" + " ".join(X[0:20]) + separator)
        f.close()
        
    t1.stop()
    print("\n总计获取{NUM}条数据".format(NUM = len(issue_data)))
        
class thread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.flag = 0
        
    def waiting(self):
        c = 0
        while True:
            if self.flag:
                return
            if c > 240:
                return
            print("\r", end="")
            msg = "Loading data now" + "." * (c % 3 + 1) + " " * (3 - (c % 3 + 1))    
            c += 1
            print(msg, end = '', flush = True)
            time.sleep(1)
        return
            
    def run(self):
        self.waiting()
        return
        
    def stop(self):
        self.flag = 1
        return
        