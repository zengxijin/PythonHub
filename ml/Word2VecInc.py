# imput sample:
# run command sample: ./Word2VecInc.py 51 1,2,3 4,5,6
import sys
import gensim
model = gensim.models.Word2Vec.load('/tmp/node_vector_training.model')
new_data = []
node_id = sys.argv[2].strip().split(',')[0]
for i in xrange(2, len(sys.argv)):
    tmp = sys.argv[i].strip().split(',')
    new_data.append(tmp)
# tmp_v = new_data.strip().split(' ')
model.build_vocab(new_data, update=True)
model.train(new_data, total_examples=model.corpus_count, epochs=model.iter)
# model.save("test_model.model")
sim_vec = model.most_similar(positive=[node_id], topn=sys.argv[1])
for i in xrange(0, len(sim_vec)):
    # print type(sim_vec[i])
    print sim_vec[i][0],
