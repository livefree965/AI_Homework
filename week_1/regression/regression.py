import csv
import copy
import math
import json
import numpy as np

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


def load_valid_mat():
    with open('validation_set.csv') as f:
        datas = []
        f_csv = csv.DictReader(f)
        for line in f_csv:
            datas.append([line['anger'], line['disgust'], line['fear'], line['joy'], line['sad'],
                          line['surprise']])
    return datas


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
    emotions = {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sad': 0, 'surprise': 0}
    emotions_map = ['anger', 'disgust', 'fear', 'joy', 'sad', 'surprise']
    for i in range(k):
        for one_emo in range(6):
            try:
                emotions[emotions_map[one_emo]] += res[i]['emotion'][one_emo] / res[i]['distance']
            except:
                a = 6
    emotion_sum = sum(emotions.values())
    for key in emotions_map:
        emotions[key] = emotions[key] / emotion_sum
    return emotions


train_data = load_train()
validation_data = load_validation()
train_one_hot_mat = one_hot(train_data)
valid_one_hot_mat = one_hot(validation_data)
# save_one_hot('train_one_hot_mat', train_one_hot_mat)
# save_one_hot('valid_one_hot_mat', valid_one_hot_mat)
# train_one_hot_mat = load_one_hot('train_one_hot_mat')
# valid_one_hot_mat = load_one_hot('valid_one_hot_mat')
predict_mat = []
valid_mat = load_valid_mat()
for valid_exam in valid_one_hot_mat:
    neibour = get_distance(valid_exam, train_one_hot_mat)
    res = k_result(5, neibour)
    items = sorted(res.items(), key=lambda item: item[1])
    predict_mat.append(list(res.values()))
x = np.array(predict_mat)
y = np.array(valid_mat).T
print(np.cov(x, y) / np.sqrt(np.var(x) * np.var(y)))
