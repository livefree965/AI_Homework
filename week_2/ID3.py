import csv
import numpy as np
from TreeNode import *
import copy
from graphviz import Digraph
import math
import csv


def CalEntropy(dataset: list, method: str):
    """
    :param dataset: 计算的数据集
    :param method: 熵的算法
    :return: 熵和预测值（多数投票原则）
    """
    size = len(dataset)
    zero_num = 0  # 统计结果为0的数据数量
    zero_mark = '0'  # 结果为0的标志，这是文件读进来最后一个结果默认为字符
    for data in dataset:
        if data[-1] == zero_mark:
            zero_num += 1
    p = zero_num / size  # 计算为0的概率
    if p == 1 or p == 0:  # 因为涉及到取对数，这种情况直接返回结果防止inf出现
        return [0, 1 - p]
    if method == 'ID3' or method == 'C4.5':  # 根据定义返回结果
        return [-p * np.log2(p) - (1 - p) * np.log2(1 - p), 0 if p >= 0.5 else 1]
    else:
        return [1 - p ** 2 - (1 - p) ** 2, 0 if p >= 0.5 else 1]


def LoadDataset(filename):
    dataSet = []
    with open(filename) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            dataSet.append(row)
    labels = []
    for i in range(len(dataSet[0]) - 1):
        labels.append('feature' + str(i))
    labels_values = []
    for i in labels:
        labels_values.append([])
    for data in dataSet:
        for pos in range(len(data) - 1):
            if data[pos] not in labels_values[pos]:
                labels_values[pos].append(data[pos])
    return dataSet, labels, labels_values


def FilterDataset(dataset: list, label_pos, label):
    res = []
    for data in dataset:
        if data[label_pos] == label:
            res.append(data)
    return res


def Remove_Featrue_From_Dataset(dataset: list, pos):
    res = []
    for data in dataset:
        data.pop(pos)
        res.append(data)
    return res


def GetBestFeature(features: list, dataset, features_values: list, method: str) -> list:
    """
    :param features: 特征的集合
    :param dataset: 数据集
    :param features_values: 特征的属性值的集合，为一个二层嵌套集合
    :return: 返回一个列表,特征所在位置，对应划分后的熵,以及预测值
    """
    dataset_size = len(dataset)
    if dataset_size == 0:  # 没有数据，返回-1
        return [-1, -1, -1]
    initial_entropy, predict = CalEntropy(dataset, method)  # 未划分的熵
    if initial_entropy == 0:  # 说明数据集所有结果相同，不需要进一步分子节点
        return [-1, initial_entropy, predict]
    features_res = []  # 特征选取后熵的集合
    min_pos = [0, 0, 0]  # 最佳的特征对应的下标，初始化为0,记录对应的熵和预测值
    for feature in features:  # feature为取定一个特征开始计算
        pos = features.index(feature)  # pos为特征在列表中的下标
        sum = 0  # 该特征划分后加起来的熵，先设置为0
        splitinfo = 0
        for value in features_values[pos]:  # 对于该特征可能取的属性值
            value_dataset = []  # 准备计算该特征某属性值对应划分后的数据集的熵
            for data in dataset:
                if data[pos] == value:  # 如果一条数据符合，则加入数据集
                    value_dataset.append(data)
            if len(value_dataset) != 0:
                entropy, predict = CalEntropy(value_dataset, method)
                sum += len(value_dataset) / dataset_size * entropy  # 计算该特征某一个值的熵，根据公式不断相加得到最后的结果
                splitinfo += (-len(value_dataset) / dataset_size) * np.log2(len(value_dataset) / dataset_size)
        sum = initial_entropy - sum
        if method == 'ID3' or method == 'CART':
            if sum > min_pos[1]:  # 如果取得更优的结果，则更新结果
                min_pos = [pos, sum, predict]
            features_res.append(sum)  # 用于后期数据收集
        elif method == 'C4.5':
            sum /= splitinfo
            if sum > min_pos[1]:  # 如果取得更优的结果，则更新结果
                min_pos = [pos, sum, predict]
            features_res.append(sum)  # 用于后期数据收集
    return min_pos


def BulidTree(dataset, pointer: TreeNode, features: list, features_values: list, method: str):
    """
    :param dataset: 该节点数据集
    :param pointer: 目前指针指向的节点
    :param features: 特征集合
    :param features_values: 二层及格，特征的属性值集合
    :param method: 算法名
    :return: 节点需要建立则返回True
    """
    feature_pos, entropy, predict = GetBestFeature(features, dataset, features_values,
                                                   method)  # 获得最佳的特征下标，对应划分后的熵和划分后预测值
    pointer.predict = predict  # 更新节点预测值,叶子节点的该值为最终预测值
    if entropy == -1:  # 这就说明划分后本节点对应属性值没有数据返回失败值，该节点不需要建立
        return False
    if feature_pos == -1:  # 这里说明数据集结果已经完全一致，不需要继续建立子节点来进一步分割数据集
        return True
    pointer.feature = features[feature_pos]  # 该节点选取的下一步划分的特征
    feature_values = features_values[feature_pos]
    new_features = copy.deepcopy(features)
    new_features_values = copy.deepcopy(features_values)
    # 这一步是为了避免修改到传入的参数
    new_features.pop(feature_pos)
    new_features_values.pop(feature_pos)
    # 从列表中删除这个特征
    for label_name in feature_values:
        # 获得属性值在数据集中对应的数据
        new_dataset = Remove_Featrue_From_Dataset(FilterDataset(copy.deepcopy(dataset), feature_pos, label_name),
                                                  feature_pos)
        Node = TreeNode(label_name, new_dataset)
        Node.size = len(new_dataset)
        Node.parent = pointer
        pointer.child.append(Node)
        # 添加这个属性值到子节点中去
        res = BulidTree(new_dataset, pointer.child[-1], new_features, new_features_values, method)
        # 递归建立树
        if not res:  # 说明节点不需要建立，删除之
            pointer.child.pop()
    return True


