# Age-and-Gender-Prediction
A CNN model which predicts age and gender from facial images 

## Dataset Info

UTKFACE Dataset contains a wide age range of facial images spanning from 0 to 116 years, containing over 20,000 annotated images, including age, gender, and ethnicity information. The dataset showcases diverse variations in pose, expression, illumination, occlusion, and resolution, presenting a robust challenge for age and gender prediction tasks.each image contains a name with age,gender,ethnicity separated by a '-'.
example of a image name : 80_1_0_20170110140948978.jpg.chip.jpg

## Model Development
This project aims to predict age and gender utilizing UTKFACE dataset by developing a convolutional neural network with various convolution and max pooling layers,dropout and dense layers.

### steps followed:
#### 1. converting to dataframe : 
Started with splitting the name of the image with age and gender labels and creating a dataframe with image ,age and gender as columns 

#### 2. Extracting features :
Features are extracted from the images to enhance the performance

#### 3. Normalizing :
Scaling the pixel values of the images to a range

#### 4. Train Test Validation Split :
The entire dataset(23858 files) is split into train set,test set,validation set and the split is as follows 

total dataset is splitted into 80% train and 20% test and then the train set is further split into train and validation set and the final sizes are 

Train data size: 15268

Validation data size: 3818

Test data size: 4772

#### 5. CNN Model :
It contains one input layer, 4 convolution + max pooling layers and they are flattened and then two parallel dense layers (one for gender detection and one for age prediction ) and dropout layers for both and then output layers which is shown below


![image](https://github.com/Vijayalakshmi2805/Age-and-Gender-Prediction/assets/155812943/a3efc08d-d6ad-4999-96ad-f871e78c7f69)

## Libraries Used

* Pandas
* Numpy
* Matplotlib
* Keras
* Tensorflow
* Scikit-learn

## Results

MAE is chosen for age prediction because it's a suitable metric for regression tasks 
 
Accuracy is chosen for gender prediction because it's a common metric for binary classification tasks

![image](https://github.com/Vijayalakshmi2805/Age-and-Gender-Prediction/assets/155812943/fff925d2-7d63-4cf6-ad3b-df63c12c23a1)















