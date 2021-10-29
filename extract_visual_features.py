import math as m
import pickle
from sklearn import mixture
from sklearn import metrics
from sklearn import svm
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def _read_pickle(scene):
    pkl_file = './data/scenes/'+str(scene)+'_layout.p'
    data = open(pkl_file, 'rb')
    positions = pickle.load(data)
    return positions

def _get_actions(positions):
    actions = []
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            if positions[obj]['moving']:
                mov_obj = obj
                break
    if mov_obj != None:
        x_O = positions[mov_obj]['x']
        y_O = positions[mov_obj]['y']
        z_O = positions[mov_obj]['z']

        x_R = positions['gripper']['x']
        y_R = positions['gripper']['y']
        z_R = positions['gripper']['z']

        # check if it's a pick up
        if x_O[1] == x_R[1] and y_O[1] == y_R[1] and z_O[1] == z_R[1]:
            actions = ["pick", "remove", "take", "pick up"]
        elif x_O[0] == x_R[0] and y_O[0] == y_R[0] and z_O[0] == z_R[0]:
            actions = ["put", "place", "drop", "down", "put down"]
        elif x_O[0] != x_O[1] or y_O[0] != y_O[1] or z_O[0] != z_O[1]:
            actions = ["move", "shift", "stack"]
    else:
        actions = []
    return actions

def _get_trees(actions, positions):
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            if positions[obj]['moving']:
                mov_obj = obj
                break

    if mov_obj != None:
        x = positions[mov_obj]['x']
        y = positions[mov_obj]['y']
        z = positions[mov_obj]['z']

    tree = {}
    if actions == ["pick", "remove", "take", "pick up"]:
        tree['NLTK'] = "(V (Action "+actions[0]+") (Entity id_"+str(mov_obj)+"))"
        tree['py'] = {}
        tree['py']['A'] = actions[0]
        tree['py']['E'] = mov_obj
    elif actions == ["put", "place", "drop", "down", "put down"]:
        tree['NLTK'] = "(V (Action "+actions[0]+") (Entity id_"+str(mov_obj)+"))"
        tree['py'] = {}
        tree['py']['A'] = actions[0]
        tree['py']['E'] = mov_obj
    elif actions == ["move", "shift", "stack"]:
        tree['NLTK'] = "(V (Action "+actions[0]+") (Entity id_"+str(mov_obj)+") (Destination "+str(x[1])+","+str(y[1])+","+str(z[1])+"))"
        tree['py'] = {}
        tree['py']['A'] = actions[0]
        tree['py']['E'] = mov_obj
        tree['py']['D'] = [x[1], y[1], z[1]]
    elif actions == ['nothing']:
        tree['NLTK'] = "(V (Action "+actions[0]+"))"
        tree['py'] = {}
        tree['py']['A'] = actions[0]
    return tree

def _get_locations(positions):
    locations = []
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            if positions[obj]['moving']:
                mov_obj = obj
                break
    if mov_obj != None:
        x = positions[mov_obj]['x']
        y = positions[mov_obj]['y']
        if x[0] < 3 and y[0] < 3:
            locations.append([1, 1])
        if x[0] < 3 and 2 < y[0] < 5:
            locations.append([1, 3.5])
        if x[0] < 3 and y[0] > 4:
            locations.append([1, 6])

        if 3 < x[0] < 5 and y[0] < 3:
            locations.append([3.5, 1])
        if 3 < x[0] < 5 and 2 < y[0] < 5:
            locations.append([3.5, 3.5])
        if 3 < x[0] < 5 and y[0] > 4:
            locations.append([3.5, 6])

        if x[0] > 5 and y[0] < 3:
            locations.append([6, 1])
        if x[0] > 5 and 2 < y[0] < 5:
            locations.append([6, 3.5])
        if x[0] > 5 and y[0] > 4:
            locations.append([6, 6])

        if x[1] < 3 and y[1] < 3:
            locations.append([1, 1])
        if x[1] < 3 and 2 < y[1] < 5:
            locations.append([1, 3.5])
        if x[1] < 3 and y[1] > 4:
            locations.append([1, 6])

        if 3 < x[1] < 5 and y[1] < 3:
            locations.append([3.5, 1])
        if 3 < x[1] < 5 and 2 < y[1] < 5:
            locations.append([3.5, 3.5])
        if 3 < x[1] < 5 and y[1] > 4:
            locations.append([3.5, 6])

        if x[1] > 5 and y[1] < 3:
            locations.append([6, 1])
        if x[1] > 5 and 2 < y[1] < 5:
            locations.append([6, 3.5])
        if x[1] > 5 and y[1] > 4:
            locations.append([6, 6])

    return locations