def BuildFullTree(dataset, features, features_values, method: str):
    Decision_Tree = TreeNode('root', dataset)
    BulidTree(dataset, Decision_Tree, features, features_values, method)
    return Decision_Tree


def Show_tree(decison_Tree: TreeNode, pos, dot, num):
    """
    递归方式可视化一棵树
    :param decison_Tree: 当前所在节点
    :param pos: 深度
    :param dot: graph实例
    :param num: 计算层数，可视化进行上色（这个最后没用）
    :return:
    """
    # 输出的标签
    predict_output = 'Predict: ' + str(int(decison_Tree.predict))
    size_output = 'Data_Size: ' + str(len(decison_Tree.value)) + '\n'
    feature_output = 'Feature: ' + str(decison_Tree.feature) + '\n'
    if decison_Tree.feature == None:
        dot.node(decison_Tree.No, size_output + predict_output)
    else:
        dot.node(decison_Tree.No, feature_output + size_output + predict_output)
    for child in decison_Tree.child:
        dot.node(child.No, str(child.feature) + ' ' + str(child.label), shape='box')
        # 创建子节点
        dot.edge(decison_Tree.No, child.No, child.label)
        # 到子节点的连线
        Show_tree(child, pos, dot, num)


def Predict(data, tree: TreeNode):
    """
    递归预测结果
    :param data: 数据
    :param tree: 当前节点
    :return: 预测结果
    """
    if len(tree.child) == 0:  # 到叶子了返回结果
        return tree.predict
    else:
        feature_pos = int(tree.feature[7])
        for child in tree.child:
            if child.label == data[feature_pos]:  # 如果子节点标签符合，进入下一个节点
                return Predict(data, child)
    return tree.predict


def Predict_Dataset(dataset, tree):
    bingo = 0
    for data in dataset:
        predict_value = Predict(data, tree)
        if predict_value == int(data[-1]):
            bingo += 1
    return bingo / len(dataset)


def Split_Dataset(dataset, percentage, pos):
    """
    划分数据集，取一部分为验证集，其余为训练集
    :param dataset: 未划分数据集
    :param percentage: 验证集的比例
    :param pos: 验证集在原始数据集的起始位置
    :return: 训练集和验证集
    """
    size = len(dataset)
    valid_start_pos = min(math.floor(size * pos), size)  # 避免越界
    valid_end_pos = min(math.floor(size * (pos + percentage)), size)
    train_dataset = []
    valid_dataset = []
    for pos in range(size):
        if pos < valid_start_pos or pos > valid_end_pos:
            train_dataset.append(dataset[pos])
        else:
            valid_dataset.append(dataset[pos])
    return [train_dataset, valid_dataset]


def Post_Pruning(tree: TreeNode):
    """
    后剪枝算法
    :param tree: 当前所在节点
    :return:
    """
    for child in tree.child:
        Post_Pruning(child)  # 树的后序遍历
    if tree.is_not_leaf():  # 如果不是叶子节点
        res = tree.need_cut()  # 判断是否需要剪枝
        if res == True:
            tree.child = []  # 子节点清空
    return


def Insert_Dataset_Tree(dataset, tree: TreeNode):
    for data in dataset:
        Insert_ValidData_Tree(data, tree)


def Insert_ValidData_Tree(data, tree: TreeNode):
    tree.value.append(data)
    if len(tree.child) == 0:
        return
    else:
        feature_pos = int(tree.feature[7])
        for child in tree.child:
            if child.label == data[feature_pos]:
                Insert_ValidData_Tree(data, child)
    return


def Save_Tree_to_Pdf(filename, tree: TreeNode):
    dot = Digraph(comment='jiajia')
    Show_tree(tree, 0, dot, 0)
    dot.render('test-output/' + filename, view=True)


if __name__ == '__main__':
    dataSet, features, features_values = LoadDataset('Car_train.csv')
    for pos in range(4):
        train_dataset, valid_dataset = Split_Dataset(dataSet, 0.2, pos * 0.2)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'ID3')
        ID3_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'C4.5')
        C45_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'CART')
        CART_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        print('Size of train_dataset:', len(train_dataset), '|| Size of vaild_dataset:', len(valid_dataset),
              '|| ID3 acc:', ID3_acc, 'C4.5 acc:', C45_acc, 'CART acc:', CART_acc)
    for pos in range(4):
        train_dataset, valid_dataset = Split_Dataset(dataSet, 0.2, pos * 0.2)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'ID3')
        Raw_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        Decision_Tree.clear_value()
        Insert_Dataset_Tree(valid_dataset, Decision_Tree)
        Post_Pruning(Decision_Tree)
        Cut_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        print("Raw acc:", Raw_acc, "Cut acc:", Cut_acc)
    dataSet, features, features_values = LoadDataset('Car_train.csv')
    Decision_Tree = BuildFullTree(dataSet, features, features_values, 'ID3')
    # Save_Tree_to_Pdf('final.gv', Decision_Tree)
    dataSet, features, features_values = LoadDataset('Car_test.csv')
    for data in dataSet:
        res = Predict(data, Decision_Tree)
        with open('res.csv', 'a') as f:
            f_csv = csv.writer(f, lineterminator='\n')
            f_csv.writerow([int(res)])
# dot.render('test-output/round-table.gv', view=True)
