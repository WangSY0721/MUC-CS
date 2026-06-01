import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 读取数据
file_path = 'student-mat.csv'
data = pd.read_csv(file_path, sep=';')

# 数据清洗
# 编码类别特征&处理异常值
categorical_features = data.select_dtypes(include=['object']).columns
data_encoded = pd.get_dummies(data, columns=categorical_features, drop_first=True)

# 截断缺勤异常值
absences_threshold = data_encoded['absences'].quantile(0.99)
data_encoded['absences'] = data_encoded['absences'].clip(upper=absences_threshold)

# 特征和目标变量分离
X = data_encoded.drop(columns=['G3'])  # 特征集（去掉目标变量 G3）
y = data_encoded['G3']  # 目标变量

# 数据集划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 打印输出
print("训练集样本数:", X_train.shape[0])
print("测试集样本数:", X_test.shape[0])
