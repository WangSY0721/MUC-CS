import matplotlib.pyplot as plt
from sklearn.cluster import KMeans  # 导入KMeans聚类算法
from sklearn import datasets
import os

# 在 Python 脚本中设置环境变量以避免内存泄漏问题
# 通过设置 'OMP_NUM_THREADS' 为 1，来指定仅使用一个线程进行并行计算，
os.environ['OMP_NUM_THREADS'] = '1'

# 加载数据集
iris = datasets.load_iris()
X = iris.data[:, :4]  # 只取数据集的前两个特征（花萼长度和花萼宽度）

# 构造KMeans聚类器
k = 3  # 设置聚类的簇数为3
kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)

# 使用训练数据拟合KMeans模型
kmeans.fit(X)  # 执行KMeans聚类，计算并确定聚类的结果

# 聚类结果可视化
# 使用散点图展示数据点，并根据KMeans聚类标签对颜色进行编码
plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, s=50, cmap='viridis')

# 获取聚类中心（质心），并在图中标出
centers = kmeans.cluster_centers_  # 获取KMeans聚类后的质心坐标
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)

# 设置标题和坐标轴标签
plt.title('K-means Clustering')
plt.xlabel('Sepal Length')  # 花萼长度
plt.ylabel('Sepal Width')  # 花萼宽度
plt.show()