def _get_locations2(positions):
    locations = []
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            x = positions[obj]['x'][1]
            y = positions[obj]['y'][1]

            if [x, y] not in locations:
                locations.append([x, y])

    return locations

def _get_colors(positions):
    colors = []
    for obj in positions:
        if obj != 'gripper':
            color = positions[obj]['F_HSV']
            for c in color.split('-'):
                if c not in colors:
                    colors.append(c)
    return colors

def _get_shapes(positions):
    shapes = []
    for obj in positions:
        if obj != 'gripper':
            shape = positions[obj]['F_SHAPE']
            for s in shape.split('-'):
                if s not in shapes:
                    shapes.append(s)
    return shapes

def _get_distances(positions):
    distances = []
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            if positions[obj]['moving']:
                mov_obj = obj
                break
    if mov_obj != None:
        x1 = positions[mov_obj]['x']
        y1 = positions[mov_obj]['y']
        z1 = positions[mov_obj]['z']
        for obj in positions:
            if obj != 'gripper' and obj != mov_obj:
                x2 = positions[obj]['x']
                y2 = positions[obj]['y']
                z2 = positions[obj]['z']
                d = [np.abs(x1[0]-x2[0]), np.abs(x1[1]-x2[1]), np.abs(y1[0]-y2[0]), np.abs(y1[1]-y2[1]), np.abs(z1[0]-z2[0]), np.abs(z1[1]-z2[1])]
                for i in d:
                    if i not in distances:
                        distances.append(i)
    return distances

def cart2sph(x, y, z):

    XsqPlusYsq = x ** 2 + y ** 2
    r = m.sqrt(XsqPlusYsq + z ** 2)  # r
    theta = m.atan2(z, m.sqrt(XsqPlusYsq)) * 180 / np.pi  # theta
    # print 'theta---', theta
    azimuth = m.atan2(y, x) * 180 / np.pi  # phi
    # print 'azimuth===', azimuth

    return r, theta, azimuth

def _func_directions(dx,dy,dz):
        dx = float(dx)
        dy = float(dy)
        dz = float(dz)
        max = np.max(np.abs([dx,dy,dz]))
        if np.abs(dx)/max < .5:
            dx = 0
        else:
            dx = np.sign(dx)

        if np.abs(dy)/max < .5:
            dy = 0
        else:
            dy = np.sign(dy)

        if np.abs(dz)/max < .5:
            dz = 0
        else:
            dz = np.sign(dz)
        return dx,dy,dz

