import copy


class VariableElimination:
    @staticmethod
    def inference(factor_list, query_variables,
                  ordered_list_of_hidden_variables, evidence_list):
        # 对evidence进行消除
        for ev in evidence_list:  # 对每一个evidence进行处理
            VariableElimination.print_factors(factor_list)
            new_factor_list = []  # 存放不影响的节点
            tmp_factor_list = []  # 存放影响的节点
            for factor in factor_list:
                if ev in factor.var_list:  # 与evidence相关
                    tmp_factor_list.append(factor)
                else:  # 与evidence无关
                    new_factor_list.append(factor)
            for factor in tmp_factor_list[1:]:  # 将相关变量相乘，求出新的概率
                tmp_factor_list[0] = tmp_factor_list[0].multiply(factor)  # 相乘
            new_factor_list.append(tmp_factor_list[0].restrict(ev, evidence_list[ev]))  # 消去相关的变量并加入回列表中
            factor_list = new_factor_list  # 赋值，对下一个evidence进行处理
            # Your code here
        for var in ordered_list_of_hidden_variables:
            new_factor_list = []
            tmp_factor_list = []
            for factor in factor_list:
                if var in factor.var_list:
                    tmp_factor_list.append(factor)
                else:
                    new_factor_list.append(factor)
            for factor in tmp_factor_list[1:]:
                tmp_factor_list[0] = tmp_factor_list[0].multiply(factor)
            new_factor_list.append(tmp_factor_list[0].sum_out(var))  # 同上，逐个消去变量
            factor_list = new_factor_list
            # Your code here
        print("RESULT: ")
        res = factor_list[0]
        for factor in factor_list[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v / total for k, v in res.cpt.items()}
        res.print_inf()

    @staticmethod
    def print_factors(factor_list):
        for factor in factor_list:
            factor.print_inf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')

    @staticmethod
    def get_union(left: list, right: list):
        return list(set(left).union(set(right)))


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.var_list = var_list
        self.cpt = {}

    def set_cpt(self, cpt):
        self.cpt = cpt

    def print_inf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.var_list))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def multiply(self, factor):
        # tmp_list = ['B', 'E', 'A', 'J', 'M']
        tmp_list = Util.get_union(self.var_list, factor.var_list)
        new_list = []
        new_mark = []
        for var in tmp_list:
            new_list.append(var)
            if var in self.var_list and var in factor.var_list:
                new_mark.append(0)
            elif var in self.var_list:
                new_mark.append(1)
            else:
                new_mark.append(2)
        new_cpt = {}
        for key_1 in self.cpt.keys():
            for key_2 in factor.cpt.keys():
                matched = True
                tmp_key = ''
                for i in range(len(new_list)):
                    if new_mark[i] == 0:
                        if key_1[self.var_list.index(new_list[i])] == key_2[factor.var_list.index(new_list[i])]:
                            tmp_key += key_1[self.var_list.index(new_list[i])]
                        else:
                            matched = False
                            break
                    elif new_mark[i] == 1:
                        tmp_key += key_1[self.var_list.index(new_list[i])]
                    else:
                        tmp_key += key_2[factor.var_list.index(new_list[i])]
                if not matched:
                    continue
                new_cpt[tmp_key] = self.cpt[key_1] * factor.cpt[key_2]
        '''function that multiplies with another factor'''
        # Your code here
        new_node = Node('f' + str(new_list), new_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def sum_out(self, variable):
        var_i = 0
        new_var_list = []
        for i in range(len(self.var_list)):
            if self.var_list[i] != variable:
                new_var_list.append(self.var_list[i])
            else:
                var_i = i
        new_cpt = {}
        for key in self.cpt.keys():
            tmp_key = key[:var_i] + key[var_i + 1:]
            if tmp_key in new_cpt.keys():
                continue
            new_cpt[tmp_key] = 0
            for sec_key in self.cpt.keys():
                if sec_key[:var_i] + sec_key[var_i + 1:] == tmp_key:
                    new_cpt[tmp_key] += self.cpt[sec_key] / 2
        '''function that sums out a variable given a factor'''
        # Your code here
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        var_i = 0
        new_var_list = []
        for i in range(len(self.var_list)):
            if self.var_list[i] != variable:
                new_var_list.append(self.var_list[i])
            else:
                var_i = i
        new_cpt = {}
        for key in self.cpt:
            if key[var_i] == str(value):
                tmp_key = key[:var_i] + key[var_i + 1:]
                new_cpt[tmp_key] = self.cpt[key] * 2
        '''function that restricts a variable to some value
        in a given factor'''
        # Your code here
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node


# Create nodes for Bayes Net
B = Node('B', ['B'])
E = Node('E', ['E'])
A = Node('A', ['A', 'B', 'E'])
J = Node('J', ['J', 'A'])
M = Node('M', ['M', 'A'])

# Generate cpt for each node
B.set_cpt({'0': 0.999, '1': 0.001})
E.set_cpt({'0': 0.998, '1': 0.002})
A.set_cpt({'111': 0.95, '011': 0.05, '110': 0.94, '010': 0.06,
           '101': 0.29, '001': 0.71, '100': 0.001, '000': 0.999})
J.set_cpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
M.set_cpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})

print("P(A) **********************")
VariableElimination.inference([B, E, A, J, M], ['A'], ['B', 'E', 'J', 'M'], {})

print("P(B | J, ~M) **********************")
VariableElimination.inference([B, E, A, J, M], ['B'], ['E', 'A'], {'J': 1, 'M': 0})

print("P(A | J, ~M) **********************")
VariableElimination.inference([B, E, A, J, M], ['A'], ['E', 'B'], {'J': 1, 'M': 0})

print("P(B | A) **********************")
VariableElimination.inference([B, E, A, J, M], ['B'], ['E', 'J', 'M'], {'A': 1})

print("P(J, ~M | ~B) **********************")
VariableElimination.inference([B, E, A, J, M], ['J', '~M'], ['E', 'A'], {'B': 0})
