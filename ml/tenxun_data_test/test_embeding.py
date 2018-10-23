from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors

model_path = "E:\\Tencent_AILab_ChineseEmbedding\\head_10w.txt"
# model = Word2Vec.load(model_path)
# model = Word2Vec.load_word2vec_format(model_path)
model = KeyedVectors.load_word2vec_format(model_path)
# model.save("word2vec.model")

# model.update_vocab(new_sentences)
# model.train(new_sentences)
# model.save("updated_model")

print(model.syn0.shape)

top10 = model.similar_by_word("链家")
print(top10)
