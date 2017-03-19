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
| VERT_SCALE       | (The height of part over the eyes) / (the height of part under the eyes) |
| RESIZE           | Scale used to shrink the original image  |



## 2. Processing

- Searching objects meet the requirement
- Extracting the faces, aligning them according to the center of two eyes, and saving at current directory