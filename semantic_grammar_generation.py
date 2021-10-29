import pickle
import itertools
from copy import deepcopy

def _read_tags():
    pkl_file = './learning/tags.p'
    data = open(pkl_file, 'rb')
    hypotheses_tags, VF_dict, LF_dict = pickle.load(data)
    return [hypotheses_tags, VF_dict, LF_dict]

def _read_sentences(scene):
    pkl_file = './data/scenes/'+str(scene)+'_sentences.p'
    data = open(pkl_file, 'rb')
    sentences = pickle.load(data)
    return sentences

def _read_vf(scene):
    pkl_file = './learning/'+str(scene)+'_visual_features.p'
    data = open(pkl_file, 'rb')
    vf, tree = pickle.load(data)
    return vf, tree

def _read_passed_tags():
    pkl_file = './matching/Passed_tags.p'
    data = open(pkl_file, 'rb')
    Matching, Matching_VF, passed_scenes, passed_ids = pickle.load(data)
    return [Matching, Matching_VF, passed_scenes, passed_ids]

def _read_grammar_trees(scene):
    pkl_file = './learning/'+str(scene)+'_grammar.p'
    data = open(pkl_file, 'rb')
    tree = pickle.load(data)
    return tree

def _test_Actions(element):
    action_flag = 1
    action_position = []
    for count, item in enumerate(element):
        if 'actions_' in item:
            action_position.append(count)
    # print action_position
    if len(action_position) == 0:
        action_flag = 0

    elif len(action_position) > 1:
        L = [a_i - b_i for a_i, b_i in zip(action_position[:-1], action_position[1:])]
        for i in L:

            if i != -1:
                action_flag = 0

    return action_flag

#--------------------------------------------------------------------------------------------------------#
# this function tests one subset of words at a time
def _all_possibilities_func(subset, hyp_language_pass):
    all_possibilities = []      # all the possibilities gathered in one list
    words = {}
    count = 0
    #  words is a list for counting the word that appear in the subset(words[]) list and how many times they appear
    for word in subset:
        if word not in words:
            words[word] = count
            count += 1
            all_possibilities.append(hyp_language_pass[word].keys())
    return all_possibilities, words

def _get_semantics(grammar_tree_id_count, hypotheses_tags):
    # words is a list for collecting all the words show in all the grammar_trees[id][count](With duplication)
    words = []
    for i in range(len(grammar_tree_id_count)):
        for word in grammar_tree_id_count[i]:
            words.append(word)
    semantic_trees = {}
    all_possibilities, words_dict = _all_possibilities_func(words, hypotheses_tags)
    for count, element in enumerate(itertools.product(*all_possibilities)):
        # print element
        valid = _test_Actions(element)
        if valid:
            semantic_trees[count] = deepcopy(grammar_tree_id_count)
            c = 0
            for i in range(len(semantic_trees[count])):
                for j in range(len(semantic_trees[count][i])):
                    semantic_trees[count][i][j] = element[words_dict[words[c]]]
                    c += 1
    return semantic_trees

hypotheses_tags, VF_dict, LF_dict = _read_tags()

for scene in range(1, 1001):
    semantic_trees = {}
    print 'generating grammar from scene : ', scene
    VF, Tree = _read_vf(scene)
    sentences = _read_sentences(scene)
    grammar_trees = _read_grammar_trees(scene)
    counter = 0
    for id in sentences:

        semantic_trees[id] = {}
        # count is the number of combination of n-grams-list for idth sentence
        for count in grammar_trees[id]:
            grammar_tree_id_count = grammar_trees[id][count]
            semantic_trees[id][count] = _get_semantics(grammar_tree_id_count, hypotheses_tags)
            counter += len(semantic_trees[id][count])
    pkl_file = './learning/'+str(scene)+'_semantic_grammar.p'
    print 'semantic_trees====', semantic_trees
    pickle.dump(semantic_trees, open(pkl_file, 'wb'))
