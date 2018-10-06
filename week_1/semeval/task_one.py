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
    data_row = copy.deepcopy(unique_word) # 每个列表要有自己的字典
    size = len(data)
    word_appear = {} #记录句子中已经出现的单词
    for word in data:
        if word not in word_appear.keys(): #如果句子中还没出现这个单词
            word_appear_page[word] += 1 #单词出现的文章数加一
        word_appear[word] = 1
        data_row[word] += 1 / size #句子对应的字典，出现一次根据TF矩阵加上相应的值
    tf_mat.append(data_row) #将字典加入列表中，加入完毕则TF矩阵构造完成
idf_mat = copy.deepcopy(unique_word)
for word in idf_mat.keys():
    idf_mat[word] = math.log(sentence_size / (1 + word_appear_page[word])) ##IDF矩阵构建的公式
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
