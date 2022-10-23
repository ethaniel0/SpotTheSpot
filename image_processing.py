import numpy as np
import cv2
import random
import tensorflow as tf

IMG_SIZE = 69

spots = []

model = tf.keras.models.load_model("LotNeuralNetwork.model")

useImgs = True

def define_spots():
    top_left = (75,85)
    spot_width = 170
    spot_height = 113

    #first column
    for i in range(1,7):
        x = top_left[0]
        y = top_left[1] + i * spot_height
        spots.append(np.array([[x, y], [x, y - spot_height], [x + spot_width, y - spot_height], [x + spot_width, y]]))

    #second column
    top_left = (395, 85)
    for i in range(1,7):
        x = top_left[0]
        y = top_left[1] + i * spot_height
        spots.append(np.array([[x, y], [x, y - spot_height], [x + spot_width, y - spot_height], [x + spot_width, y]]))

def outline_spots(img):
    for spot in spots:
        cv2.polylines(img, [spot], True, (0, 255, 0), 2)

def find_classification_rectangle(spot):
    x, y, w, h = cv2.boundingRect(spot)
    return x, y, w, h

def find_subimage(img, spot):
    x, y, w, h = find_classification_rectangle(spot)
    im = img[y:y+h, x:x+w]
    return cv2.resize(im, (IMG_SIZE, IMG_SIZE))

def classify_subimage(img, spot):
    global useImgs
    print('finding subimage')
    subimage = find_subimage(img, spot)
    cv2.imwrite('./totest/' + str(random.randint(0, 100000)) + '.jpg', subimage)
    return model.predict(np.array([subimage]), verbose=0)

def process(img):
    global spots, useImgs
    define_spots()
    num = 0
    for spot in spots:
        classification = classify_subimage(img, spot)[0]
        num += 1
        print(classification)
        if classification[0] < classification[1]:
            cv2.polylines(img, [spot], True, (0, 0, 0), 2)
        else:
            cv2.polylines(img, [spot], True, (255, 255, 255), 2)
    
    spots = []
    useImgs = True

    return img
