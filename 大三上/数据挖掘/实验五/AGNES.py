import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering  # 导入AGNES聚类算法
from sklearn import datasets

# 加载数据集
iris = datasets.load_iris()
X = iris.data[:, :4]

# 构造聚类器
agnes = AgglomerativeClustering(n_clusters=3, linkage="ward")  # 初始化AGNES聚类器，设置目标簇数为3

# 执行聚类算法
agnes.fit(X)

# 聚类结果可视化
plt.scatter(X[:, 0], X[:, 1], c=agnes.labels_, s=50, cmap='viridis')

# 添加图表标题和标签
plt.title('AGNES Clustering')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()
