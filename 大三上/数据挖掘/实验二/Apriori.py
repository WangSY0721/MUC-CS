import random

# 生成数据集
def loadDataSet():
    items = ['洗发水', '肥皂', '毛巾', '牙膏', '洗洁精', '洗衣粉', '卫生纸', '沐浴露', '洗面奶']
    num_transactions = 10  # 事务的数量
    avg = 3  # 事务中项的平均数量
    dataset = []
    for _ in range(num_transactions):
        num_items = random.randint(avg // 2, avg * 3 // 2)  # 随机选择项的数量
        transaction = random.sample(items, num_items)  # 随机选择项
        dataset.append(transaction)
    for i, transaction in enumerate(dataset[:10]):
        print(f"事务 {i + 1}: {transaction}")
    return dataset

# 从给定的数据集中创建候选1项集
def create_initial_candidates(data_set):
    candidate_items = []
    for transaction in data_set:
        for item in transaction:
            if [item] not in candidate_items:  # 去重
                candidate_items.append([item])
    candidate_items.sort()
    return list(map(frozenset, candidate_items))  # 将列表转化为frozenset集合，作为候选项集

# D：数据集，Ck：候选集，minSupport：最小支持度
# 扫描数据集，计算频繁项集
def scanD(D, Ck, minSupport):
    ssCnt = {}  # 存储每个候选项集的计数
    for tid in D:
        for can in Ck:
            if can.issubset(tid):  # 如果候选项集是事务的子集
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1

    numItems = float(len(D))
    Lk = []  # 存储满足最小支持度的频繁项集
    supportData = {}  # 存储每个候选项集的支持度

    for key in ssCnt:
        support = ssCnt[key] / numItems  # 计算支持度
        if support >= minSupport:
            Lk.append(key)
        supportData[key] = support
    return Lk, supportData  # 返回频繁项集和支持度数据

# 根据频繁(k-1)项集生成候选k项集，并进行剪枝
def aprioriGen(Lk_1, k):
    Ck = []  # 存储生成的候选k项集
    lenLk = len(Lk_1)
    for i in range(lenLk):
        L1 = Lk_1[i]
        for j in range(i + 1, lenLk):
            L2 = Lk_1[j]
            if len(L1 & L2) == k - 2:  # 如果两个项集的前k-2个项相同
                Ck_candidate = L1 | L2
                # 剪枝过程：检查候选项集的每个(k-1)子集是否都是频繁的
                if has_infrequent_subset(Ck_candidate, Lk_1):
                    continue
                Ck.append(Ck_candidate)
    return Ck

# 检查候选项集的每个(k-1)子集是否都是频繁的
def has_infrequent_subset(Ck_candidate, Lk_1):
    for subset in subsets(Ck_candidate):
        if subset not in Lk_1:
            return True  # 发现不频繁的子集，剪枝
    return False

# 生成所有k项集的子集
def subsets(Ck_candidate):
    return [frozenset(Ck_candidate - {item}) for item in Ck_candidate]

# Apriori算法主流程
def apriori(dataSet, minSupport):
    C1 = create_initial_candidates(dataSet)  # 创建候选1项集
    L1, supportData = scanD(dataSet, C1, minSupport)  # 获取频繁1项集
    L = [L1]  # 存储所有频繁项集
    k = 2  # 从2项集开始
    while len(L[k - 2]) > 0:
        Lk_1 = L[k - 2]  # 获取频繁(k-1)项集
        Ck = aprioriGen(Lk_1, k)  # 生成候选k项集
        if len(Ck) == 0:
            break
        Lk, supK = scanD(dataSet, Ck, minSupport)  # 获取频繁k项集
        supportData.update(supK)  # 更新支持度数据
        L.append(Lk)  # 将频繁k项集添加到L中
        k += 1

    return L, supportData

# 从频繁项集中生成满足最小置信度的关联规则
def generateRules(L, supportData, minConf):
    bigRuleList = []  # 存储所有生成的规则
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]  # 频繁项集中的每个元素作为单独的后件
            calcConf(freqSet, H1, supportData, bigRuleList, minConf)  # 计算置信度并生成规则
    return bigRuleList

# 计算置信度并生成规则
def calcConf(freqSet, H, supportData, brl, minConf):
    prunedH = []  # 存储满足最小置信度的后件
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]  # 计算置信度
        if conf >= minConf:
            print(f"{freqSet - conseq} --> {conseq} conf: {conf}")
            brl.append((freqSet - conseq, conseq, conf))  # 存储规则
            prunedH.append(conseq)  # 保留满足置信度的后件
    return prunedH


if __name__ == "__main__":
    dataset = loadDataSet()  # 加载数据集
    L, supportData = apriori(dataset, 0.2)  # 执行Apriori算法，最小支持度为0.2
    rules = generateRules(L, supportData, 0.7)  # 生成置信度大于等于0.7的关联规则
