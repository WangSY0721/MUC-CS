import math
from graphviz import Digraph

# 计算数据集的熵，熵是信息论中的概念，用于度量数据集的不确定性或混乱程度
def calculate_entropy(data_set):
    num_entries = len(data_set)  # 数据集中的样本数量
    label_counts = {}  # 用于统计每个类别的样本数量
    for feat_vec in data_set:
        current_label = feat_vec[-1]  # 获取样本的类别标签
        if current_label not in label_counts:
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    entropy = 0.0  # 熵的初始值
    for key in label_counts:
        prob = float(label_counts[key]) / num_entries  # 计算每个类别的概率
        entropy -= prob * math.log(prob, 2)  # 计算熵
    return entropy

# 计算信息增益，信息增益是选择决策树分裂属性的重要指标
def calculate_info_gain(data_set, attribute, feature_names):
    total_entropy = calculate_entropy(data_set)  # 计算数据集的总熵
    values = set([example[attribute] for example in data_set])  # 获取属性的所有可能值
    weighted_entropy = 0.0  # 加权熵的初始值
    for value in values:
        sub_data_set = [example for example in data_set if example[attribute] == value]  # 根据属性值划分子集
        weighted_entropy += (len(sub_data_set) / len(data_set)) * calculate_entropy(sub_data_set)  # 计算加权熵
    info_gain = total_entropy - weighted_entropy  # 计算信息增益
    return info_gain, feature_names[attribute]  # 返回信息增益和属性名称

# 选择最佳分裂特征，即信息增益最大的特征
def choose_best_feature_to_split(data_set, features, feature_names):
    best_feat = None
    max_info_gain = -1
    for feature in features:
        info_gain, _ = calculate_info_gain(data_set, feature, feature_names)  # 计算每个特征的信息增益
        if info_gain > max_info_gain:
            max_info_gain = info_gain
            best_feat = feature
    return best_feat

# 使用ID3算法构建决策树
def id3(data_set, original_data_set, features, feature_names):
    if len(set([example[-1] for example in data_set])) == 1:  # 如果数据集的所有样本都属于同一类别，则停止划分
        return data_set[0][-1]
    if not features:  # 如果没有更多的特征可以用于划分，则返回出现次数最多的类别
        return majority_cnt_label(original_data_set)
    best_feat = choose_best_feature_to_split(data_set, features, feature_names)  # 选择最佳分裂特征
    best_feat_label = feature_names[best_feat]  # 获取最佳分裂特征的名称
    my_tree = {best_feat_label: {}}  # 创建决策树的当前节点
    features = [i for i in features if i != best_feat]  # 移除已经使用的特征

    for value in set([example[best_feat] for example in data_set]):  # 对于最佳分裂特征的每个值
        sub_data_set = [example for example in data_set if example[best_feat] == value]  # 划分子集
        my_tree[best_feat_label][value] = id3(sub_data_set, original_data_set, features, feature_names)  # 递归构建决策树

    return my_tree

# 多数表决类标签，用于处理纯叶子节点的情况
def majority_cnt_label(data_set):
    class_count = {}
    for feat_vec in data_set:
        current_class = feat_vec[-1]
        if current_class not in class_count:
            class_count[current_class] = 0
        class_count[current_class] += 1
    sorted_class_count = sorted(class_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_class_count[0][0]

# 递归构建决策树的可视化图形
def visualize_tree(dot, my_tree, parent=None, edge_label=""):
    if isinstance(my_tree, dict):  # 如果是内部节点
        for key, value in my_tree.items():
            node_label = key
            node_id = str(id(value))
            if parent:
                dot.edge(parent, node_id, label=edge_label)
            dot.node(node_id, node_label)
            for sub_key, sub_tree in value.items():
                visualize_tree(dot, sub_tree, parent=node_id, edge_label=str(sub_key))
    else:  # 如果是叶子节点
        node_id = str(id(my_tree))
        dot.node(node_id, str(my_tree))
        if parent:
            dot.edge(parent, node_id, label=edge_label)

data_set = [
    ['Sunny', 'Hot', 'High', 'Weak', 'No'],
    ['Sunny', 'Hot', 'High', 'Strong', 'No'],
    ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
    ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
    ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
    ['Sunny', 'Mild', 'High', 'Weak', 'No'],
    ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'],
    ['Sunny', 'Mild', 'Normal', 'Strong', 'Yes'],
    ['Overcast', 'Mild', 'High', 'Strong', 'Yes'],
    ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'High', 'Strong', 'No']
]

# 特征名称
feature_names = ['Outlook', 'Temperature', 'Humidity', 'Wind']

# 特征集
features = [0, 1, 2, 3]  # 索引对应天气、温度、湿度、风速

# 构建决策树
my_tree = id3(data_set, data_set, features, feature_names)

# 使用graphviz可视化
dot = Digraph(comment='Decision Tree')
visualize_tree(dot, my_tree)
dot.render('decision_tree', view=True)  # 保存并打开决策树图形
