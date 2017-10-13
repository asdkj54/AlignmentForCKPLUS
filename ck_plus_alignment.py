import numpy as np
import os
import cv2

'''
TODO
1. Classify the images into different directories according to emotion label. Done
2. Alignment the image according to eye centers. Done
3. Rotation. Done
4. Intensity quatization(CLAHE). Done 
5. Scaling according to the mean of eye center distance. 

'''

### Configuration ###
## Path
LANDMARK_PATH = "../../CK_PLUS/Landmarks"
SUBJ_PATH = "../../CK_PLUS/cohn-kanade-images"
SAVE_PATH = "./training"
LABEL_PATH = "../../CK_PLUS/Emotion"

RESIZE = 1 # scale for the output resize,

FACE_SHAPE = (150, 110) # width, height
VERT_SCALE = 1.9/3   #  (the distance from center of two eyes to the bottom of image) / (that to the top of image) 
HORI_SCALE = 1/2   # (the distance between two eyes) / (the width of image) 

EXPR_DICT = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]

class DirIterate():
    def __init__(self, path, depth=2):
        self.depth = depth
        self.path = path
        self.filesList = []
        
    def find_all(self, pattern, path=None):
        '''
        return all absolute path
        TODO 
        modify to a generator?
        '''
        if path == None:
            path = self.path
        it = os.scandir(path)
        for entry in it:
            if entry.is_dir():
                self.find_all(pattern, path=path+"/"+entry.name)
            elif entry.is_file() and pattern in entry.name:
                self.filesList.append(entry.name)
        return self.filesList
    
class CkPlusAlignment():
    def __init__(self):
        pass

    def get_landmarks(self, filename):
        '''
        Extract all the landmarks from the landmark file, return list of x coordinate and list of y coordinate.
        '''
        x = []
        y = []

        with open(filename) as f:
            while True:
                try:
                    lmStr = f.readline().strip().split()
                    x.append(float(lmStr[0]))
                    y.append(float(lmStr[1]))
                except IndexError: # EOF
                    break
        return x, y

    def get_eyes_corners(self, xLst, yLst, cornerIdxLst):
        '''
        return eye corner coordinates, list of x, and list y. 
        '''
        eyeCorner = np.zeros((4, 2))
        for i, idx in enumerate(cornerIdxLst):
            eyeCorner[i, 0] = xLst[idx]
            eyeCorner[i, 1] = yLst[idx]
        return eyeCorner[:, 0], eyeCorner[:, 1] # 

    def crop_face(self, img, eyeX, eyeY, shape):
        eyeDist = np.abs(eyeX[0] - eyeX[1])
        dsrY, dsrX = shape
        centX = np.mean(eyeX)
        centY = np.mean(eyeY)
        
        limY, limX = img.shape
        
        diffX = eyeDist * (1 / HORI_SCALE) 
        x1 = int(centX - (HORI_SCALE * diffX))
        x2 = int(centX + (HORI_SCALE * diffX))
        assert(x1 > 0)
        assert(x2 < limX)

        scale = diffX / float(dsrX)
        diffY = scale * dsrY

        y1 = int(centY - ((1 - VERT_SCALE) * diffY))
        y2 = int(centY + (VERT_SCALE) * diffY)
        assert(y1 > 0)
        assert(y2 < limY)

        #return cv2.resize(img[y1:y2, x1:x2], shape)
        return img[y1:y2, x1:x2]   

    def hist_equal(self, img):
        # return cv2.equalizeHist(img)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(img)

    def rotate(self, img, lmEyeCentX, lmEyeCentY):
        thi = np.degrees(np.arctan(np.diff(lmEyeCentY) / np.diff(lmEyeCentX)))
        # print("thi = %f" % thi)
        M = cv2.getRotationMatrix2D((np.mean(lmEyeCentX), np.mean(lmEyeCentY)), thi, 1)
        return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

def classify_for_emotions():
    dirIter = DirIterate(LABEL_PATH)
    align = CkPlusAlignment()

    files = dirIter.find_all("txt")

    for i in range(len(files)):
        print("Image No.{:d}".format(i))
        p1, p2, p3, _ = files[i].split('_') # p1: Subject directory, p2: sequence directory, p3: frame number
        with open("{0}/{1}/{2}/{3}".format(LABEL_PATH, p1, p2, files[i])) as f:
            idx = int(float(f.readline().strip(' \n')))
        label = EXPR_DICT[idx]
        src = "{0}/{1}/{2}/{1}_{2}_{3}.png".format(SUBJ_PATH, p1, p2, p3)
        dst = "{0}/{4}/{1}_{2}_{3}.png".format(SAVE_PATH, p1, p2, p3, label)

        img = cv2.imread(src, 0) 
        # Histogram equalization
        img = align.hist_equal(img) 
        # Find all landmarks
        lmX, lmY = align.get_landmarks("{0}/{1}/{2}/{1}_{2}_{3}_landmarks.txt".format(LANDMARK_PATH, p1, p2, p3)) # can be optimized
        # Filter out eye's corner landmarks
        lmEyeCornX, lmEyeCornY = align.get_eyes_corners(lmX, lmY, [36, 39, 42, 45])            
        # Compute eyes' center
        lmEyeCentX, lmEyeCentY = [np.mean(lmEyeCornX[0:2]), np.mean(lmEyeCornX[2:4])], [np.mean(lmEyeCornY[0:2]), np.mean(lmEyeCornY[2:4])]
        # Rotation
        img = align.rotate(img, lmEyeCentX, lmEyeCentY)  
        imgCrop = align.crop_face(img, lmEyeCentX, lmEyeCentY, FACE_SHAPE) 
        imgCropResize = cv2.resize(imgCrop, (int(FACE_SHAPE[1]*RESIZE), int(FACE_SHAPE[0]*RESIZE)))
         
        if not cv2.imwrite(dst, imgCropResize):
            os.makedirs("{0}/{1}".format(SAVE_PATH, label))
            cv2.imwrite(dst, imgCropResize)

def main():
    classify_for_emotions()

    

if __name__ == "__main__":
    main()
    
