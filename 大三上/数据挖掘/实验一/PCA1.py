from sklearn.datasets import load_iris
import pandas as pd
import numpy as np

# 加载鸢尾花数据集
iris = load_iris()
X = iris.data
y = iris.target

# 将数据转换为DataFrame格式
df = pd.DataFrame(X, columns=iris.feature_names)  # 创建DataFrame，列名为特征名称
df['species'] = iris.target_names[y]  # 添加一个新的列，包含对应的鸢尾花种类名称
print(df.head())

# 中心化数据
def demean(X):
    return X - np.mean(X,axis=0)  # 减去每个特征的均值，axis=0表示沿着列操作

X_demean = demean(X)  # 对特征数据进行中心化处理
print("标准化后的数据（前五行）：\n", X_demean[:5])

# 计算协方差矩阵
cov_matrix = np.cov(X_demean.T)  # 计算中心化后数据的协方差矩阵，.T表示转置
# cov是NumPy库中用于计算协方差矩阵的函数
print("协方差矩阵：\n", cov_matrix)

# 计算特征值和特征向量
eig_vals, eig_vecs = np.linalg.eig(cov_matrix)  # 对协方差矩阵进行特征值分解
# np.linalg是NumPy库中用于线性代数运算的模块，eig函数用于计算方阵的特征值和特征向量
print("特征值：\n", eig_vals)
print("特征向量：\n", eig_vecs)

# 选择前k个主成分
k = 2
top_k_eig_vecs = eig_vecs[:, :k]  # 选择前k列特征向量，对应于最大的k个特征值

# 计算降维后的数据
X_pca = X_demean.dot(top_k_eig_vecs)  # 将中心化后的数据与选定的特征向量相乘，实现降维
print("降维后的数据（前五行）：\n", X_pca[:5])
