# SC

当前已设置为Private

source url:http://openinsight.x-lab.info/superset/sqllab/

当前已设置为Private

data与data_csv内是实验数据，但水杉码园传不上来

代码结构有点乱，尤其是数据获取的部分，因为只要获取一次就够了。

cluster是我写的KMeans和两种距离。

connect.py是连接到ods数据集。

context_vec.py是文本编码成词向量，里面两个方法对应上下文编码，嵌入层编码。

Contribute_vec.ipynb只用了一次，用于多表连接，计算贡献分数，存入Action.csv后就没用了

Drafts.ipynb顾名思义只用了一次，将ods数据转化成csv，以及最后部分用Pygithub爬取了数据（那几个token已经过期了）。另外部分是草稿。

get_data.py用于获取data文件夹里的文本数据。

get_dataset.py用于获取纯文本，以及贡献向量。

get_df.py用于提取ods数据集的数据并整理成csv返回。

main.py是主体文件，包括各种模型的使用，训练，以及生成结果。

MLP.py和TextCNN.py是模型文件。

read_data.py是从data文件夹里读取纯文本数据。

transform.py是清洗文本，并提取tf-idf向量。