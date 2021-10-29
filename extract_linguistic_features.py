import numpy as np
import pickle


def _read_stop_wrods():
    pkl_file = './learning/idf_FW_linguistic_features.p'
    data = open(pkl_file, 'rb')
    stop = pickle.load(data)
    return stop

def _read_pickle(scene):
    pkl_file = './data/scenes/'+str(scene)+'_sentences.p'
    data = open(pkl_file, 'rb')
    sentences = pickle.load(data)
    return sentences


def _find_n_grams(sentence):
    n_word = 3  # length of n_grams
    sen = sentence.split(' ')
    n_grams = []
    for i in range(len(sen)):
        # if w[i]not in self.words[s]: self.words[s].append(w[i])
        for j in range(i+1,np.min([i+1+n_word,len(sen)+1])):
            n_grams.append(' '.join(sen[i:j]))
    # print 'n_grams----',n_grams
    for i, word_1 in enumerate(sen):
        if i + 2 < len(sen):
            print i, '+', i + 2
            print sen[i], '+', sen[i + 2]
            skip_one_gram = " ".join([sen[i], sen[i + 2]])
            n_grams.append(skip_one_gram)
            print 'skip_one_gram', skip_one_gram
        if i + 3 < len(sen):
            print i, '+', i + 3
            print sen[i], '+', sen[i + 3]
            skip_two_gram = " ".join([sen[i], sen[i + 3]])
            n_grams.append(skip_two_gram)
            print 'skip_two_gram', skip_two_gram
        if i + 4 < len(sen):
            print i, '+', i + 4
            print sen[i], '+', sen[i + 4]
            skip_three_gram = " ".join([sen[i], sen[i + 4]])
            n_grams.append(skip_three_gram)
            print 'skip_three_gram', skip_three_gram

    return n_grams

def _get_n_grams(sentences,stop):
    all_n_grams = []
    for id in sentences:
        n = _find_n_grams(sentences[id]['text'])
        for i in n:
            ok = 1
            for stop_word in stop:
                if stop_word == i or ' '+stop_word in i or stop_word+' ' in i:
                    ok = 0
            if ok:
                if i not in all_n_grams:
                    all_n_grams.append(i)
    return all_n_grams

stop = _read_stop_wrods()
for scene in range(1,1001):
    print 'extracting feature from scene : ',scene
    pkl_file = './learning/'+str(scene)+'_linguistic_features.p'
    LF = {}
    sentences = _read_pickle(scene)
    LF['n_grams'] = _get_n_grams(sentences,  stop)
    print 'LF_n_grams------', LF['n_grams']
    pickle.dump(LF, open(pkl_file, 'wb'))
    file1 = './learning/'+str(scene)+'_linguistic_feature.txt'
    F = open(file1, 'w')
    for n in LF['n_grams']:
        F.write(n+'\n')
    F.close()
