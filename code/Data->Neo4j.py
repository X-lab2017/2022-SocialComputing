from py2neo import Graph, Node,Relationship,NodeMatcher
import csv
graph = Graph('http://localhost:7474', auth = ('neo4j','syz0615'))


def createnode():
    csvFile = open("point.csv", "r")
    reader = csv.reader(csvFile)

    # 建立空字典
    result = {}
    nums=0
    for line in reader:
        if nums >= 10000 and nums < 50000:
            if reader.line_num == 1 or len(line) == 0:
                continue
            node = Node("repo", repo_id=int(line[0]),pagerank=float(line[1]))
            graph.create(node)

        nums += 1


def createrelationship():
    matcher = NodeMatcher(graph)
    csvFile = open("line.csv", "r")
    reader = csv.reader(csvFile)

    # 建立空字典
    result = {}
    nums = 0
    for line in reader:
        if nums >= 5000 and nums < 25000:
            if reader.line_num == 1 or len(line) == 0:
                continue
            node_1 = matcher.match("repo", repo_id=int(line[0])).first()
            node_2 = matcher.match("repo", repo_id=int(line[1])).first()
            rel1 = Relationship(node_1,line[2],node_2)
            rel2 = Relationship(node_2,line[2],node_1)
            graph.create(rel1)
            graph.create(rel2)
        nums+=1

def delete():
    graph.delete_all()
if __name__ == "__main__":
    createrelationship()


