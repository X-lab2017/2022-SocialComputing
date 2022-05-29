import pandas as pd
import networkx as nx

from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)


def hits():
    user_follow = pd.read_csv('data/users.csv', dtype=str)
    user_follow_d = user_follow.drop_duplicates()
    g = nx.DiGraph()
    for database_id, followers, following in user_follow_d.values:
        followers = str(followers).split(",")
        for follower in followers:
            if follower != 'nan':
                g.add_edge(follower, database_id)

        following = str(following).split(",")
        for one_following in following:
            if one_following != 'nan':
                g.add_edge(database_id, one_following)
    print('start')

    h, a = nx.hits(g)
    print('end')
    with open("./result/hits_h.txt", "w") as f:
        f.write("id\th\n")
        for key in h:
            f.write(str(key) + "\t" + str(h[key]) + "\n")

    with open("./result/hits_a.txt", "w") as f:
        f.write("id\ta\n")
        for key in a:
            f.write(str(key) + "\t" + str(a[key]) + "\n")
    print('save')


if __name__ == '__main__':
    hits()
