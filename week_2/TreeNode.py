Now_no = 0


class TreeNode:
    def __init__(self, label, value, parent=None):
        self.label = label  # 父节点选择这个节点，该标签对应的特征的属性值，例如身高属性值中的">170"
        self.feature = None  # 该节点选择的最佳特征，例如一个数据来到该节点，通过判断该特征属性值决定下一个要去的节点
        self.value = value  # 保存了通过该节点的数据，剪枝的时候有用
        self.size = 0  # 节点的数据集的大小，用于可视化，与计算无关
        global Now_no  # 这个是用来可视化的，与计算无关
        self.No = str(Now_no)
        Now_no += 1
        self.predict = None  # 节点的预测值
        self.child = []  # 节点的子节点
        self.parent = None  # 节点的父节点

    def clear_value(self):
        """
        清空节点中原先存储的数据，这是为了后期剪枝做的准备
        :return: None
        """
        self.value = []
        for child in self.child:
            child.clear_value()

    def is_not_leaf(self):
        """
        :return: 判断节点是不是一个叶子，用于剪枝
        """
        return len(self.child) != 0

    def predict_result(self):
        """
        :return: 预测的正确量和错误量，用于剪枝
        """
        res = 0
        for value in self.value:
            if int(value[-1]) == self.predict:
                res += 1
        return [res, len(self.value) - res]

    def r_predict_result(self):
        """
        递归获得该节点下所有子节点预测的正确量和错误量之和
        :return: 所有子节点预测的正确量和错误量，用于剪枝
        """
        if not self.is_not_leaf():
            return self.predict_result()
        else:
            child_right = 0
            child_false = 0
            for child in self.child:
                right, false = child.r_predict_result()
                child_right += right
                child_false += false
            return child_right, child_false

    def need_cut(self):
        """
        对比该节点的预测情况和子节点们预测的情况，决定是否要将其变成叶子
        :return:
        """
        if len(self.value) != 0:
            a = 6
        own_right, own_false = self.predict_result()
        child_right, child_false = self.r_predict_result()
        if own_right >= child_right:
            return True
        else:
            return False
