Now_no = 0


class TreeNode:
    def __init__(self, label, value, parent=None):
        self.label = label
        self.feature = None
        self.value = value
        self.size = 0
        global Now_no
        self.No = str(Now_no)
        Now_no += 1
        self.predict = None
        self.child = []
        self.parent = None
