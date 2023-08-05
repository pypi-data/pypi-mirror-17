# Copyright 2016 Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
from EvoDAG.command_line import CommandLine, main
from test_root import X, cl


def training_set():
    import tempfile
    fname = tempfile.mktemp()
    with open(fname, 'w') as fpt:
        for x, v in zip(X, cl):
            l = x.tolist()
            l.append(v)
            fpt.write(','.join(map(str, l)))
            fpt.write('\n')
    return fname


def test_command_line():
    fname = training_set()
    sys.argv = ['EvoDAG', '-s', '1', '-e', '10', '-p', '100', fname]
    c = CommandLine()
    c.parse_args()
    assert c.data.training_set == fname
    os.unlink(fname)
    os.unlink(c.data.model_file)
    assert c.evo._early_stopping_rounds == 10
    assert c.evo._classifier
    assert c.evo._popsize == 100
    assert c.evo._seed == 1


def test_main():
    fname = training_set()
    sys.argv = ['EvoDAG', '-m', 'temp.evodag.gz',
                '-e', '10', '-p', '100', fname, '-t', fname]
    main()
    os.unlink(fname)
    os.unlink('temp.evodag.gz')
    os.unlink(fname + '.evodag.csv')


def test_optimize_parameters():
    import os
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag.gz', '-p10', '-e2', '-r', '2', fname]
    c = CommandLine()
    c.parse_args()
    os.unlink(fname)
    os.unlink(c.data.model_file)
    assert c.evo._popsize == 10
    assert os.path.isfile('cache.evodag.gz')
    os.unlink('cache.evodag.gz')


def test_previous_model():
    import gzip
    import pickle
    fname = training_set()
    if os.path.isfile('model.evodag.gz'):
        os.unlink('model.evodag.gz')
    sys.argv = ['EvoDAG', '-p10', '-e2', '-m', 'model.evodag.gz', fname]
    c = CommandLine()
    c.parse_args()
    with gzip.open(c.data.model_file, 'w') as fpt:
        pickle.dump([], fpt)
        pickle.dump([], fpt)
        pickle.dump([], fpt)
    c = CommandLine()
    c.parse_args()
    os.unlink(fname)
    os.unlink(c.data.model_file)
    assert isinstance(c.model, list) and len(c.model) == 0


def test_cpu_cores():
    import os
    fname = training_set()
    sys.argv = ['EvoDAG', '-u2', '--parameters',
                'cache.evodag.gz', '-p10', '-e2', '-r', '2', fname]
    c = CommandLine()
    c.parse_args()
    assert c.evo._popsize == 10
    assert os.path.isfile('cache.evodag.gz')
    os.unlink(c.data.model_file)
    c = CommandLine()
    c.parse_args()
    os.unlink('cache.evodag.gz')
    os.unlink(fname)
    os.unlink(c.data.model_file)
    

def test_ensemble_size():
    import os
    from EvoDAG.model import Ensemble
    fname = training_set()
    sys.argv = ['EvoDAG', '-u2', '-n2', '--parameters',
                'cache.evodag.gz', '-p10', '-e2', '-r', '2', fname]
    c = CommandLine()
    c.parse_args()
    os.unlink(fname)
    os.unlink(c.data.model_file)
    assert os.path.isfile('cache.evodag.gz')
    assert isinstance(c.model, Ensemble)
    os.unlink('cache.evodag.gz')

    
def test_word2id():
    import tempfile
    fname = tempfile.mktemp()
    id2word = dict([[0, 'a'], [1, 'b'], [2, 'c']])
    with open(fname, 'w') as fpt:
        for x, v in zip(X, cl):
            l = x.tolist()
            l.append(id2word[v])
            fpt.write(','.join(map(str, l)))
            fpt.write('\n')
    sys.argv = ['EvoDAG', '-e2', '-p10', fname]
    c = CommandLine()
    c.parse_args()
    os.unlink(fname)


def test_output_file():
    fname = training_set()
    print(fname)
    sys.argv = ['EvoDAG', '-e2', '-p10',
                '-o', 'output.evodag.csv', '-t', fname,
                fname]
    c = CommandLine()
    c.parse_args()
    os.unlink(fname)
    print(os.path.isfile('output.evodag.csv'))
    assert os.path.isfile('output.evodag.csv')
    os.unlink('output.evodag.csv')
    

def test_id2word():
    import tempfile
    fname = tempfile.mktemp()
    id2word = dict([[0, 'a'], [1, 'b'], [2, 'c']])
    with open(fname, 'w') as fpt:
        for x, v in zip(X, cl):
            l = x.tolist()
            l.append(id2word[v])
            fpt.write(','.join(map(str, l)))
            fpt.write('\n')
    sys.argv = ['EvoDAG', '-e2', '-p10', fname, '-t',
                fname, '-o', 'output.txt']
    c = CommandLine()
    c.parse_args()
    with open('output.txt', 'r') as fpt:
        a = fpt.readlines()
    for i in a:
        assert i.rstrip() in ['a', 'b', 'c']
    os.unlink(fname)
    os.unlink('output.txt')


def test_json():
    import tempfile
    import json
    fname = tempfile.mktemp()
    with open(fname, 'w') as fpt:
        for x, y in zip(X, cl):
            a = {k: v for k, v in enumerate(x)}
            a['klass'] = int(y)
            a['num_terms'] = len(x)
            fpt.write(json.dumps(a) + '\n')
    print("termine con el json")
    sys.argv = ['EvoDAG', '-m', 'temp.evodag.gz', '--json',
                '-e', '10', '-p', '100', fname, '-ooutput.evodag', '-t', fname]
    main()
    os.unlink(fname)
    os.unlink('temp.evodag.gz')
    print(open('output.evodag').read())
    os.unlink('output.evodag')


