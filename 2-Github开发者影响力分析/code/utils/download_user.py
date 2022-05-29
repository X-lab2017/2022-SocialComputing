import connect

from odps.df import DataFrame


def download():
    o = connect.connect()
    users = DataFrame(o.get_table('ods_github_users'))
    users = users.to_pandas()
    user_follow = users.loc[:, ["database_id", "followers", "following"]]
    user_follow.to_csv("../data/users.csv", index=False)


if __name__ == '__main__':
    download()
