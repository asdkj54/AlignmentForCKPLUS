import matplotlib.pyplot as plt
import numpy as np
import os


### Configuration ###
LANDMARK_PATH = "../Landmarks"
SUBJ_PATH = "../cohn-kanade-images"
SAVE_PATH = "./training"
SUBJ_NUM = 20
IMG_PER_SUBJ_NUM = 5
IMG_INDX = 3 # start from 1

FACE_SHAPE = (320, 280)
VERT_SCALE = 2/3 #  (the distance from center of two eyes to the bottom of image) / (that to the top of image) 

numOfFaces = 11

def get_landmarks(filename):
    x = []
    y = []

    with open(filename) as f:
        while True:
            try:
                lm_str = f.readline().strip().split()
                x.append(float(lm_str[0]))
                y.append(float(lm_str[1]))
            except IndexError:
                break
    return x, y

def get_eyes_corners(filename):
    eyeCornerInx = [36, 39, 42, 45] # index of landmarks for eye corners
    lmX, lmY = get_landmarks(filename)
    eyeCorner = np.zeros((4, 2))
    for i in range(len(eyeCornerInx)):
        eyeCorner[i, 0] = lmX[eyeCornerInx[i]]
        eyeCorner[i, 1] = lmY[eyeCornerInx[i]]
    return eyeCorner[:, 0], eyeCorner[:, 1]

def get_eyes_centers(filename):
    ecX, ecY = get_eyes_corners(filename)
    return np.array([np.mean(ecX[0:2]), np.mean(ecX[2:4])]), np.array([np.mean(ecY[0:2]), np.mean(ecY[2:4])])

def crop_face(img, eyeX, eyeY, shape):
    limY, limX = img.shape
    dsrY, dsrX = shape
    x = np.mean(eyeX)
    y = np.mean(eyeY)

    y1 = int(y - ((1-VERT_SCALE) * dsrY))
    y2 = int(y + (VERT_SCALE * dsrY))
    assert(y1 > 0)
    assert(y2 < limY)

    x1 = int(x - (1/2 * dsrX))
    x2 = int(x + (1/2 * dsrX))
    assert(x1 > 0)
    assert(x2 < limX)

    return img[y1:y2, x1:x2]

def find_subj():
    '''
    find subjects that meet the requirement
    '''
    subj_list =  sorted(os.listdir(SUBJ_PATH))
    candidate_list = []

    for s in subj_list:
        # Check if each subject has enough subgroups
        subgroup_list = os.listdir(SUBJ_PATH+'/'+s)
        # TODO: Check the number in each subgroup
        if len(subgroup_list) >= IMG_PER_SUBJ_NUM:
            candidate_list.append(s)
        if len(candidate_list) >= SUBJ_NUM:
            break
    else:
        raise Warning("There are no enough subjects meet the requirement")
    
    return candidate_list

def extract_subj(candidate_list):
    '''
    extract, alignment the subjects, and save them
    '''
    for s in candidate_list:
        subgroup_list = sorted(os.listdir(SUBJ_PATH+'/'+s))
        # Check save path
        if not os.path.exists(SAVE_PATH+'/'+s):
            print("Creating directory %s" % SAVE_PATH+'/'+s)
            os.makedirs(SAVE_PATH+'/'+s)

        for i in range(IMG_PER_SUBJ_NUM):
            print("Extracting %s" % "{0}/{1}/{2}/{1}_{2}_{3:08d}.png".format(SUBJ_PATH, s, subgroup_list[i], IMG_INDX))
            img = plt.imread("{0}/{1}/{2}/{1}_{2}_{3:08d}.png".format(SUBJ_PATH, s, subgroup_list[i], IMG_INDX))
            lmX, lmY = get_eyes_centers("{0}/{1}/{2}/{1}_{2}_{3:08d}_landmarks.txt".format(LANDMARK_PATH, s, subgroup_list[i], IMG_INDX))
            imgCrop = crop_face(img, lmX, lmY, FACE_SHAPE) # TODO the shape 
            plt.imsave(SAVE_PATH+'/'+s+"/{:03d}.png".format(i), imgCrop, cmap="gray")

def main():
    subjectsList = find_subj()
    extract_subj(subjectsList)

if __name__ == "__main__":
    main()
    
