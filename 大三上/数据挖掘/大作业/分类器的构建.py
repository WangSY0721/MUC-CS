import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from collections import Counter

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 读取数据，使用分号分隔符
data = pd.read_csv('student-mat.csv', sep=';')

# 编码所有非数值型数据
encoder = LabelEncoder()
for col in data.columns:
    if data[col].dtype == 'object':
        data[col] = encoder.fit_transform(data[col])

# 特征选择
important_features = ['G2', 'G1', 'failures', 'Medu', 'higher', 'age', 'Fedu', 'goout', 'romantic', 'traveltime']
X = data[important_features]
y = data['G3']

# 移除样本数小于2的类别
y_counts = y.value_counts()
min_samples = 2  # 设定移除样本数少于2的类别
valid_classes = y_counts[y_counts >= min_samples].index
data = data[data['G3'].isin(valid_classes)]
X = data[important_features]
y = data['G3']

# 数据平衡处理，设置较小的n_neighbors避免邻居过少的错误
smote = SMOTE(random_state=42, k_neighbors=2)
X, y = smote.fit_resample(X, y)

# 查看采样后的类别分布
print("SMOTE后类别分布：")
print(Counter(y))

# 标准化特征数据
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 定义评估函数
def evaluate_model(y_test, y_pred, model_name):
    print(f"\n模型: {model_name}")
    print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")
    print("分类报告:")
    print(classification_report(y_test, y_pred))
    print("混淆矩阵:")
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.title(f"{model_name} 混淆矩阵")
    plt.show()

# 1.决策树
clf_tree = DecisionTreeClassifier(random_state=42)
clf_tree.fit(X_train, y_train)
y_pred_tree = clf_tree.predict(X_test)
evaluate_model(y_test, y_pred_tree, "决策树")

# 2.支持向量机 (SVM)
clf_svm = SVC(kernel='linear', random_state=42)
clf_svm.fit(X_train, y_train)
y_pred_svm = clf_svm.predict(X_test)
evaluate_model(y_test, y_pred_svm, "支持向量机")

# 3.朴素贝叶斯
clf_nb = GaussianNB()
clf_nb.fit(X_train, y_train)
y_pred_nb = clf_nb.predict(X_test)
evaluate_model(y_test, y_pred_nb, "朴素贝叶斯")

# 4.神经网络
clf_nn = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
clf_nn.fit(X_train, y_train)
y_pred_nn = clf_nn.predict(X_test)
evaluate_model(y_test, y_pred_nn, "神经网络")
