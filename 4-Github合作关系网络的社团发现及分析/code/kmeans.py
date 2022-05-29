# k-means
def k_means(m, K):
    """
    :param m: node2vec的训练结果
    :param K: 类别数
    :return: 聚类结果
    """
    nodes = list(G.nodes)
    # 任意选择K个节点作为初始聚类中心
    centers = []
    temp = []
    for i in range(K):
        t = np.random.randint(0, len(nodes) - 1)
        node = nodes[t]
        # print(node)
        # print(centers)
        if not isinstance(node, int):
            if node.all() not in centers:
                temp.append(nodes[t])
                # print(nodes[t])
                # print(type(nodes[t]))
                centers.append(m[int(nodes[t])])  # 中心为128维向量
        else:
            print(node in centers)
            print(node, centers)
            if node not in centers:
                temp.append(nodes[t])
                # print(nodes[t])
                # print(type(nodes[t]))
                centers.append(m[int(nodes[t])])  # 中心为128维向量

    # 迭代50次
    res = {}
    for i in range(K):
        res[i] = []

    for time in range(50):
        # clear
        for i in range(K):
            res[i].clear()
        # 算出每个点的向量到聚类中心的距离
        nodes_distance = {}
        for node in nodes:
            # node到中心节点的距离
            node_distance = []
            for center in centers:
                node_distance.append(get_dis(m[node], center))
            nodes_distance[node] = node_distance  # 保存node节点到各个中心的距离
        # 对每个节点重新划分类别，选择一个最近的节点进行分类，类别为0-5
        for node in nodes:
            temp = nodes_distance[node]  # 存放着6个距离
            cls = temp.index(min(temp))
            res[cls].append(node)

        # 更新聚类中心
        centers.clear()
        for i in range(K):
            center = []
            for j in range(128):
                t = [m[node][j] for node in res[i]]  # 第i个类别中所有node节点的第j个坐标
                center.append(np.mean(t))
            centers.append(center)

    return res
