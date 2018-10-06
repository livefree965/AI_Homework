import csv
import copy
import math
import json
import numpy as np

unique_word = {}


def load_dataset(filename):
    with open(filename) as f:
        datas = []
        f_csv = csv.DictReader(f)
        for line in f_csv:
            line_words = [line['tezheng1'], line['tezheng2'], line['tezheng3'], line['tezheng4'], line['tezheng5']]
            for word in line_words:
                unique_word[word] = 0
            datas.append({'words': line_words, 'label': line['label']})
    return datas


def one_hot(datas):
    tf_mat = []
    for data in datas:
        data_row = copy.deepcopy(unique_word)
        for word in data['words']:
            data_row[word] += 1
        data_row['emotion'] = data['label']
        tf_mat.append(data_row)
    return tf_mat


def cal_distance(train_exam, test_exam):
    x = []
    y = []
    for key in train_exam.keys():
        if key != 'emotion':
            x.append(train_exam[key])
            y.append(test_exam[key])
    x = np.array(x)
    y = np.array(y)
    dis = np.linalg.norm(x - y)
    return dis


def get_distance(test_exam, train_data):
    res = []
    for train_exam in train_data:
        one_data = {}
        one_data['distance'] = cal_distance(train_exam, test_exam)
        one_data['emotion'] = train_exam['emotion']
        res.append(one_data)
    return res


def k_result(k, res):
    res.sort(key=lambda x: x['distance'])  # 排序来获取最近的邻居
    emotions = {}
    for i in range(k):  # 统计前k个邻居的情绪情况
        if res[i]['emotion'] in emotions:
            emotions[res[i]['emotion']] += 1
        else:
            emotions[res[i]['emotion']] = 1
    items = sorted(emotions.items(), key=lambda item: item[1])  # 对这些情绪排序，取众数最大的
    return items[-1][0]


def save_to_csv(filename, rowdata):
    with open(filename, 'a') as f:
        f_csv = csv.writer(f, lineterminator='\n')
        f_csv.writerow(rowdata)


train_data = load_dataset('train_beta.csv')
validation_data = load_dataset('valid_beta.csv')
train_one_hot_mat = one_hot(train_data)
valid_one_hot_mat = one_hot(validation_data)
all = 0
right = 0
print(len(valid_one_hot_mat))
for valid_exam in valid_one_hot_mat:
    all += 1
    neibour = get_distance(valid_exam, train_one_hot_mat)
    res = k_result(2, neibour)
    # save_to_csv('res.csv', [res])
    print(res)

# for k in range(1, 21):
#     all = 0
#     right = 0
#     print("K:", k)
#     for valid_exam in valid_one_hot_mat:
#         all += 1
#         neibour = get_distance(valid_exam, train_one_hot_mat)
#         res = k_result(k, neibour)
#         print(res)
#     print(right / all)
