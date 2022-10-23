import os
import cv2

# loop through the files in the totest folder
for filename in os.listdir('./totest'):
    # open the file
    img = cv2.imread('./totest/' + filename)
    # show image
    cv2.imshow('image', img)
    # wait for keypress
    k = cv2.waitKey(0)
    # if k == f, move file to dataset/free
    if k == ord('f'):
        os.rename('./totest/' + filename, './dataset/free/' + filename)
    # if k == t, move file to dataset/taken
    elif k == ord('t'):
        os.rename('./totest/' + filename, './dataset/taken/' + filename)
    cv2.destroyAllWindows()