def _get_directions(positions):

    directions = []
    azimuthal_coordinates = []
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            if positions[obj]['moving']:
                mov_obj = obj
                break
    if mov_obj != None:
        # x1,y1,z1 are move_obj's positions
        x1 = positions[mov_obj]['x']
        y1 = positions[mov_obj]['y']
        z1 = positions[mov_obj]['z']
        for obj in positions:
            if obj != 'gripper' and obj != mov_obj:
                # x2,y2,z2 are move_obj's positions
                x2 = positions[obj]['x']
                y2 = positions[obj]['y']
                z2 = positions[obj]['z']
                az_coordinates_0 = cart2sph(x1[0]-x2[0], y1[0]-y2[0], z1[0]-z2[0])
                d = _func_directions(x1[0]-x2[0],y1[0]-y2[0],z1[0]-z2[0])
                if d not in directions:
                    directions.append(d)
                # if az_coordinates_0 not in azimuthal_coordinates:
                #     azimuthal_coordinates.append(az_coordinates_0)

                az_coordinates_1 = cart2sph(x1[1]-x2[1],y1[1]-y2[1],z1[1]-z2[1])
                d = _func_directions(x1[1]-x2[1],y1[1]-y2[1],z1[1]-z2[1])
                if d not in directions:
                    directions.append(d)
                # if az_coordinates_1 not in azimuthal_coordinates:
                #     azimuthal_coordinates.append(az_coordinates_1)
    return directions

def _get_directions2(positions):
    directions = []
    mov_obj = None
    for obj in positions:
        if obj != 'gripper':
            if positions[obj]['moving']:
                mov_obj = obj
                break
    for obj1 in positions:
        if obj1 != mov_obj:
            continue
        # x1,y1,z1 are the positions of an object that has not been moved
        x1 = positions[obj1]['x']
        y1 = positions[obj1]['y']
        z1 = positions[obj1]['z']
        for obj2 in positions:
            # x2,y2,z2 are the coordinates of an object that has not moved and is different from obj1 that has not moved
            if obj2 != 'gripper' and obj2 != obj1:
                x2 = positions[obj2]['x']
                y2 = positions[obj2]['y']
                z2 = positions[obj2]['z']
                # d = cart2sph(x1[0]-x2[0],y1[0]-y2[0],z1[0]-z2[0])
                d = [x1[0]-x2[0], y1[0]-y2[0], z1[0]-z2[0]]
                dx = float(d[0])
                dy = float(d[1])
                dz = float(d[2])
                max = np.max(np.abs([dx,dy,dz]))
                if max != 0:
                    d = _func_directions(x1[0]-x2[0], y1[0]-y2[0], z1[0]-z2[0])
                    # d = [d[0]/max, d[1]/max, d[2]/max]
                # print "---",d
                # d = _func_directions(x1[0]-x2[0],y1[0]-y2[0],z1[0]-z2[0])
                # if d not in directions:
                directions.append(d)
                # # d = cart2sph(x1[1]-x2[1],y1[1]-y2[1],z1[1]-z2[1])
                # d = _func_directions(x1[1]-x2[1],y1[1]-y2[1],z1[1]-z2[1])
                # if d not in directions:
                #     directions.append(d)
    return directions


def _cluster_data(X, GT, name, n):
    print name
    best_v = 0
    for i in range(4):
        print '#####',i
        n_components_range = range(4, n)
        cv_types = ['spherical', 'tied', 'diag', 'full']
        lowest_bic = np.infty
        for cv_type in cv_types:
            for n_components in n_components_range:
                gmm = mixture.GaussianMixture(n_components=n_components, covariance_type=cv_type)
                gmm.fit(X)
                Y_ = gmm.predict(X)
                bic = gmm.bic(X)
                if bic < lowest_bic:
                    lowest_bic = bic
                    best_gmm = gmm
                    final_Y_ = Y_

    pickle.dump([final_Y_, best_gmm], open('./results/'+name+'_clusters.p', "wb"))
    _print_results(GT, final_Y_, best_gmm)




def _append_data(data, X_, unique_, GT_, mean, sigma):
    for i in data:
        if i not in unique_:
            unique_.append(i)

        d = unique_.index(i) + np.random.normal(mean, sigma, 1)
        if X_ == []:
            X_ = [d]
            # print 'dddddd',d
        else:
            X_ = np.vstack((X_,d))
        GT_.append(i)
    return X_, unique_, GT_

def _append_data2(data, X_, unique_, GT_, mean, sigma):
    for i in data:
        if i not in unique_:
            unique_.append(i)

        d = i + np.random.multivariate_normal(mean, sigma, 1)[0]

        if X_ == []:
            X_ = [d]
        else:
            X_ = np.vstack((X_,d))
        GT_.append(unique_.index(i))
    return X_, unique_, GT_

