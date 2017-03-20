# AlignmentForCKPLUS
A script to implement simple alignment for the CK_PLUS database

## 1. Configuring

| Constant         | Description                              |
| ---------------- | ---------------------------------------- |
| LANDMARK_PATH    | The root of the landmark files           |
| SUBJ_PATH        | The root of the subjects                 |
| SUBJ_NUM         | Number of subjects needed                |
| IMG_PER_SUBJ_NUM | Number of images from each subject       |
| IMG_INDX         | The index of image in each subgroup      |
| FACE_SHAPE       | The shape of the output images           |
| RESIZE           | Scale used to shrink the original image  |
| FACE_SHAPE       | **Desired** shape for the crop_face(), but the output may not be this shape, cause some adjustment in this function |
| VERT_SCALE       | (the distance from center of two eyes to the bottom of image) / (that to the top of image) |
| HORI_SCALE       | (the distance between two eyes) / (the width of image) |



## 2. Processing

- Searching objects meet the requirement
- Extracting the faces, aligning them according to the center of two eyes, and saving at current directory