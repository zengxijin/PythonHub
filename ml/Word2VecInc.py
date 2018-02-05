# imput sample:
# run command sample: ./Word2VecInc.py 51 -4997816680341835271,-3316483741552779112,747873468606477381,527339124957220179,1614505455050530776,-5768653493889486991,-384548834315283201,-5395980713609502551,6207235105550302889,4452483878111425273,-2821110282058078629 -4997816680341835271,-3316483741552779112,747873468606477381,527339124957220179,1614505455050530776,-5768653493889486991,-384548834315283201,-5395980713609502551,6207235105550302889,4452483878111425273,-2821110282058078629
import sys
import gensim


model = gensim.models.Word2Vec.load(
    '/home/zengxj/python/node_vector_training_cash.model')
new_data = []
node_id = sys.argv[2].strip().split(',')[0]

# If incremental train is needed, there should be at least 12 arguments
if (len(sys.argv) > 3):
  for i in xrange(2, len(sys.argv)):
    tokens = sys.argv[i].strip().split(',')
    for j in xrange(1, len(tokens)):
      tmp = []
      tmp.append(tokens[0])
      tmp.append(tokens[j])
      new_data.append(tmp)
  model.build_vocab(new_data, update=True)
  model.train(new_data, total_examples=model.corpus_count, epochs=model.iter)


sim_vec = model.most_similar(positive=[node_id], topn=int(sys.argv[1]))
print "result:"
for i in xrange(0, len(sim_vec)):
    print sim_vec[i][0],
