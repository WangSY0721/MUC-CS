from sklearn.decomposition import PCA
import pandas as pd
from sklearn.datasets import load_iris

# 加载Iris数据集
data = load_iris()

# 创建DataFrame并显示前五行
df = pd.DataFrame(data.data, columns=data.feature_names)
df['species'] = data.target

# 设置显示的最大列数
pd.set_option('display.max_columns', None)  # 显示所有列

# 获取特征数据
X = df.drop('species', axis=1)

# 创建PCA对象，选择降维到2维
pca = PCA(n_components=2)  # n_components参数指定了要选择多少个主成分（即降维后的维度）

# 使用PCA进行降维
X_pca_sklearn = pca.fit_transform(X)  # 确保使用标准化后的数据
# fit步骤计算训练数据（在这里是X）的主成分，transform步骤将这些主成分应用于数据集，将原始数据转换到新的特征空间

# 创建降维后的DataFrame并显示前五行
df_pca_sklearn = pd.DataFrame(X_pca_sklearn, columns=[f'PC{i+1}' for i in range(2)])

print("使用sklearn降维后的数据（前五行）：")
print(df_pca_sklearn.head())
