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
            datas.append({'words': line_words,
                          'label': [line['anger'], line['disgust'], line['fear'], line['joy'], line['sad'],
                                    line['surprise']]})
            for i in datas:
                for j in range(len(i['label'])):
                    i['label'][j] = float(i['label'][j])
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
            datas.append({'words': line_words,
                          'label': [line['anger'], line['disgust'], line['fear'], line['joy'], line['sad'],
                                    line['surprise']]})
            for i in datas:
                for j in range(len(i['label'])):
                    i['label'][j] = float(i['label'][j])
    return datas


def cal_distance(train_exam, test_exam):
    dis = 0
    for key in train_exam.keys():
        if key != 'emotion':
            if train_exam[key] != test_exam[key]:
                dis += (train_exam[key] - test_exam[key]) ** 2
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
    res.sort(key=lambda x: x['distance'])
    emotions = [0] * 5
    for i in range(k):
        for one_emo in range(len(res[i]['emotion'])):
            emotions[one_emo] += res[i]['emotion'][one_emo] / res[i]['distance']
    items = sorted(emotions.items(), key=lambda item: item[1])
    return items[-1][0]


train_data = load_train()
validation_data = load_validation()
train_one_hot_mat = one_hot(train_data)
valid_one_hot_mat = one_hot(validation_data)
# save_one_hot('train_one_hot_mat', train_one_hot_mat)
# save_one_hot('valid_one_hot_mat', valid_one_hot_mat)
# train_one_hot_mat = load_one_hot('train_one_hot_mat')
# valid_one_hot_mat = load_one_hot('valid_one_hot_mat')
all = 0
right = 0
for valid_exam in valid_one_hot_mat:
    all += 1
    neibour = get_distance(valid_exam, train_one_hot_mat)
    res = k_result(5, neibour)
    if valid_exam['emotion'] == res:
        right += 1
        print('yes')
    else:
        print('fuck')
print(right / all)
