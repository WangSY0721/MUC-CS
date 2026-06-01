import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 读取数据
file_path = 'student-mat.csv'
data = pd.read_csv(file_path, sep=';')

# 1.数据清洗
# 检查缺失值
print("缺失值检查：")
print(data.isnull().sum())

# 编码类别特征
categorical_features = data.select_dtypes(include=['object']).columns
data_encoded = pd.get_dummies(data, columns=categorical_features, drop_first=True)

# 处理异常值
absences_threshold = data_encoded['absences'].quantile(0.99)
data_encoded['absences'] = data_encoded['absences'].clip(upper=absences_threshold)

# 2.数据描述
print("\n数据集基本信息：")
print(data_encoded.info())
print("\n数据描述统计：")
print(data_encoded.describe())

# 相关性分析
# 计算相关性矩阵
correlation_matrix = data_encoded.corr()

# 绘制与目标变量 G3 的相关性热力图
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix[['G3']].sort_values(by='G3', ascending=False),
            annot=True, cmap='viridis', linewidths=0.5)
plt.title('Feature Correlation with G3')
plt.show()

# 输出与G3强相关的特征
print("\n与G3强相关的特征：")
strong_corr_features = correlation_matrix['G3'].abs().sort_values(ascending=False).head(15)
print(strong_corr_features)

# 数据归约（PCA）
# 标准化数据
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_encoded.drop(columns=['G3']))

# 执行PCA
pca = PCA(n_components=5)
principal_components = pca.fit_transform(scaled_data)

# 查看PCA结果
print("\nPCA主要成分解释方差比：")
print(pca.explained_variance_ratio_)

# 将PCA结果转换为DataFrame
pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(5)])
print("\nPCA转换后的数据：")
print(pca_df.head())

# 查看每个主成分与原始特征的关系
print("\n每个主成分与原始特征的关系：")
pca_components = pd.DataFrame(pca.components_, columns=data_encoded.drop(columns=['G3']).columns)
print(pca_components)

