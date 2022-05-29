import os

def read_data():
    dir_path = "data"
    separator = "\n<" + "-" * 10 + ">\n"
    
    assert os.path.exists(dir_path)
    
    repo_name = []
    repo_data = []
    
    for file in os.listdir(dir_path):
        if file[-4:] != '.txt':
            continue
        file_path = "/".join((dir_path, file))
        f = open(file_path, 'r+', encoding = 'utf-8')
        repo = f.read().split(separator)
        for r in repo:
            if r:
                name, data = r.split("\n", 1)
                repo_name.append(int(name))
                repo_data.append(data)
    return repo_name, repo_data