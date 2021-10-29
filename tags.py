import numpy as np
import pickle
from sklearn.utils.linear_assignment_ import linear_assignment


def _read_pickle(scene):
    pkl_file = './learning/'+str(scene)+'_linguistic_features.p'
    data = open(pkl_file, 'rb')
    lf = pickle.load(data)
    pkl_file = './learning/'+str(scene)+'_visual_features.p'
    data = open(pkl_file, 'rb')
    [vf, tree] = pickle.load(data)
    return lf, vf

def _get_GT():
    GT_total_links = 0
    GT_dict = {}
    # if "colours" in features:
    GT_dict['color_black'] = ["black"]
    GT_dict['color_blue'] = ["blue"]
    GT_dict['color_cyan'] = ["cyan", "sky", "turquoise"]
    GT_dict['color_gray'] = ["gray", "grey"]
    GT_dict['color_green'] = ["green"]
    GT_dict['color_pink'] = ["magenta", "pink", "purple"]
    GT_dict['color_red'] = ["red"]
    GT_dict['color_white'] = ["white"]
    GT_dict['color_yellow'] = ["yellow"]

    # if "shapes" in features:
    GT_dict['type_cube'] = ["block", "blocks", "parallelipiped", "square", "squares"]
    GT_dict['type_cylinder'] = ["can", "cans", "cylinder", "cylinders", "drums"]
    GT_dict['type_prism'] = ["prism", "pyramid", "tetrahedron"]
    GT_dict['type_sphere'] = ["sphere", "orb", "ball"]
    GT_dict['type_tower'] = ["tower", "stack", "squares"]

    # actions_approach
    GT_dict["take"] = ["pick", "remove", "take","pick up"]
    GT_dict["move"] = ["move", "shift", "stack"]
    GT_dict["drop"] = ["put", "place", "drop", "down","put down"]

    # locations
    GT_dict["locations_[1, 1]"] = ["left_lower"]
    GT_dict["locations_[1, 3.5]"] = ["left_center"]
    GT_dict["locations_[1, 6]"] = ["left_upper"]
    GT_dict["locations_[3.5, 1]"] = ["middle_upper"]
    GT_dict["locations_[3.5, 3.5]"] = ["center"]
    GT_dict["locations_[3.5, 6]"] = ["middle_lower"]
    GT_dict["locations_[6, 1]"] = ["right_lower"]
    GT_dict["locations_[6, 3.5]"] = ["right_center"]
    GT_dict["locations_[6, 6]"] = ["right_upper"]

    # relations
    GT_dict["relation_(1.0, 0, 0)"] = ["front"]
    GT_dict["relation_(-1.0, 0, 0)"] = ["back"]
    GT_dict["relation_(0, 0, 1.0)"] = ["highest", "on", "onto", "over", "above", "on top of"]
    GT_dict["relation_(0, 1.0, 0)"] = ["right"]
    GT_dict["relation_(0, 1.0, 0)"] = ["left"]

    return GT_dict



#--------------------------------------------------------------------------------------------------------#
LF_dict = {}
VF_dict = {}
pos = 0
GT_dict = _get_GT()
print 'GT_dict----',GT_dict
scenes = [1001]
hyp_number = 0
correct_number = 0
for max_scene in scenes:
    for scene in range(1, max_scene):
        print 'generating dictionaries from scene : ', scene
        LF,VF = _read_pickle(scene)
        for f in VF:
            for v in VF[f]:
                if f+'_'+str(v) not in VF_dict:
                    VF_dict[f+'_'+str(v)] = {}
                    VF_dict[f+'_'+str(v)]['VF'] = v
                    VF_dict[f+'_'+str(v)]['count'] = 1
                else:
                    VF_dict[f+'_'+str(v)]['count'] += 1
        for n in LF['n_grams']:
            if n == 'position':
                pos += 1
            if n not in LF_dict:
                LF_dict[n] = {}
                LF_dict[n]['count'] = 1
            else:
                LF_dict[n]['count'] += 1


    # initiate the dictionaries
    for n_gram in LF_dict:
        for ki_vj in sorted(VF_dict.keys()):
            LF_dict[n_gram][ki_vj] = 0
            # print 'LF_dict[',n_gram,'][',ki_vj,']', LF_dict[n_gram][ki_vj]

    for scene in range(1, max_scene):

        LF, VF = _read_pickle(scene)
        vf_in_this_scene = []
        for f in VF:
            for v in VF[f]:
                vf_in_this_scene.append(f+'_'+str(v))
        for n in LF['n_grams']:
            for v in vf_in_this_scene:
                LF_dict[n][v] += 1

    rows = len(VF_dict.keys())
    cols = len(LF_dict.keys())
    cost_matrix = np.ones((rows, cols), dtype=np.float32)

    for col, lexicon in enumerate(sorted(LF_dict.keys())):
        for row, v in enumerate(sorted(VF_dict.keys())):
            cost_matrix[row, col] = LF_dict[lexicon][v]

    for i in range(len(cost_matrix)):
        matrix_max = np.max(cost_matrix)
    matrix_lf_vf = cost_matrix / matrix_max
    match_list = linear_assignment(1 - matrix_lf_vf)
    correct_number = len(match_list)

    for col, lexicon in enumerate(sorted(LF_dict.keys())):
        for row, v in enumerate(sorted(VF_dict.keys())):
            #  language appears alone in the scene
            LF_dict[lexicon][v] = 1 - LF_dict[lexicon][v]/float(LF_dict[lexicon]['count'])
            cost_matrix[row, col] = LF_dict[lexicon][v]



    # this is the Hangarian algorithm   row:46, col:3606   Only the concept of language appears alone in the scene
    for row in range(len(VF_dict.keys())):
        cost_matrix[row, :] -= np.min(cost_matrix[row, :])
    for col in range(len(LF_dict.keys())):
        cost_matrix[:, col] -= np.min(cost_matrix[:, col])


    alpha = .01
    sorted_LF = sorted(LF_dict.keys())
    sorted_VF = sorted(VF_dict.keys())
    hypotheses_tags = {}
    for val2, VF in enumerate(sorted_VF):
        for val1, LF in enumerate(sorted_LF):
            if cost_matrix[val2, val1] <= alpha:
                if LF not in hypotheses_tags:
                    hypotheses_tags[LF] = {}
                hypotheses_tags[LF][VF] = cost_matrix[val2, val1]
                # print 'hypotheses_tags[',LF,'][',VF,']',hypotheses_tags[LF][VF]
                hyp_number += 1
                print VF, '---', LF, ':', cost_matrix[val2, val1]

# print 'match_list',match_list
print 'hyp_number--',hyp_number, 'correct_number', correct_number


pkl_file = './learning/tags.p'
pickle.dump([hypotheses_tags, VF_dict, LF_dict], open(pkl_file, 'wb'))
