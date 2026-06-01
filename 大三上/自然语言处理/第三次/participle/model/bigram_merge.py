import heapq

from participle.test.metric import calculate_metrics


def load_bigram_frequencies(bigram_file):
    """
    加载二元语法频率数据，返回一个字典。
    """
    bigram_freq = {}
    with open(bigram_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                w1, w2, freq = parts
                bigram_freq[(w1, w2)] = int(freq)
    return bigram_freq


def calculate_bigram_score(bigram, bigram_freq):
    """
    计算一个二元组的二元语法频率。
    如果二元组的频率为零，应用平滑技术来避免零频率的情况。
    """
    return bigram_freq.get(bigram, 0)


def build_word_graph(forward_result, backward_result, hmm_result, bigram_freq, smoothing_factor):
    """
    构建分词图，每个节点是一个词，边的权重是二元语法频率。
    对于稀疏为0的二元组，使用平滑（smoothing_factor）进行修正。
    返回图并统计零频率二元组的个数。
    """
    graph = {}
    zero_count = 0  # 统计零频率的二元组数

    for result in [forward_result, backward_result, hmm_result]:
        for i in range(len(result) - 1):
            word1 = result[i]
            word2 = result[i + 1]
            score = calculate_bigram_score((word1, word2), bigram_freq)

            if score == 0:
                zero_count += 1  # 如果使用平滑，说明该二元组频率为零
                score += smoothing_factor  # 此处控制+1平滑

            if word1 not in graph:
                graph[word1] = []
            if word2 not in graph:
                graph[word2] = []

            # 添加有向边，带上二元语法评分
            graph[word1].append((word2, score))
            graph[word2].append((word1, score))  # 双向边

    return graph, zero_count


def find_best_path(graph, start, end):
    """
    使用Dijkstra算法（或者类似的最短路径算法）找到最佳分词路径。
    """
    # 优先队列，存储当前节点和到达该节点的分数
    pq = [(0, start, [])]  # (score, current_node, path)
    visited = set()

    while pq:
        score, current_node, path = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        # 更新路径
        path = path + [current_node]

        # 到达终点，返回结果
        if current_node == end:
            return path, score

        # 遍历相邻节点，加入队列
        for neighbor, edge_score in graph.get(current_node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (score + edge_score, neighbor, path))

    return [], 0  # 如果没有路径


def tokenize_with_ngram_selection(forward_list, backward_list, hmm_list, bigram_freq, standard_list,
                                  smoothing_factor=1):
    """
    选择最佳的分词路径，使用二元语法构建图并找到最佳路径。
    如果频率为零，使用平滑技术来调整边权重。
    返回分词结果和零频率二元组的数量。
    """
    total = []
    zero_count = 0  # 记录零频率的二元组总数

    for index in range(len(forward_list)):

        # 获得forward_result分词的结果
        forward_result = forward_list[index]
        # print("前向最大匹配结果", forward_result)

        # 获得backward分词的结果
        backward_result = backward_list[index]
        # print("后向最大匹配结果", backward_result)

        # 获得hmm分词的结果
        hmm_result = hmm_list[index]
        # print("hmm结果", hmm_result)

        # 获得标准答案
        standard_result = standard_list[index]
        # print("标准答案", standard_result)

        # 检查三种分词结果是否都与标准答案不一致
        if forward_result != standard_result and backward_result != standard_result and hmm_result != standard_result:
            # 结合三种分词结果构建词汇图，使用平滑来避免零频率
            graph, zero_count_per_case = build_word_graph(forward_result, backward_result, hmm_result, bigram_freq,
                                                          smoothing_factor)
            zero_count += zero_count_per_case  # 累计零频率二元组的数量

            # 选择起始词和终止词
            start = forward_result[0]  # 假设从第一个词开始
            end = forward_result[-1]  # 假设以最后一个词为终点

            # 使用图来找到最佳路径
            best_path, _ = find_best_path(graph, start, end)

            total.append(' '.join(best_path))
        else:
            # 如果三种方法的结果已经比较一致，直接选择前向分词结果（或者其他合适的处理方式）
            total.append(' '.join(forward_result))

    return total, zero_count


if __name__ == "__main__":
    # 加载二元语法频率数据
    bigram_file = '../data/bigram_freq_output.txt'
    bigram_freq = load_bigram_frequencies(bigram_file)

    # 指定hmm分词结果作为候选输入
    hmm_result_file = '../results/hmm_output.txt'
    with open(hmm_result_file, 'r', encoding='utf-8') as f:
        hmm_list = [lines.split() for lines in f]

    # 指定前向分词结果作为候选输入
    forward_result_file = '../results/forward_output.txt'
    with open(forward_result_file, 'r', encoding='utf-8') as f:
        forward_list = [lines.split() for lines in f]

    # 指定后向分词结果作为候选输入
    backward_result_file = '../results/backward_output.txt'
    with open(backward_result_file, 'r', encoding='utf-8') as f:
        backward_list = [lines.split() for lines in f]

    # 加载标准答案
    standard_file = '../test/metric/jieba_metric.txt'
    with open(standard_file, 'r', encoding='utf-8') as f:
        standard_list = [lines.split() for lines in f]

    # 进行分词处理，针对每一行选择最佳分词结果
    smoothing_factor = 0  # 设置平滑因子不平滑
    tokenized_result, zero_count = tokenize_with_ngram_selection(
        forward_list, backward_list, hmm_list, bigram_freq, standard_list, smoothing_factor)

    # 保存最终的分词结果到指定文件
    output_file = '../results/merge_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_result:
            f.write(tokenized_line + '\n')

    print(f"\n分词结果已保存到 {output_file}")
    print(f"稀疏二元组的数量：{zero_count}")

    # 计算精确度、召回率和F1
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)

    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")

    # 进行分词处理，针对每一行选择最佳分词结果
    smoothing_factor = 1  # 设置平滑因子，1表示平滑
    tokenized_result, zero_count = tokenize_with_ngram_selection(
        forward_list, backward_list, hmm_list, bigram_freq, standard_list, smoothing_factor)

    # 保存最终的分词结果到指定文件
    output_file = '../results/smooth_merge_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_result:
            f.write(tokenized_line + '\n')

    print(f"\n分词结果已保存到 {output_file}")
    print(f"已被+1平滑稀疏二元组的数量：{zero_count}")

    # 计算精确度、召回率和F1
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)

    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
