from pathlib import Path
import os
import numpy as np
import cv2

square_size = 40  # mm size of square
path = Path().absolute()
path = os.path.join(path, str(square_size) + 'mm')
left_p = os.path.join(path, 'left')
right_p = os.path.join(path, 'right')
mtxL = np.loadtxt(os.path.join(path, "mtxL.csv"), delimiter=",")
mtxR = np.loadtxt(os.path.join(path, "mtxR.csv"), delimiter=",")
distL = np.loadtxt(os.path.join(path, "distL.csv"), delimiter=",")
distR = np.loadtxt(os.path.join(path, "distR.csv"), delimiter=",")
OmtxL = np.loadtxt(os.path.join(path, "OmtxL.csv"), delimiter=",")
OmtxR = np.loadtxt(os.path.join(path, "OmtxR.csv"), delimiter=",")
map1L = np.loadtxt(os.path.join(path, "map1L.csv"), delimiter=",")
map2L = np.loadtxt(os.path.join(path, "map2L.csv"), delimiter=",")
map1R = np.loadtxt(os.path.join(path, "map1R.csv"), delimiter=",")
map2R = np.loadtxt(os.path.join(path, "map2R.csv"), delimiter=",")
# map1R = map1R.reshape((480, 640, 2))
# map1L = map1L.reshape((480, 640, 2))

map1R = map1R.reshape((576, 704, 2))
map1L = map1L.reshape((576, 704, 2))

# uncomment the following section for use with test images
id = 12
imgR = cv2.imread(os.path.join(right_p, 'chessboard-R'+str(id)+'.png'))
imgL = cv2.imread(os.path.join(left_p, 'chessboard-L'+str(id)+'.png'))

Left_nice = cv2.remap(imgL, np.int16(map1L), np.int16(map2L), cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT,
                      0)  # Rectify the image using the calibration parameters founds during the initialisation
Right_nice = cv2.remap(imgR, np.int16(map1R), np.int16(map2R), cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
hL, wL = imgL.shape[:2]
hR, wR = imgR.shape[:2]
# Draw Red lines
for line in range(0, int(Right_nice.shape[0] / 20)):  # Draw horizontal lines
    cv2.line(imgR, (0, int(Right_nice.shape[0] / 20 * line)),
             (wR, int(Right_nice.shape[0] / 20 * line)), (0, 0, 255), 1)
    cv2.line(imgL, (0, int(Right_nice.shape[0] / 20 * line)),
             (wL, int(Right_nice.shape[0] / 20 * line)), (0, 0, 255), 1)


for line in range(0, int(imgR.shape[0] / 20)):  # Draw horizontal lines
    cv2.line(Right_nice, (0, int(Right_nice.shape[0] / 20 * line)),
             (wR, int(Right_nice.shape[0] / 20 * line)), (0, 255, 0), 1)
    cv2.line(Left_nice, (0, int(Right_nice.shape[0] / 20 * line)),
             (wL, int(Right_nice.shape[0] / 20 * line)), (0, 255, 0), 1)

# Show the Undistorted images
cv2.imshow('Both Images', np.hstack([Left_nice, Right_nice]))
cv2.imshow('Normal', np.hstack([imgL, imgR]))
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
# Comment the following section for use with test images

CamR = cv2.VideoCapture(1)   # Wenn 1 then Right Cam and wenn 2 Left Cam
CamL = cv2.VideoCapture(2)
while True:
    # Start Reading Camera images
    retR, frameR = CamR.read()
    retL, frameL = CamL.read()

    #####
    hR, wR = frameR.shape[:2]
    hL, wL = frameL.shape[:2]
    # undistorted

    # Rectify the images on rotation and alignment
    Left_nice = cv2.remap(frameL, np.int16(map1L), np.int16(map2L), cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    Right_nice = cv2.remap(frameR, np.int16(map1R), np.int16(map2R), cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    # Draw Red lines
    for line in range(0, int(Right_nice.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
        Left_nice[line * 20, :] = (0, 0, 255)
        Right_nice[line * 20, :] = (0, 0, 255)

    for line in range(0, int(frameR.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
        frameL[line * 20, :] = (0, 255, 0)
        frameR[line * 20, :] = (0, 255, 0)

    # Show the Undistorted images
    cv2.imshow('Both Images', np.hstack([Left_nice, Right_nice]))
    cv2.imshow('Normal', np.hstack([frameL, frameR]))

    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()

'''