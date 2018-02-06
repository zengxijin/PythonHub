import gensim
import base64
import logging
import traceback
from flask import Flask, jsonify, request

app = Flask(__name__)


# global var
model = gensim.models.Word2Vec.load('/home/zengxj/python/node_vector_training_cash.model')


def sim(node_id, topn, inputs):
    new_data = []
    for i in xrange(1, len(inputs)):
        tokens = inputs[i].strip().split(',')
        for j in xrange(1, len(tokens)):
            tmp = []
            tmp.append(tokens[0])
            tmp.append(tokens[j])
            new_data.append(tmp)
        model.build_vocab(new_data, update=True)
        model.train(new_data, total_examples=model.corpus_count, epochs=model.iter)
    
    sim_vec = model.most_similar(positive=[node_id], topn=int(topn))
    result_data = []
    for i in xrange(0, len(sim_vec)):
        result_data.append(sim_vec[i][0])

    return result_data


@app.route('/ml/api/v1.0/sim', methods=['POST'])
def sim_api():
    req = request.json
    app.logger.info(req)

    # channel info
    client_id = req['clientId']
    # service flag, can used to route in future
    service = req['service']

    # parse the params
    tmp_kv = {}
    if 'params' in req:
        params_list = req['params']
        if len(params_list) > 1:
            for kv in params_list:
                key = kv['key']
                val = kv['value']
                is_base64 = kv['base64']
                if is_base64:
                    tmp_kv[key] = base64.b64decode(val)
                else:
                    tmp_kv[key] = val
                # print ('key:%s value:%s base64:%s' % (key, val, is_base64))
        else:
            app.logger.warning('params is empty')

    node_id = tmp_kv['inputs'].split(',')[0]
    topn = tmp_kv['topn']
    inputs = tmp_kv['inputs'].split(' ')
    
    # print tmp_kv
    # print node_id
    # print topn
    # print inputs
    try:
        sim_result = sim(node_id, topn, inputs)
    except Exception:
        app.logger.error('trace: %s', traceback.format_exc())
    else:
        app.logger.info('sim result: %s', sim_result)
    
    print sim_result
    
    return jsonify({'result': sim_result})


if __name__ == '__main__':
    handler = logging.FileHandler('sim.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.debug = True

    app.run(host='0.0.0.0')


