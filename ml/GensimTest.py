from gensim import corpora
from gensim import models
from gensim import similarities

trainTexts = [['human', 'interface', 'computer'],
              ['survey', 'user', 'computer', 'system', 'response', 'time'],
              ['eps', 'user', 'interface', 'system'],
              ['system', 'human', 'system', 'eps'],
              ['user', 'response', 'time'],
              ['trees'],
              ['graph', 'trees'],
              ['graph', 'minors', 'trees'],
              ['graph', 'minors', 'survey']]

dictionary = corpora.Dictionary(trainTexts)
corpus = [dictionary.doc2bow(text) for text in trainTexts]
print corpus

# 完成对corpus中出现的每一个特征的IDF值的统计工作
tfidf = models.TfidfModel(corpus)
doc_bow = [(0, 1), (1, 1)]
print tfidf[doc_bow]

# 将模型持久化到磁盘上
tfidf.save("./model.tfidf")
# 加载已存在的模型
# tfidf = models.TfidfModel.load("./model.tfidf")


# 构造LSI模型并将待检索的query和文本转化为LSI主题向量
# 转换之前的corpus和query均是BOW向量
lsi_model = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
documents = lsi_model[corpus]
# 输入的查询以及转为一样的lsi模型
query = dictionary.doc2bow(['human', 'wqewq', 'fdffgdf'])
query_vec = lsi_model[query]

# 相似度计算
index = similarities.MatrixSimilarity(documents)
sims = index[query_vec]
print sims


class MyCorpus(object):
    def __iter__(self):
        for line in open('input.txt'):
            # assume there's one document per line, tokens separated by
            # whitespace
            yield dictionary.doc2bow(line.lower.split())
