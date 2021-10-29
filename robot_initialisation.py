import os
import pickle
import numpy as np
from load_xml import *


class Robot():
    def __init__(self):
        self.total_num_objects = 0
        self._initilize_values()
        self.all_sentences_count = 1
        self.Data = read_data()
        self.all_words = []

    def _initilize_values(self):
        self.chess_shift_x = 8
        self.chess_shift_y = 6
        self.len_arm1 = 8
        self.len_arm2 = 6
        self.len_gripper = 2

        self.len_base = 2
        self.l1 = 0
        self.l2 = self.len_arm1  # 8
        self.l3 = self.len_arm2 + self.len_gripper  # 8
        self.a0 = 0
        self.a1 = 0
        self.a2 = 0
        self.step = 8
        self.frame_number = 0
        self.object = {}
        self.object_shape = {}
        self.words = []
        self.positions = {}
        # manage directories to store data and images
        self.image_dir = './data/scenes/'
        if not os.path.isdir(self.image_dir):
            print 'please change the directory'

    def _fix_sentences(self):
        if self.scene not in self.Data['commands']:
            self.Data['commands'][self.scene] = {}
        S = self.Data['commands'][self.scene]

        for i in S:
            S[i] = S[i].replace("    ", " ")
            S[i] = S[i].replace("   ", " ")
            S[i] = S[i].replace("  ", " ")
            S[i] = S[i].replace("  ", " ")
            S[i] = S[i].replace("  ", " ")
            S[i] = S[i].replace("  ", " ")
            S[i] = S[i].replace(".", "")
            S[i] = S[i].replace(",", "")
            S[i] = S[i].replace("'", "")
            S[i] = S[i].replace("-", " ")
            S[i] = S[i].replace("/", " ")
            S[i] = S[i].replace("!", "")
            S[i] = S[i].replace("(", "")
            S[i] = S[i].replace(")", "")
            S[i] = S[i].replace("?", "")
            S[i] = S[i].replace(" botton ", " bottom ")
            S[i] = S[i].replace(" o nthe ", " on the ")
            S[i] = S[i].replace(" highthest ", " highest ")
            S[i] = S[i].replace(" taht ", " that ")
            S[i] = S[i].replace(" yelllow ", " yellow ")
            S[i] = S[i].replace(" bluee ", " blue ")
            S[i] = S[i].replace(" paced ", " placed ")
            S[i] = S[i].replace(" edhe ", " edge ")
            S[i] = S[i].replace(" gree ", " green ")
            S[i] = S[i].replace(" ed ", " red ")
            S[i] = S[i].replace(" pf ", " of ")
            S[i] = S[i].replace(" tow ", " top ")
            S[i] = S[i].replace(" te ", " the ")
            S[i] = S[i].replace(" if ", " of ")
            S[i] = S[i].replace(" l2 ", " 2 ")
            S[i] = S[i].replace(" re ", " red ")
            S[i] = S[i].replace(" rd ", " red ")
            S[i] = S[i].replace(" reb ", " red ")
            S[i] = S[i].replace(" op ", " top ")
            S[i] = S[i].replace(" closet ", " closest ")
            S[i] = S[i].replace("pickup ", "pick up ")
            S[i] = S[i].replace(" dearest ", " nearest ")
            S[i] = S[i].replace(" gyellow ", " yellow ")
            S[i] = S[i].replace(" yeloow ", " yellow ")
            S[i] = S[i].replace(" uo ", " up ")
            S[i] = S[i].replace(" un ", " up ")
            S[i] = S[i].replace(" twp ", " two ")
            S[i] = S[i].replace(" blok ", " block ")
            S[i] = S[i].replace(" o ", " on ")
            S[i] = S[i].replace(" thee ", " the ")
            S[i] = S[i].replace(" sian ", " cyan ")
            S[i] = S[i].replace(" he ", " the ")
            S[i] = S[i].replace(" an ", " and ")
            S[i] = S[i].replace(" atop ", " top ")
            S[i] = S[i].replace(" i ton ", " it on ")
            S[i] = S[i].replace(" hte ", " the ")
            S[i] = S[i].replace(" pryamid ", " pyramid ")
            S[i] = S[i].replace(" robort ", " robot ")
            S[i] = S[i].replace(" othe ", " other ")
            S[i] = S[i].replace(" squre ", " square ")
            S[i] = S[i].replace(" sqaure ", " square ")
            S[i] = S[i].replace(" coloum ", " column ")
            S[i] = S[i].replace(" rght ", " right ")
            S[i] = S[i].replace(" letf ", " left ")
            S[i] = S[i].replace(" cibe ", " cube ")
            S[i] = S[i].replace(" bloack ", " block ")
            S[i] = S[i].replace(" ywllow ", " yellow ")
            S[i] = S[i].replace(" torquise ", " turquoise ")
            S[i] = S[i].replace(" pyrramid ", " pyramid ")
            S[i] = S[i].replace(" pyraamid ", " pyramid ")
            S[i] = S[i].replace(" ptramid ", " pyramid ")
            S[i] = S[i].replace(" whire ", " white ")
            S[i] = S[i].replace(" bluee ", " blue ")
            S[i] = S[i].replace(" siyan ", " cyan ")
            S[i] = S[i].replace(" sian ", " cyan ")
            S[i] = S[i].replace(" redbox ", " red box ")
            S[i] = S[i].replace(" ble ", " blue ")
            S[i] = S[i].replace(" theblue ", " the blue ")
            S[i] = S[i].replace(" thenext ", " the next ")
            S[i] = S[i].replace(" gyellow ", " yellow ")
            S[i] = S[i].replace(" gree ", " green ")
            S[i] = S[i].replace(" midle ", " middle ")
            S[i] = S[i].replace(" adn ", " and ")
            S[i] = S[i].replace(" diaganal ", " diagonal ")
            S[i] = S[i].replace(" diagnol ", " diagonal ")
            S[i] = S[i].replace(" inbetween ", " in between ")
            S[i] = S[i].replace(" ligh tgreen ", " light green ")
            S[i] = S[i].replace(" towerlocated ", " tower located ")
            S[i] = S[i].replace(" toten ", " tower ")
            S[i] = S[i].replace(" forwardmost ", " forward most ")
            S[i] = S[i].replace(" cubest ", " cube ")
            S[i] = S[i].replace(" infront ", " in front ")
            S[i] = S[i].replace(" tto ", " to ")
            S[i] = S[i].replace(" fron ", " front ")
            S[i] = S[i].replace(" onred ", " on red ")
            S[i] = S[i].replace(" betweeen ", " between ")
            S[i] = S[i].replace(" prysm ", " prism ")
            S[i] = S[i].replace(" bacl ", " back ")
            S[i] = S[i].replace(" sme ", " same ")

            A = S[i].split(' ')
            while '' in A:         A.remove('')
            s = ' '.join(A)
            S[i] = s.lower()
            print 'S[i]', S[i]
            self.Data['commands_id'][i]['text'] = s.lower()

        self.Data['commands'][self.scene] = S

    def _change_data(self):
        def _change(words, key):
            for i, word in enumerate(words):
                indices = [j for j, x in enumerate(s) if x == word]
                for m in indices:
                    s[m] = key[i]
            self.Data['commands'][self.scene][sentence] = ' '.join(s)

        prism = ['pyramid', 'prism', 'tetrahedron', 'triangle']
        sphere = ['ball', 'sphere', 'orb', 'orb']
        prisms = ['pyramids', 'prisms', 'tetrahedrons', 'triangles']
        spheres = ['balls', 'spheres', 'orbs', 'orbs']
        box = ['block', 'cube', 'box', 'slab', 'parallelipiped', 'parallelepiped', 'brick', 'square']
        cylinder = ['cylinder', 'can', 'drum', 'drum', 'can', 'can', 'can', 'can']
        boxes = ['cubes', 'boxes', 'blocks', 'slabs', 'parallelipipeds', 'bricks', 'squares']
        cylinders = ['cylinders', 'cans', 'drums', 'drums', 'cans', 'cans', 'cans']


        # change commands
        for sentence in self.Data['commands'][self.scene]:
            print 'position-----', self.Data['layouts']
            # change scenes
            I = self.Data['scenes'][self.scene]['initial']
            F = self.Data['scenes'][self.scene]['final']
            s = self.Data['commands'][self.scene][sentence].split(' ')
            # color_need_to change:
            if self.scene == id in [2, 4, 33, 34, 35, 36,38,40,48,49,50,51,52,53,58,62,63,64,73,74,75,76,79,80,93,94,95,
                                    96,97,99,100,102,103,104,105,106,107,110,112,113,124,128,129,132,133,134,135,137,
                                    138,139,140,144,146,147,148,149,150,151,155,161,165,168,170,171,172,175,177,179,
                                    181,182,184,190,194,196,199,200,206,208,210,211,214,215,216,218,220,221,222,223,
                                    224,226,228,231,234,235,239,240,241,244,247,249,250,251,253,255,257,258,260,263,
                                    266,267,270,272,274,276,277,279,280,282,284,288,290,292,294,295,297,301,302,303,
                                    304,305,306,308,309,310,311,312,313,314,315,317,318,319,322,323,324,329,331,332,
                                    345,346,347,348,349,351,352,355,356,357,360,362,363,366,368,369,373,374,375,380,
                                    391,393,394,396,404,406,407,409,411,412,413,414,415,416,420,422,423,425,427,430,
                                    432,433,434,435,436,439,440,445,448,449,452,455,465,468,469,473,474,475,478,479,
                                    480,481,483,484,486,492,495,496,497,499,500,501,504,506,514,519,521,524,525,527,
                                    528,529,530,532,533,534,537,539,541,542,543,549,551,552,555,556,569,572,573,578,
                579,588,590,591,601,602,604,605,608,613,614,622,624,627,629,632,633,634,635,636,638,639,642,647,648,
                650,654,656,657,658,661,665,666,668,669,670,671,676,680,682,686,688,692,695,697,698,701,702,704,705,
                709,710,711,712,716,728,719,720,721,727,730,731,733,734,738,739,745,749,750,751,753,757,760,763,769,
                770,771,776,777,779,783,785,786,787,790,791,792,793,794,795,796,798,802,810,812,818,819,822,825,826,
                841,843,845,849,850,855,857,858,859,860,861,863,869,870,871,872,873,874,876,878,880,881,883,884,885,886,
                889,890,891,908,910,911,913,914,915,916,917,919,920,921,924,925,926,929,931,933,934,935,936,937,938,942,
                944,947,948,950,951,954,957,958,960,961,966,968,969,970,973,974,975,976,978,981,983,988,999,1000]:
                _change(['red'], ['black'])
                for obj in self.Data['layouts'][I]:
                    if self.Data['layouts'][I][obj]['F_HSV'] == 'red':
                        self.Data['layouts'][I][obj]['F_HSV'] = 'black'
                for obj in self.Data['layouts'][F]:
                    if self.Data['layouts'][F][obj]['F_HSV'] == 'red':
                        self.Data['layouts'][F][obj]['F_HSV'] = 'black'
            if self.scene == 20:
                _change(['yellow'], ['green'])
                for obj in self.Data['layouts'][I]:
                    if self.Data['layouts'][I][obj]['F_HSV'] == 'yellow':
                        self.Data['layouts'][I][obj]['F_HSV'] = 'green'
                for obj in self.Data['layouts'][F]:
                    if self.Data['layouts'][F][obj]['F_HSV'] == 'yellow':
                        self.Data['layouts'][F][obj]['F_HSV'] = 'green'
            if self.scene == id in [1, 7, 17, 18, 24, 30, 32,42,43,44,46,47,57,59,62,64,90,91,92,93,94,96,105,106,108,111,
                112,113,116,118,119,122,123,124,125,127,128,129,131,132,133,135,138,139,141,142,143,145,146,151,152,153,
                154,155,156,157,163,164,165,166,169,170,172,173,174,175,176,178,179,181,182,185,190,193,195,198,199,200,
                202,208,210,211,214,215,230,231,243,244,248,249,250,252,254,258,259,261,264,278,289,291,294,296,297,301,
                308,310,322,323,362,363,373,374,375,376,377,378,383,384,385,390,393,394,395,396,399,400,405,409,412,413,
                415,416,419,420,431,434,436,437,442,457,458,463,464,473,474,475,476,482,499,500,504,506,508,511,513,514,
                515,516,518,520,529,530,531,532,533,534,535,536,548,549,550,551,569,573,574,575,577,578,580,581,583,584,
                586,587,588,589,590,592,593,595,598,604,605,606,617,618,619,667,668,669,670,671,672,673,674,675,679,680,
                681,683,684,685,686,688,715,719,720,729,730,739,740,742,744,745,746,748,749,750,751,803,808,809,811,813,
                814,818,823,824,829,843,844,846,847,865,867,870,871,873,879,886,887,888,897,898,899,901,907,908,909,911,
                929,930,932,935,936,953,955,956,957,960,964,965,966,967,977,978,980,986,989,991,992,993,994,999,1000]:
                _change(prism, sphere)
                _change(prisms, spheres)
                for obj in self.Data['layouts'][I]:
                    if self.Data['layouts'][I][obj]['F_SHAPE'] in prism:
                        self.Data['layouts'][I][obj]['F_SHAPE'] = 'sphere'
                for obj in self.Data['layouts'][F]:
                    if self.Data['layouts'][F][obj]['F_SHAPE'] in prisms:
                        self.Data['layouts'][F][obj]['F_SHAPE'] = 'spheres'
            if self.scene == id in [9, 10, 11, 12, 13, 15, 22, 28, 36,37,38,39,40,49,55,56,60,61,63,65,67,68,69,71,75,76,
                                    77,79,83,84,86,87,88,90,91,92,96,97,98,102,107,117,118,127,128,133,134,137,140,144,145,
                                    148,149,150,152,153,154,157,158,159,160,163,164,165,166,169,170,172,175,176,177,178,
                                    180,181,182,183,186,187,190,191,192,193,196,200,201,202,204,205,207,209,210,211,217,
                                    218,219,222,227,229,230,231,232,233,234,235,236,238,239,241,241,243,247,249,254,255,
                                    259,261,264,265,267,268,272,275,276,277,281,283,288,293,297,299,302,303,304,305,309,310,
                                    311,314,319,320,324,328,331,333,334,335,339,340,341,343,346,347,351,353,354,356,357,358,
                                    359,362,366,369,370,372,374,375,376,377,378,379,381,383,385,387,388,394,395,402,407,410,
                411,413,415,416,423,426,430,432,433,434,436,437,438,439,442,443,450,453,454,464,466,467,468,470,471,472,473,
                475,476,477,480,484,485,486,493,495,498,499,502,507,508,509,511,512,514,515,516,519,520,522,523,524,526,529,
                530,531,532,533,537,538,539,540,542,543,546,547,549,550,552,553,555,558,560,562,563,566,567,568,572,574,575,
                577,591,605,606,607,609,611,612,613,614,618,625,627,628,629,631,632,634,636,644,645,649,650,651,654,655,656,
                660,661,662,663,664,665,670,673,677,678,681,682,684,686,688,693,694,695,696,701,704,705,706,709,714,715,716,
                718,719,727,728,733,745,749,750,752,753,754,756,757,758,759,761,762,763,765,765,766,768,771,772,773,774,776,
                779,782,783,784,789,791,793,795,796,798,804,805,806,807,808,809,811,812,814,815,816,817,819,820,821,822,823,
                826,827,828,829,831,832,834,836,838,846,847,848,850,851,858,860,861,871,872,874,875,877,878,879,880,882,883,
                886,887,890,893,895,899,900,902,903,904,907,909,910,911,912,914,915,916,917,919,920,922,923,924,927,928,929,
                930,933,935,938,942,944,946,951,952,953,955,957,959,962,963,964,965,967,968,970,971,973,975,976,977,979,982,
                987,989,990,993,994,996,998,999,1000]:
                _change(box, cylinder)
                _change(boxes, cylinders)
                for obj in self.Data['layouts'][I]:
                    if self.Data['layouts'][I][obj]['F_SHAPE'] in box:
                        self.Data['layouts'][I][obj]['F_SHAPE'] = 'cylinder'
                for obj in self.Data['layouts'][F]:
                    if self.Data['layouts'][F][obj]['F_SHAPE'] in boxes:
                        self.Data['layouts'][F][obj]['F_SHAPE'] = 'cylinders'


        # change scenes
        I = self.Data['scenes'][self.scene]['initial']
        F = self.Data['scenes'][self.scene]['final']
        self.Data['scenes'][self.scene]['initial'] = 1000 + I
        self.Data['scenes'][self.scene]['final'] = 1000 + F

        # change layouts
        self.Data['layouts'][1000 + I] = {}
        self.Data['layouts'][1000 + F] = {}
        for obj in self.Data['layouts'][I]:
            self.Data['layouts'][1000 + I][obj] = dict(self.Data['layouts'][I][obj])
        for obj in self.Data['layouts'][F]:
            self.Data['layouts'][1000 + F][obj] = dict(self.Data['layouts'][F][obj])


        # change gripper
        self.Data['gripper'][1000 + I] = self.Data['gripper'][I]
        self.Data['gripper'][1000 + F] = self.Data['gripper'][F]

    # -----------------------------------------------------------------------------------------------------#     print scentences
    def _print_scentenses(self):
        scene = self.scene
        self.sentences = {}
        to_be_poped = []
        for count, i in enumerate(self.Data['commands'][scene]):
            if i not in self.Data['comments']:
                # print count, '-', self.Data['commands'][scene][i]
                self.all_sentences_count += 1
                self.sentences[count] = ['GOOD', self.Data['commands'][scene][i]]
                for word in self.Data['commands'][scene][i].split(' '):
                    if word not in self.all_words:
                        self.all_words.append(word)
            else:
                # print count,'-','SPAM'
                to_be_poped.append(i)
                # print count,'-',self.Data['commands'][scene][i]
                # self.sentences[count] = ['SPAM',self.Data['commands'][scene][i]]
        for i in to_be_poped:
            self.Data['commands'][scene].pop(i)
            self.Data['commands_id'].pop(i)
            self.Data['RCL'].pop(i)
        # print self.all_words
        print len(self.all_words)
        print '--------------------------'

    # -----------------------------------------------------------------------------------------------------#     initilize scene
    def _initialize_scene(self):
        self._add_objects_to_scene()
        self._initialize_robot()

    #-----------------------------------------------------------------------------------------------------#     update scene number
    def _update_scene_number(self):
        self.label.text = 'Scene number : '+str(self.scene)

    # -----------------------------------------------------------------------------------------------------#     find tower objects
    def _get_towers(self, layout):
        groups = {}
        height = {}
        colours = {}
        shapes = {}
        towers = {}
        for obj in layout:
            if obj != 'gripper':
                x = layout[obj]['position'][0]
                y = layout[obj]['position'][1]
                z = layout[obj]['position'][2]
                rgb = layout[obj]['F_HSV']
                shape = layout[obj]['F_SHAPE']
                if shape in ['cube', 'block', 'cube', 'box', 'slab', 'parallelipiped', 'brick', 'square','cylinder', 'can', 'drum']:
                    if (x, y) not in groups:
                        groups[(x, y)] = 1
                        height[(x, y)] = z
                        colours[(x, y)] = rgb
                        shapes[(x, y)] = 'tower'
                    else:
                        groups[(x, y)] += 1
                        if z > height[(x, y)]:
                            height[(x, y)] = z
                        if rgb not in colours[(x, y)]:
                            colours[(x, y)] += '-' + rgb
                        if shape not in shapes[(x, y)]:
                            shapes[(x, y)] += '-' + shape


        for i in groups:
            if groups[i] > 1:
                key = np.max(self.positions.keys()) + 1

                self.positions[key] = {}
                self.positions[key]['x'] = [i[0], i[0]]
                self.positions[key]['y'] = [i[1], i[1]]
                self.positions[key]['z'] = [height[i], height[i]]
                self.positions[key]['F_HSV'] = colours[i]
                self.positions[key]['F_SHAPE'] = 'tower'
                self.positions[key]['moving'] = 0
        print 'self.positions------', self.positions

    # -----------------------------------------------------------------------------------------------------#     add objects to scene
    def _add_objects_to_scene(self):
        self.frame_number = 0
        l1 = self.Data['layouts'][self.Data['scenes'][self.scene]['initial']]  # initial layout
        # print 'l1----------'
        # print l1
        for obj in l1:
            self.total_num_objects += 1
            x = l1[obj]['position'][0]
            y = l1[obj]['position'][1]
            z = l1[obj]['position'][2]

            # inilizing the position vector to be saved later
            self.positions[obj] = {}
            self.positions[obj]['x'] = [int(x)]
            self.positions[obj]['y'] = [int(y)]
            self.positions[obj]['z'] = [int(z)]
            self.positions[obj]['F_HSV'] = l1[obj]['F_HSV']
            self.positions[obj]['F_SHAPE'] = l1[obj]['F_SHAPE']
            # print 'I_move---------',self.Data['scenes'][self.scene]['I_move']
            if obj != self.Data['scenes'][self.scene]['I_move']:
                self.positions[obj]['x'] = [int(x), int(x)]
                self.positions[obj]['y'] = [int(y), int(y)]
                self.positions[obj]['z'] = [int(z), int(z)]
                self.positions[obj]['moving'] = 0
            else:
                self.positions[obj]['moving'] = 1

        self._get_towers(l1)

        I = self.Data['scenes'][self.scene]['I_move']
        l2 = self.Data['layouts'][self.Data['scenes'][self.scene]['final']]  # final layout
        # print '>>>',self.Data['scenes'][self.scene]['F_move']
        for obj in l2:
            if obj == self.Data['scenes'][self.scene]['F_move']:
                x = l2[obj]['position'][0]
                y = l2[obj]['position'][1]
                z = l2[obj]['position'][2]
                # print '>>;',x,y,z
                self.positions[I]['x'].append(int(x))
                self.positions[I]['y'].append(int(y))
                self.positions[I]['z'].append(int(z))

    # -----------------------------------------------------------------------------------------------------#     initilize robot in the scene
    def _initialize_robot(self):
        initial_position = self.Data['gripper'][self.Data['scenes'][self.scene]['initial']]
        final_position = self.Data['gripper'][self.Data['scenes'][self.scene]['final']]

        self.positions['gripper'] = {}
        self.positions['gripper']['x'] = [int(initial_position[0]), int(final_position[0])]
        self.positions['gripper']['y'] = [int(initial_position[1]), int(final_position[1])]
        self.positions['gripper']['z'] = [int(initial_position[2]), int(final_position[2])]

    # -----------------------------------------------------------------------------------------------------#     save motion
    def _save_motion(self):
        F = open(self.image_dir + str(self.scene) + '_sentences' + '.txt', 'w')
        for i in self.sentences:
            # print 'self.sentences_i============',self.sentences[i]
            F.write(self.sentences[i][1] + '\n')
        F.close()

        F = open(self.image_dir + str(self.scene) + '_layout' + '.txt', 'w')
        for key in self.positions:
            F.write('object:' + str(key) + '\n')
            F.write('x:')
            x = self.positions[key]['x']
            F.write(str(x[0]) + ',' + str(x[1]))
            F.write("\n")
            F.write('y:')
            y = self.positions[key]['y']
            F.write(str(y[0]) + ',' + str(y[1]))
            F.write("\n")
            F.write('z:')
            z = self.positions[key]['z']
            F.write(str(z[0]) + ',' + str(z[1]))
            F.write("\n")
            if key != 'gripper':
                c = self.positions[key]['F_HSV']
                s = self.positions[key]['F_SHAPE']
                F.write('F_RGB:' + c)
                F.write("\n")
                F.write('F_SHAPE:' + s)
                F.write("\n")
        F.close()
        print 'self.positions------', self.positions
        pickle.dump(self.positions, open(self.image_dir + str(self.scene) + '_layout.p', 'wb'))
        sentence = {}
        for id in self.Data['commands'][self.scene]:
            sentence[id] = {}
            sentence[id]['text'] = self.Data['commands'][self.scene][id]
            sentence[id]['RCL'] = self.Data['RCL'][id]
        print 'sentence====', sentence
        pickle.dump(sentence, open(self.image_dir + str(self.scene) + '_sentences.p', 'wb'))
    #-----------------------------------------------------------------------------------------------------#     clear scene
    def _clear_scene(self):
        keys = self.object.keys()
        for i in keys:
            self.object[i].visible = False
            self.object.pop(i)
            self.object_shape.pop(i)