def test_params():
    import os
    import gzip
    from EvoDAG.command_line import params
    import json
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag.gz', '-p10', '-e2', '-r', '2', fname]
    params()
    os.unlink(fname)
    assert os.path.isfile('cache.evodag.gz')
    with gzip.open('cache.evodag.gz', 'rb') as fpt:
        try:
            d = fpt.read()
            a = json.loads(str(d, encoding='utf-8'))
        except TypeError:
            a = json.loads(d)
    os.unlink('cache.evodag.gz')
    assert len(a) == len([x for x in a if 'fitness' in x])
    print(a)


def test_parameters_values():
    import os
    from EvoDAG.command_line import params
    import json
    fname = training_set()
    with open('p.conf', 'w') as fpt:
        fpt.write(json.dumps(dict(popsize=['x'])))
    sys.argv = ['EvoDAG', '-Pcache.evodag.gz', '-p10', '-e2',
                '--parameters-values', 'p.conf',
                '-r', '2', fname]
    try:
        params()
        assert False
    except ValueError:
        pass
    os.unlink('p.conf')
    os.unlink(fname)


def test_train():
    import os
    from EvoDAG.command_line import params, train
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag.gz', '-p10', '-e2', '-r', '2', fname]
    params()
    sys.argv = ['EvoDAG', '--parameters', 'cache.evodag.gz',
                '-n2',
                '--model', 'model.evodag',
                '--test', fname, fname]
    train()
    os.unlink(fname)
    os.unlink('cache.evodag.gz')
    assert os.path.isfile('model.evodag')
    os.unlink('model.evodag')


def test_predict():
    import os
    from EvoDAG.command_line import params, train, predict
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag.gz', '-p10', '-e2', '-r', '2', fname]
    params()
    sys.argv = ['EvoDAG', '--parameters', 'cache.evodag.gz',
                '-n2',
                '--model', 'model.evodag',
                '--test', fname, fname]
    train()
    sys.argv = ['EvoDAG', '--output', 'output.evodag',
                '--model', 'model.evodag', fname]
    predict()
    os.unlink(fname)
    os.unlink('cache.evodag.gz')
    os.unlink('model.evodag')
    assert os.path.isfile('output.evodag')
    os.unlink('output.evodag')
    

def test_generational():
    import os
    from EvoDAG.command_line import CommandLineParams
    import gzip
    import json
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag.gz', '-p10', '-e2',
                '--evolution', 'Generational',
                '-r', '2', fname]
    c = CommandLineParams()
    c.parse_args()
    with gzip.open('cache.evodag.gz') as fpt:
        data = fpt.read()
        try:
            a = json.loads(str(data, encoding='utf-8'))
        except TypeError:
            a = json.loads(data)
    a = a[0]
    assert 'population_class' in a
    assert a['population_class'] == 'Generational'
    os.unlink('cache.evodag.gz')
    print(a)


def test_all_inputs():
    import os
    from EvoDAG.command_line import CommandLineParams
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag.gz', '-p6', '-e2',
                '--all-inputs', '-r', '2', fname]
    c = CommandLineParams()
    c.parse_args()
    os.unlink('cache.evodag.gz')
    

def test_time_limit():
    import os
    from EvoDAG.command_line import params, train
    import json
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag', '-p10', '-e2',
                '--time-limit', '10',
                '-r', '2', fname]
    params()
    sys.argv = ['EvoDAG', '--parameters', 'cache.evodag',
                '-n2',
                '--model', 'model.evodag',
                '--test', fname, fname]
    train()
    os.unlink(fname)
    with open('cache.evodag') as fpt:
        a = json.loads(fpt.read())[0]
    assert 'time_limit' in a
    os.unlink('cache.evodag')
    assert os.path.isfile('model.evodag')
    os.unlink('model.evodag')


def test_word2id2():
    import tempfile
    import os
    from EvoDAG.command_line import CommandLineParams
    fname = tempfile.mktemp()
    id2word = dict([[0, 'a'], [1, 'b'], [2, 'c']])
    with open(fname, 'w') as fpt:
        for x, v in zip(X, cl):
            l = x.tolist()
            l.append(id2word[v])
            fpt.write(','.join(map(str, l)))
            fpt.write('\n')
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag', '-p3', '-e1',
                '-r', '1', fname]
    c = CommandLineParams()
    c.parse_args()
    print(len(c.word2id))
    assert len(c.word2id) == 0
    os.unlink('cache.evodag')
    os.unlink(fname)


def test_decision_function():
    import os
    from EvoDAG.command_line import params, train, predict
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag', '-p3', '-e1',
                '-r', '1', fname]
    params()
    sys.argv = ['EvoDAG', '--parameters', 'cache.evodag',
                '-n2',
                '--model', 'model.evodag',
                '--test', fname, fname]
    train()
    sys.argv = ['EvoDAG', '--output', 'output.evodag',
                '--decision-function',
                '--model', 'model.evodag', fname]
    predict()
    os.unlink(fname)
    os.unlink('cache.evodag')
    os.unlink('model.evodag')
    os.unlink('output.evodag')


def test_random_generations():
    import os
    import json
    from EvoDAG.command_line import params
    fname = training_set()
    sys.argv = ['EvoDAG', '--parameters',
                'cache.evodag', '-p3', '-e1',
                '--random-generations', '1',
                '-r', '1', fname]
    params()
    os.unlink(fname)
    with open('cache.evodag') as fpt:
        a = json.loads(fpt.read())[0]
    assert 'random_generations' in a
    os.unlink('cache.evodag')
