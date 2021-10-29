import numpy as np
import pickle
import operator



def _read_pickle(scene):
    pkl_file = './data/scenes/'+str(scene)+'_sentences.p'
    data = open(pkl_file, 'rb')
    sentences = pickle.load(data)
    return sentences


def _find_n_grams(sentence):
    n_word = 1  # length of n_grams
    w = sentence.split(' ')
    n_grams = []
    for i in range(len(w)):
        for j in range(i+1, np.min([i+1+n_word, len(w)+1])):
            n_grams.append(' '.join(w[i:j]))
    return n_grams

def _get_words(sentences):
    n_grams_unique = []
    n_grams_all = []
    n = _find_n_grams(sentences[id]['text'])
    # print 'n_grams-------',n
    for word in n:
        if word not in n_grams_unique:
            n_grams_unique.append(word)

    for word in n:
        n_grams_all.append(word)
    return n_grams_all



tf = {}
tf_idf = {}
n_doc = 0.0
all_words = []


for scene in range(1, 1001):
    sentences = _read_pickle(scene)
    for id in sentences:
        words = _get_words(sentences)
        for word in words:
            if word not in all_words:
                all_words.append(word)

# Number of documents containing the word
n_doc_c_word = dict.fromkeys(all_words, 0)

for scene in range(1, 1001):
    # print 'extracting feature from scene : ', scene
    pkl_file = './data/scenes/'+str(scene)+'_linguistic_features.p'
    sentences = _read_pickle(scene)
    # print 'sentences=======', sentences
    for id in sentences:

        n_doc += 1
        words = _get_words(sentences)

        for word in words:
            if word not in tf:
                tf[word] = 1.0
            else:
                tf[word] += 1
            if word in all_words:
                n_doc_c_word[word] += 1


total = sum(tf.itervalues(), 0.0)
tf = {k: v/total for k, v in tf.iteritems()}

sorted_x = sorted(tf.items(), key=operator.itemgetter(1))


Functional_Word = []
Stop_Word = []
alpha_min = 0.00026329240395843255
alpha_max = 0.05
print 'alpha_max',alpha_max
print 'alpha_min',alpha_min
print 'len(all_words)',len(all_words)
for word in all_words:
    tf_idf[word] = tf[word] * np.log(n_doc/n_doc_c_word[word]+1)
    print 'tf_idf[', word, '] =',tf_idf[word]

    if tf_idf[word] > alpha_min and tf_idf[word] < alpha_max:
        Functional_Word.append(word)
    if tf_idf[word] > alpha_max or tf_idf[word] < alpha_min:
        Stop_Word.append(word)
print 'tf_idf =',sorted(tf_idf.items(),key=operator.itemgetter(1))
print 'with_tf=',tf_idf['with'],'n_doc=',n_doc,'with_n_doc_c_word',n_doc_c_word['with']
print 'be_tf=',tf_idf['be']
print 'the_tf=',tf_idf['the'],'n_doc=',n_doc,'the_n_doc_c_word',n_doc_c_word['the']
print 'FW---------',Functional_Word
print 'SW---------',Stop_Word
print 'len(FW)-----',len(Functional_Word)
print 'len(SW)-----',len(Stop_Word)
print n_doc
pkl_file = './learning/idf_FW_linguistic_features.p'
pickle.dump(Stop_Word, open(pkl_file, 'wb'))