def _append_data3(data, X_, unique_, GT_, mean, sigma):
    for i in data:

        du = _func_directions(i[0], i[1], i[2])
        if du not in unique_:
            unique_.append(du)

        if X_ == []:
            X_ = [i]
        else:
            X_ = np.vstack((X_,i))
        GT_.append(unique_.index(du))
    return X_, unique_, GT_

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    lists = []
    for i in range(n):
        list1 = np.arange( i*l/n+1 , (i+1)*l/n+1 )
        lists.append(list1)
    return lists

def _print_results(GT,Y_,best_gmm):
    #print v_measure_score(GT, Y_)
    true_labels = GT
    pred_labels = Y_
    print "\n dataset unique labels:", len(set(true_labels))
    print "number of clusters:", len(best_gmm.means_)
    print("Mutual Information: %.2f" % metrics.mutual_info_score(true_labels, pred_labels))
    print("Adjusted Mutual Information: %0.2f" % metrics.normalized_mutual_info_score(true_labels, pred_labels))
    print("Homogeneity: %0.2f" % metrics.homogeneity_score(true_labels, pred_labels))
    print("Completeness: %0.2f" % metrics.completeness_score(true_labels, pred_labels))
    print("V-measure: %0.2f" % metrics.v_measure_score(true_labels, pred_labels))

def _pretty_plot_directions():
    final_Y_, best_gmm = pickle.load( open( './results/directions_clusters.p', "rb" ) )
    print 'best_gmm.means_',best_gmm.means_
    mpl.rcParams['legend.fontsize'] = 10

    for cluster in range(9):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        counter = 0
        ax.plot([0, 1], [0, 0], [0, 0], 'r', linewidth=3)
        ax.plot([0, 0], [0, 1], [0, 0], 'g', linewidth=3)
        ax.plot([0, 0], [0, 0], [0, 1], 'b', linewidth=3)
        for i,j in zip(X_directions, final_Y_):
            if counter == 110:
                break
            if j == cluster: #0:
                # print i
                counter += 1
                # theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
                # r = z**2 + 1
                d = np.sqrt(i[0]**2 + i[1]**2 + i[2]**2)
                # print i,d
                if d != 0:
                    x = [0,i[0]/d]
                    y = [0,i[1]/d]
                    z = [0,i[2]/d]
                    ax.plot(x, y, z, 'y')
        ax.set_xlim([-1,1])
        ax.set_ylim([-1,1])
        ax.set_zlim([-1,1])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        fig.savefig('./results/directions/'+str(cluster)+'_cluster.png')
        plt.show()

def _pretty_plot_locations():
    clusters = {}
    XY = X_locations*180/9+10
    # print GT_locations
    Y_, best_gmm = pickle.load(open( './results/locations_clusters.p', "rb" ) )
    # print XY
    for x,val in zip(XY,Y_):
        if val not in clusters:
            clusters[val] = np.zeros((200, 200, 3), dtype=np.uint8)
        a, b = x
        a = int(a)
        b = int(b)
        for i in range(10):
            clusters[val][a-i:a+i, b-i:b+i, :] += 1
        if np.max(clusters[val]) == 255:
            clusters[val] *= 244/255
    avg_images = {}
    for c in clusters:
        plt.matshow(clusters[c][:, :, 0])
        plt.axis("off")
        plt.savefig('./results/locations/'+str(c)+'_cluster.png')



def _svm(x,y,x_test,y_test):
    clf = svm.SVC(kernel='linear')
    clf.fit(x, y)
    A = clf.predict(x_test)
    mean = metrics.v_measure_score(y_test, A)
    print '-------'
    print("supervised V-measure: %0.2f" % mean)



