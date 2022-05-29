import os
import random

import pandas as pd
import numpy as np
from birankpy import birank


def get_data():
    datafiles = os.listdir('./data/log')
    datalist = []
    for datafile in datafiles:
        if datafile[0:3] == 'log':
            datalist.append(pd.read_csv('./data/log/' + datafile, index_col=False))
    data = pd.concat(datalist)
    return data


def data_preprocess(data, actor_limit, repo_limit):
    actor_id_count = data['actor_id'].value_counts()
    actor_id_count = actor_id_count[actor_id_count > actor_limit]
    actor_id = list(actor_id_count.index)
    actor_id_nobot = []
    id2name = {}
    with open("./data/users_name.csv", "r") as f:
        for line in f:
            try:
                temp = line.split(',')
                temp_id = int(temp[0])
                temp_name = temp[1][:-1]
                id2name[temp_id] = temp_name
            except ValueError:
                continue
    for i in actor_id:
        if 'bot' not in id2name[i]:
            actor_id_nobot.append(i)
    actor_id = actor_id_nobot

    repo_id_count = data['repo_id'].value_counts()
    repo_id_count = repo_id_count[repo_id_count > repo_limit]
    repo_id = list(repo_id_count.index)

    data_c = data[data['actor_id'].isin(actor_id)]
    data_c = data_c[data_c['repo_id'].isin(repo_id)]

    cheat_ids = [4995967, 31698676, 63229723, 56715417]
    for cheat_id in cheat_ids:
        repo_cnt = random.randint(5, 10)
        for i in range(repo_cnt):
            repo_id_ = repo_id[random.randint(0, len(repo_id))]
            pr_cnt = random.randint(5, 10)
            for j in range(pr_cnt):
                data_c.append(pd.DataFrame([cheat_id, repo_id_, "2021-12-%d %d:%d:%d" % (
                    random.randint(1, 30), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))]),
                              ignore_index=False)

    data_c['created_at'] = pd.to_datetime(data_c['created_at'])
    data_c['created_at'] = pd.to_numeric(data_c['created_at'])
    return data_c


def get_weight(data_c):
    w = {}
    for i in data_c.groupby(['actor_id', 'repo_id'])['created_at']:
        link = i[0]
        time = [int(x) for x in list(i[1])]
        time.sort()
        if len(time) == 1:
            b = 1
        else:
            time_interval = []
            prev = time[0]
            for curr in time:
                time_interval.append(curr - prev)
                prev = curr
            time_interval.remove(0)
            mean = np.mean(time_interval)
            std = np.std(time_interval)
            if std + mean == 0:
                b = 1
            else:
                b = (std - mean) / (std + mean)
        w[link] = - b + 1

    actor_id_set = set()
    repo_id_set = set()
    for i in w.keys():
        actor_id_set.add(i[0])
        repo_id_set.add(i[1])
    actor_id_list = list(actor_id_set)
    repo_id_list = list(repo_id_set)

    actor_id_list.sort()
    repo_id_list.sort()

    W = np.zeros((len(actor_id_list), len(repo_id_list)))

    for item in w.keys():
        i = actor_id_list.index(item[0])
        j = repo_id_list.index(item[1])
        W[i][j] = w[item]

    return W, actor_id_list, repo_id_list


def main():
    data = get_data()
    data_c = data_preprocess(data, 20, 200)
    weight, actor_id_list, repo_id_list = get_weight(data_c)
    actor, repo = birank(weight, normalizer='HITS', alpha=0.85, beta=0.85, max_iter=200, tol=1e-6, verbose=True)
    actor = actor.tolist()
    repo = repo.tolist()
    outpufile = "burstbirank_nobot"
    with open(f'./result_cheat/{outpufile}_actor.txt', 'w') as f:
        f.write("actor_id\trank\n")
        for i in range(len(actor)):
            f.write(str(actor_id_list[i]) + '\t' + str(actor[i]) + '\n')
    with open(f'./result_cheat/{outpufile}_repo.txt', 'w') as f:
        f.write("repo_id\trank\n")
        for i in range(len(repo)):
            f.write(str(repo_id_list[i]) + '\t' + str(repo[i]) + '\n')


if __name__ == '__main__':
    main()
