import pandas as pd
import networkx as nx


def pagerank():
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

    pr = nx.pagerank(g)
    print('end')
    with open("./result/pagerank.txt", "w") as f:
        f.write("id\tpagerank\n")
        for key in pr:
            f.write(str(key) + "\t" + str(pr[key]) + "\n")
    print('save')


if __name__ == '__main__':
    pagerank()
