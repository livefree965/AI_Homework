import csv
import numpy as np
from TreeNode import *
import copy
from graphviz import Digraph


def CalEntropy(dataset: list):
    size = len(dataset)
    zero_num = 0  # 统计数量
    zero_mark = '0'  # 标志
    for data in dataset:
        if data[-1] == zero_mark:
            zero_num += 1
    p = zero_num / size
    if p == 1 or p == 0:
        return [0, 1 - p]
    return [-p * np.log(p) - (1 - p) * np.log(1 - p), 0 if p > 0.5 else 1]


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


def filterDataset(dataset: list, label_pos, label):
    res = []
    for data in dataset:
        if data[label_pos] == label:
            res.append(data)
    return res


def remove_featrue_from_dataset(dataset: list, pos):
    res = []
    for data in dataset:
        data.remove(data[pos])
        res.append(data)
    return res


def GetBestFeature(labels: list, dataset, labels_values: list) -> list:
    """
    :param labels:
    :param dataset:
    :param labels_values:
    :return: 返回一个列表,特征所在位置，对应划分后的熵,以及预测值
    """
    dataset_size = len(dataset)
    if dataset_size == 0:
        return [-1, -1, -1]
    initial_entropy, predict = CalEntropy(dataset)  # 未划分的熵
    if initial_entropy == 0:
        return [-1, initial_entropy, predict]
    labels_res = []  # 特征选取后熵的集合
    min_pos = [0, initial_entropy, 0]  # 最佳的特征对应的下标，初始化为0,记录对应的熵和预测值
    for label in labels:  # label为取定一个特征开始计算
        pos = labels.index(label)  # pos为特征在列表中的下标
        sum = 0  # 该特征划分后加起来的熵，先设置为0
        for value in labels_values[pos]:  # 对于该特征可能取的值
            value_dataset = []  # 准备计算该特征某一个值对应划分后的数据集的熵
            for data in dataset:
                if data[pos] == value:  # 如果一条数据符合，则加入数据集
                    value_dataset.append(data)
            if len(value_dataset) != 0:
                entropy, predict = CalEntropy(value_dataset)
                sum += len(value_dataset) / dataset_size * entropy  # 计算改特征某一个值的熵，不断相加得到最后的结果
        if sum < min_pos[1]:  # 如果取得更优的结果，则更新结果
            min_pos = [pos, sum, predict]
        labels_res.append(sum)  # 用于后期数据收集
    return min_pos


def BulidTree(dataSet, Pointer: TreeNode, features: list, features_values: list):
    feature_pos, entropy, predict = GetBestFeature(features, dataSet, features_values)
    Pointer.predict = predict
    if entropy == -1:
        return False
    if feature_pos == -1:
        return True
    Pointer.feature = features[feature_pos]
    feature_values = features_values[feature_pos]
    new_features = copy.deepcopy(features)
    new_features_values = copy.deepcopy(features_values)
    new_features.pop(feature_pos)
    new_features_values.pop(feature_pos)
    for label_name in feature_values:
        new_dataset = remove_featrue_from_dataset(filterDataset(copy.deepcopy(dataSet), feature_pos, label_name),
                                                  feature_pos)
        Node = TreeNode(label_name, new_dataset)
        Pointer.child.append(Node)
        res = BulidTree(new_dataset, Pointer.child[-1], new_features, new_features_values)
        if not res:
            Pointer.child.pop()
    return True


def BuildFullTree():
    dataSet, features, features_values = LoadDataset('Car_train.csv')
    Decision_Tree = TreeNode('root', dataSet)
    BulidTree(dataSet, Decision_Tree, features, features_values)
    dot = Digraph(comment='jiajia')
    show_tree(Decision_Tree, 0, dot, 0)
    print(dot.source)
    dot.render('test-output/round-table.gv', view=True)
    return Decision_Tree


def show_tree(Decison_Tree: TreeNode, pos, dot, num):
    dot.node(Decison_Tree.No,
             'Best Feature: ' + str(Decison_Tree.feature) + '\n' + 'Label_name: ' + str(
                 Decison_Tree.label) + '\n' + 'Predict: ' + str(
                 int(Decison_Tree.predict)))
    for child in Decison_Tree.child:
        dot.node(child.No, str(child.feature) + ' ' + str(child.label))
        dot.edge(Decison_Tree.No, child.No)
        show_tree(child, pos, dot, num)


def predict(data, Tree: TreeNode):
    if len(Tree.child) == 0:
        return Tree.predict
    else:
        feature_pos = int(Tree.feature[7])
        for child in Tree.child:
            if child.label == data[feature_pos]:
                return predict(data, child)


def predict_dataset(dataset, Tree):
    bingo = 0
    for data in dataset:
        predict_value = predict(data, Tree)
        if predict_value == int(data[-1]):
            bingo += 1
    return bingo / len(dataset)


Decision_Tree = BuildFullTree()
dataSet, features, features_values = LoadDataset('Car_train.csv')
p = predict_dataset(dataSet, Decision_Tree)
print(p)
a = 6
