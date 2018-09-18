import csv
import copy
import math

unique_word = {}
with open("semeval.txt") as f:
    datas = []
    for line in f.readlines():
        line_words = line.split('\t')[2].replace('\n', '').split(' ')
        for word in line_words:
            unique_word[word] = 0
        datas.append(line_words)
sentence_size = len(datas)
word_appear_page = copy.deepcopy(unique_word)
tf_mat = []
for data in datas:
    data_row = copy.deepcopy(unique_word)
    size = len(data)
    word_appear = {}
    for word in data:
        if word not in word_appear.keys():
            word_appear_page[word] += 1
        word_appear[word] = 1
        data_row[word] += 1 / size
    tf_mat.append(data_row)
idf_mat = copy.deepcopy(unique_word)
for word in idf_mat.keys():
    idf_mat[word] = math.log(sentence_size / (1 + word_appear_page[word]))
tfidf_mat = copy.deepcopy(tf_mat)
for data in tfidf_mat:
    for word in data:
        data[word] *= idf_mat[word]
# with open("semeval.csv", 'w') as f:
#     header = unique_word.keys()
#     f_csv = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
#     f_csv.writeheader()
#     f_csv.writerows(tfidf_mat)
with open("semeval_res.txt", 'w') as f:
    for data in tfidf_mat:
        for value in data.values():
            if value != 0:
                f.write(str(value) + ' ')
        f.write('\n')
