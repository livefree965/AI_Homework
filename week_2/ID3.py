import csv
import numpy as np
from TreeNode import *
import copy
from graphviz import Digraph
import math


def CalEntropy(dataset: list, method: str):
    size = len(dataset)
    zero_num = 0  # 统计数量
    zero_mark = '0'  # 标志
    for data in dataset:
        if data[-1] == zero_mark:
            zero_num += 1
    p = zero_num / size
    if p == 1 or p == 0:
        return [0, 1 - p]
    if method == 'ID3' or method == 'C4.5':
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


def GetBestFeature(labels: list, dataset, labels_values: list, method: str) -> list:
    """
    :param labels:
    :param dataset:
    :param labels_values:
    :return: 返回一个列表,特征所在位置，对应划分后的熵,以及预测值
    """
    dataset_size = len(dataset)
    if dataset_size == 0:
        return [-1, -1, -1]
    initial_entropy, predict = CalEntropy(dataset, method)  # 未划分的熵
    if initial_entropy == 0:
        return [-1, initial_entropy, predict]
    labels_res = []  # 特征选取后熵的集合
    min_pos = [0, 0, 0]  # 最佳的特征对应的下标，初始化为0,记录对应的熵和预测值
    for label in labels:  # label为取定一个特征开始计算
        pos = labels.index(label)  # pos为特征在列表中的下标
        sum = 0  # 该特征划分后加起来的熵，先设置为0
        splitinfo = 0
        for value in labels_values[pos]:  # 对于该特征可能取的值
            value_dataset = []  # 准备计算该特征某一个值对应划分后的数据集的熵
            for data in dataset:
                if data[pos] == value:  # 如果一条数据符合，则加入数据集
                    value_dataset.append(data)
            if len(value_dataset) != 0:
                entropy, predict = CalEntropy(value_dataset, method)
                sum += len(value_dataset) / dataset_size * entropy  # 计算改特征某一个值的熵，不断相加得到最后的结果
                splitinfo += (-len(value_dataset) / dataset_size) * np.log2(len(value_dataset) / dataset_size)
        sum = initial_entropy - sum
        if method == 'ID3' or method == 'CART':
            if sum > min_pos[1]:  # 如果取得更优的结果，则更新结果
                min_pos = [pos, sum, predict]
            labels_res.append(sum)  # 用于后期数据收集
        elif method == 'C4.5':
            sum /= splitinfo
            if sum > min_pos[1]:  # 如果取得更优的结果，则更新结果
                min_pos = [pos, sum, predict]
            labels_res.append(sum)  # 用于后期数据收集
            pass
    return min_pos


def BulidTree(dataset, pointer: TreeNode, features: list, features_values: list, method: str):
    feature_pos, entropy, predict = GetBestFeature(features, dataset, features_values,
                                                   method)  # 获得最佳的特征下标，对应划分后的熵和划分后预测值
    pointer.predict = predict  # 更新节点预测值,叶子节点的该值为最终预测值
    if entropy == -1:  # 这就说明划分后没有数据返回失败值，该节点不需要建立
        return False
    if feature_pos == -1:  # 这里成
        return True
    pointer.feature = features[feature_pos]
    feature_values = features_values[feature_pos]
    new_features = copy.deepcopy(features)
    new_features_values = copy.deepcopy(features_values)
    new_features.pop(feature_pos)
    new_features_values.pop(feature_pos)
    for label_name in feature_values:
        new_dataset = Remove_Featrue_From_Dataset(FilterDataset(copy.deepcopy(dataset), feature_pos, label_name),
                                                  feature_pos)
        Node = TreeNode(label_name, new_dataset)
        Node.size = len(new_dataset)
        pointer.child.append(Node)
        res = BulidTree(new_dataset, pointer.child[-1], new_features, new_features_values, method)
        if not res:
            pointer.child.pop()
    return True


def BuildFullTree(dataset, features, features_values, method: str):
    Decision_Tree = TreeNode('root', dataset)
    BulidTree(dataset, Decision_Tree, features, features_values, method)
    return Decision_Tree


def Show_tree(decison_Tree: TreeNode, pos, dot, num):
    if decison_Tree.feature == None:
        dot.node(decison_Tree.No, 'Predict: ' + str(int(decison_Tree.predict)))
    else:
        dot.node(decison_Tree.No, 'Feature: ' + str(decison_Tree.feature) + '\n' + 'Predict: ' + str(
            int(decison_Tree.predict)))
    for child in decison_Tree.child:
        dot.node(child.No, str(child.feature) + ' ' + str(child.label), shape='box')
        dot.edge(decison_Tree.No, child.No, child.label)
        Show_tree(child, pos, dot, num)


def Predict(data, tree: TreeNode):
    if len(tree.child) == 0:
        return tree.predict
    else:
        feature_pos = int(tree.feature[7])
        for child in tree.child:
            if child.label == data[feature_pos]:
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
    size = len(dataset)
    valid_start_pos = min(math.floor(size * pos), size)
    valid_end_pos = min(math.floor(size * (pos + percentage)), size)
    train_dataset = []
    valid_dataset = []
    for pos in range(size):
        if pos < valid_start_pos or pos > valid_end_pos:
            train_dataset.append(dataset[pos])
        else:
            valid_dataset.append(dataset[pos])
    return [train_dataset, valid_dataset]


if __name__ == '__main__':
    dataSet, features, features_values = LoadDataset('Car_train.csv')
    for pos in range(8):
        train_dataset, valid_dataset = Split_Dataset(dataSet, 0.12, pos * 0.12)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'ID3')
        ID3_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'C4.5')
        C45_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        Decision_Tree = BuildFullTree(train_dataset, features, features_values, 'CART')
        CART_acc = Predict_Dataset(valid_dataset, Decision_Tree)
        print('Size of train_dataset:', len(train_dataset), '|| Size of vaild_dataset:', len(valid_dataset),
              '|| ID3 acc:', ID3_acc, 'C4.5 acc:', C45_acc, 'CART acc:', CART_acc)
    dot = Digraph(comment='jiajia')
    Show_tree(Decision_Tree, 0, dot, 0)
    # dot.render('test-output/round-table.gv', view=True)
