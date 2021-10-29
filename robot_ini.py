from robot_initialisation import *

R = Robot()
save = 0
save = 'save'		# saving image

for scene in range(1,1001):
    R.scene = scene
    R._initilize_values()
    R._fix_sentences()
    R._change_data()
    R._initialize_scene()                  # place the robot and objects in the initial scene position without saving or motion
    R._print_scentenses()                  # print the sentences on terminal and remove the SPAM sentence
    R._save_motion()                       # save the motion into a text file
    R._clear_scene()

print len(R.all_words)

