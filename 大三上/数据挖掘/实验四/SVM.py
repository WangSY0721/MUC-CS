import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 加载iris数据集
iris = datasets.load_iris()

# 选取前两列特征，即花萼长度和花萼宽度
X = iris.data[:, :2]
# 目标变量，即类别标签
y = iris.target

# 划分训练集和测试集，测试集占30%，随机种子为42以保证结果可复现
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建SVM分类器，使用线性核
clf = svm.SVC(kernel='linear', C=1.0)

# 训练分类器，使用训练集数据
clf.fit(X_train, y_train)

# 使用训练好的分类器进行预测
y_train_pred = clf.predict(X_train)  # 预测训练集
y_test_pred = clf.predict(X_test)  # 预测测试集

# 计算准确率
train_accuracy = accuracy_score(y_train, y_train_pred)  # 训练集准确率
test_accuracy = accuracy_score(y_test, y_test_pred)  # 测试集准确率
print(f"训练数据集的准确率为：{train_accuracy}")
print(f"测试数据集的准确率为：{test_accuracy}")

# 创建网格，用于绘制决策边界
h = .02  # 网格步长
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1  # 确定x轴的范围
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1  # 确定y轴的范围
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))  # 创建网格

# 预测网格点的类别
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)  # 将预测结果重塑为网格的形状

# 绘制预测结果
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired, shading='auto')  # 使用新的颜色映射绘制决策边界

# 绘制训练点和测试点
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=plt.cm.Paired, edgecolors='k', label='train')  # 训练点
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.Paired, edgecolors='k', marker='^', label='test')  # 测试点

# 设置图表的标签和标题
plt.xlabel('feature1')
plt.ylabel('feature2')
plt.title('SVM_visualize')
plt.legend()  # 显示图例
plt.show()