##########################################################################
# save values for further analysis
##########################################################################
for scene in range(1,1001):
    print 'extracting feature from scene : ',scene
    pkl_file = './learning/'+str(scene)+'_visual_features.p'
    VF = {}
    positions = _read_pickle(scene)
    VF['actions'] = _get_actions(positions)
    VF['locations'] = _get_locations(positions)
    VF['color'] = _get_colors(positions)
    VF['type'] = _get_shapes(positions)
    # VF['distances'] = _get_distances(positions)
    VF['relation'] = _get_directions(positions)
    # VF['temporal'] = _get_temporal(VF['actions'])
    # print 'len(VF_actions---)',len(VF['actions'])
    # print 'len(positions)',len(positions)
    trees = _get_trees(VF['actions'], positions)
    pickle.dump([VF,trees], open(pkl_file, 'wb'))
    print 'tree-----', trees


##########################################################################
# Clustering analysis
##########################################################################
four_folds = chunks(1000,4)

for test in range(1):
    X_colours = []
    X_colours_t = []
    GT_colours = []
    GT_colours_t = []
    unique_colours = []

    X_shapes = []
    GT_shapes = []
    X_shapes_t = []
    GT_shapes_t = []
    unique_shapes = []

    X_locations = []
    GT_locations = []
    X_locations_t = []
    GT_locations_t = []
    unique_locations = []

    X_directions = []
    GT_directions = []
    X_directions_t = []
    GT_directions_t = []
    unique_directions = []

    for c, data in enumerate(four_folds):
        if c != test:
            for scene in data:
                print 'c != test: scene------',scene
                pkl_file = './learning/'+str(scene)+'_visual_features.p'
                positions = _read_pickle(scene)
                X_colours, unique_colours, GT_colours           = _append_data(_get_colors(positions), X_colours, unique_colours, GT_colours, 0, .3)
                X_shapes, unique_shapes, GT_shapes              = _append_data(_get_shapes(positions), X_shapes, unique_shapes, GT_shapes, 0, .2)
                X_locations, unique_locations, GT_locations     = _append_data2(_get_locations2(positions), X_locations, unique_locations, GT_locations, [0,0], [[.2, 0], [0, .2]])
                X_directions, unique_directions, GT_directions  = _append_data3(_get_directions2(positions), X_directions, unique_directions, GT_directions, [0,0], [[0, 0], [0, 0]])
        if c == test:
            for scene in data:
                print 'c = test: scene------',scene
                pkl_file = './learning/'+str(scene)+'_visual_features.p'
                positions = _read_pickle(scene)
                X_colours_t, unique_colours, GT_colours_t           = _append_data(_get_colors(positions), X_colours_t, unique_colours, GT_colours_t, 0, .3)
                X_shapes_t, unique_shapes, GT_shapes_t              = _append_data(_get_shapes(positions), X_shapes_t, unique_shapes, GT_shapes_t, 0, .2)
                X_locations_t, unique_locations, GT_locations_t     = _append_data2(_get_locations2(positions), X_locations_t, unique_locations, GT_locations_t, [0,0], [[.2, 0], [0, .2]])
                X_directions_t, unique_directions, GT_directions_t  = _append_data3(_get_directions2(positions), X_directions_t, unique_directions, GT_directions_t, [0,0], [[0, 0], [0, 0]])


    # print X_colours_t
    # print unique_directions
    # print GT_colours_t

    _cluster_data(X_colours, GT_colours, "colours", 9)
    _svm(X_colours, GT_colours, X_colours_t, GT_colours_t)

    _cluster_data(X_shapes, GT_shapes, "shapes", 6)
    _svm(X_shapes, GT_shapes, X_shapes_t, GT_shapes_t)

    _cluster_data(X_locations, GT_locations, "locations", 9)
    _svm(X_locations, GT_locations, X_locations_t, GT_locations_t)

    _cluster_data(X_directions, GT_directions, "directions", 6)
    _svm(X_directions, GT_directions, X_directions_t, GT_directions_t)

