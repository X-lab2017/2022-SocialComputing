import connect


def download():
    o = connect.connect()
    with open("../data/users_name.csv", "w") as f:
        f.write("id, name\n")
        sql = "SELECT actor_id, actor_login FROM dim_github_actor"
        with o.execute_sql(sql).open_reader() as reader:
            for record in reader:
                f.write(str(record.actor_id) + "," + record.actor_login + "\n")


if __name__ == '__main__':
    download()
