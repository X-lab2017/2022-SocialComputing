import random

import pandas as pd
import networkx as nx


def cheat_pagerank():
    user_follow = pd.read_csv('data/users.csv', dtype=str)
    user_follow_d = user_follow.drop_duplicates()
    database_id_list = user_follow_d['database_id'].tolist()
    cnt = len(database_id_list)
    g = nx.DiGraph()
    cheat_ids = [87947603, 65024265, 93661980, 21011899]
    for database_id, followers, following in user_follow_d.values:
        followers = str(followers).split(",")
        for follower in followers:
            if follower != 'nan':
                g.add_edge(follower, database_id)

        following = str(following).split(",")
        for one_following in following:
            if one_following != 'nan':
                g.add_edge(database_id, one_following)

        if int(database_id) in cheat_ids:
            for i in range(100):
                g.add_edge(database_id_list[random.randint(0, cnt)], database_id)

    pr = nx.pagerank(g)
    with open("result_cheat/pagerank.txt", "w") as f:
        f.write("id\tpagerank\n")
        for key in pr:
            f.write(str(key) + "\t" + str(pr[key]) + "\n")


if __name__ == '__main__':
    cheat_pagerank()
