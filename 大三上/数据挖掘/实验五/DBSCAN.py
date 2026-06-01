import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import datasets

# 加载数据集
iris = datasets.load_iris()
X = iris.data[:, :4]

# 构造聚类器
dbscan = DBSCAN(eps=0.41, min_samples=5, metric='euclidean')
dbscan.fit(X)

# 聚类结果可视化
plt.scatter(X[:, 0], X[:, 1], c=dbscan.labels_, s=50, cmap='viridis')
plt.title('DBSCAN Clustering')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()