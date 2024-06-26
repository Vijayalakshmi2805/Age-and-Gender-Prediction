# -*- coding: utf-8 -*-
"""ml-project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JIkqLkl-1qyGLQEcQD5xoP9TqThmbQBb
"""

!pip install tqdm

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')
# %matplotlib inline

import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D, Input

BASE_DIR = '/content/drive/MyDrive/UTKFace'

filenames = os.listdir(BASE_DIR)
print("A single filename:", filenames[0])

# labels - age, gender, ethnicity
image_paths = []
age_labels = []
gender_labels = []

for filename in tqdm(os.listdir(BASE_DIR)):
    image_path = os.path.join(BASE_DIR, filename)
    temp = filename.split('_')
    age = int(temp[0])
    gender = int(temp[1])
    image_paths.append(image_path)
    age_labels.append(age)
    gender_labels.append(gender)

print("Number of images:", len(image_paths))
print("Sample image path:", image_paths[0])
print("Sample age label:", age_labels[0])
print("Sample gender label:", gender_labels[0])

# convert to dataframe
df = pd.DataFrame()
df['image'], df['age'], df['gender'] = image_paths, age_labels, gender_labels
df.head()

# map labels for gender
gender_dict = {0:'Male', 1:'Female'}

from PIL import Image
img = Image.open(df['image'][0])
plt.axis('off')
plt.imshow(img);

sns.distplot(df['age'])

# to display grid of images
plt.figure(figsize=(20, 20))
#files = df.iloc[0:25]
random_files = df.sample(n=25)  # Randomly select 25 samples
random_files.reset_index(drop=True, inplace=True) # Reset index for consecutive numbering


for index, file, age, gender in random_files.itertuples():
    plt.subplot(5, 5, index+1)
    img = load_img(file)
    img = np.array(img)
    plt.imshow(img)
    plt.title(f"Age: {age} Gender: {gender_dict[gender]}")
    plt.axis('off')

def extract_features(images):
    features = []
    for image in tqdm(images):
        img = load_img(image, color_mode='grayscale')
        img = img.resize((128, 128), Image.ANTIALIAS)
        img = np.array(img)
        features.append(img)

    features = np.array(features)
    # ignore this step if using RGB
    features = features.reshape(len(features), 128, 128, 1)
    return features

X = extract_features(df['image'])

#print("sample feature :",X[0])
X.shape

# normalize the images
X = X/255.0

y_gender = np.array(df['gender'])
y_age = np.array(df['age'])

input_shape = (128, 128, 1)

from sklearn.model_selection import train_test_split

# Splitting data into train and test sets (80% train, 20% test)
X_train, X_test, y_gender_train, y_gender_test, y_age_train, y_age_test = train_test_split(X, y_gender, y_age, test_size=0.2, random_state=42)

# Further splitting train data into train and validation sets (80% train, 20% validation)
X_train, X_val, y_gender_train, y_gender_val, y_age_train, y_age_val = train_test_split(X_train, y_gender_train, y_age_train, test_size=0.2, random_state=42)

# Print the sizes of the splits
print("Train data size:", X_train.shape[0])
print("Validation data size:", X_val.shape[0])
print("Test data size:", X_test.shape[0])

inputs = Input((input_shape))
# convolutional layers
conv_1 = Conv2D(32, kernel_size=(3, 3), activation='relu') (inputs)
maxp_1 = MaxPooling2D(pool_size=(2, 2)) (conv_1)
conv_2 = Conv2D(64, kernel_size=(3, 3), activation='relu') (maxp_1)
maxp_2 = MaxPooling2D(pool_size=(2, 2)) (conv_2)
conv_3 = Conv2D(128, kernel_size=(3, 3), activation='relu') (maxp_2)
maxp_3 = MaxPooling2D(pool_size=(2, 2)) (conv_3)
conv_4 = Conv2D(256, kernel_size=(3, 3), activation='relu') (maxp_3)
maxp_4 = MaxPooling2D(pool_size=(2, 2)) (conv_4)

flatten = Flatten() (maxp_4)

# fully connected layers
dense_1 = Dense(256, activation='relu') (flatten)
dense_2 = Dense(256, activation='relu') (flatten)

dropout_1 = Dropout(0.4) (dense_1)
dropout_2 = Dropout(0.4) (dense_2)

output_1 = Dense(1, activation='sigmoid', name='gender_out') (dropout_1)
output_2 = Dense(1, activation='relu', name='age_out') (dropout_2)

model = Model(inputs=[inputs], outputs=[output_1, output_2])

model.compile(loss=['binary_crossentropy', 'mae'], optimizer='adam', metrics=['accuracy', 'mae'])

# plot the model
from tensorflow.keras.utils import plot_model
plot_model(model)

# Train model using train and validation data
history = model.fit(x=X_train, y=[y_gender_train, y_age_train], batch_size=32, epochs=30, validation_data=(X_val, [y_gender_val, y_age_val]))

# Evaluate model using test data
#test_results = model.evaluate(x=X_test, y=[y_gender_test, y_age_test])
#print("Test Loss:", test_results[0])
#print("Gender Test Accuracy:", test_results[1])
#print("Age Test MAE:", test_results[2])

# Evaluate model using test data
test_results = model.evaluate(x=X_test, y=[y_gender_test, y_age_test])
print("Test Loss:", test_results[0])
print("Gender Test Accuracy:", test_results[3])
print("Age Test MAE:", test_results[6])

# plot results for gender
acc = history.history['gender_out_accuracy']
val_acc = history.history['val_gender_out_accuracy']
epochs = range(len(acc))

plt.plot(epochs, acc, 'b', label='Training Accuracy')
plt.plot(epochs, val_acc, 'r', label='Validation Accuracy')
plt.title('Accuracy Graph')
plt.legend()
plt.figure()

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.plot(epochs, loss, 'b', label='Training Loss')
plt.plot(epochs, val_loss, 'r', label='Validation Loss')
plt.title('Loss Graph')
plt.legend()
plt.show()

# plot results for age
loss = history.history['age_out_mae']
val_loss = history.history['val_age_out_mae']
epochs = range(len(loss))

plt.plot(epochs, loss, 'b', label='Training MAE')
plt.plot(epochs, val_loss, 'r', label='Validation MAE')
plt.title('Loss Graph')
plt.legend()
plt.show()