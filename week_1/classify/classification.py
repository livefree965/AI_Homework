import csv
import copy
import math
import json

unique_word = {}


def save_one_hot(filename, data):
    with open(filename, 'w') as f:
        json.dump({'datas': data}, f)


def load_one_hot(filename):
    with open(filename) as f:
        res = json.load(filename)
    return res['datas']


def load_train():
    with open('train_set.csv') as f:
        datas = []
        f_csv = csv.DictReader(f)
        for line in f_csv:
            line_words = line['Words (split by space)'].split(' ')
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


def load_validation():
    with open('validation_set.csv') as f:
        datas = []
        f_csv = csv.DictReader(f)
        for line in f_csv:
            line_words = line['Words (split by space)'].split(' ')
            for word in line_words:
                unique_word[word] = 0
            datas.append({'words': line_words, 'label': line['label']})
    return datas


def load_test():
    with open('test_set.csv') as f:
        datas = []
        f_csv = csv.DictReader(f)
        for line in f_csv:
            line_words = line['Words (split by space)'].split(' ')
            for word in line_words:
                unique_word[word] = 0
            datas.append({'words': line_words, 'label': line['label']})
    return datas


def cal_distance(train_exam, test_exam):
    dis = 0
    for key in train_exam.keys():
        if key != 'emotion':
            if train_exam[key] != test_exam[key]:
                dis += (train_exam[key] - test_exam[key])**2
    dis = math.sqrt(dis)
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
    res.sort(key=lambda x: x['distance'])   #排序来获取最近的邻居
    emotions = {}
    for i in range(k):  #统计前k个邻居的情绪情况
        if res[i]['emotion'] in emotions:
            emotions[res[i]['emotion']] += 1
        else:
            emotions[res[i]['emotion']] = 1
    items = sorted(emotions.items(), key=lambda item: item[1]) #对这些情绪排序，取众数最大的
    return items[-1][0]


train_data = load_train()
validation_data = load_validation()
test_data = load_test()
train_one_hot_mat = one_hot(train_data)
valid_one_hot_mat = one_hot(validation_data)
test_one_hot_mat = one_hot(test_data)
# save_one_hot('train_one_hot_mat', train_one_hot_mat)
# save_one_hot('valid_one_hot_mat', valid_one_hot_mat)
# train_one_hot_mat = load_one_hot('train_one_hot_mat')
# valid_one_hot_mat = load_one_hot('valid_one_hot_mat')
all = 0
right = 0
# print(len(test_one_hot_mat))
# for valid_exam in test_one_hot_mat:
#     all += 1
#     neibour = get_distance(valid_exam, train_one_hot_mat)
#     res = k_result(5, neibour)
#     with open('res.csv', 'a') as f:
#         f_csv = csv.writer(f, lineterminator='\n')
#         f_csv.writerow([res])
#     print(all)
for k in range(1, 21):
    all = 0
    right = 0
    print("K:", k)
    for valid_exam in valid_one_hot_mat:
        all += 1
        neibour = get_distance(valid_exam, train_one_hot_mat)
        res = k_result(k, neibour)
        if valid_exam['emotion'] == res:
            right += 1
        else:
            pass
    print(right / all)
