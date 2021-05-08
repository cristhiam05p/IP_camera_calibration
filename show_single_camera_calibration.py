from pathlib import Path
import os
import numpy as np
import cv2

path = Path().absolute()
path = os.path.join(path,'40mm')
left_p = os.path.join(path, 'left')
right_p = os.path.join(path, 'right')
mtxL = np.loadtxt(os.path.join(path,"mtxL.csv"), delimiter=",")
mtxR = np.loadtxt(os.path.join(path,"mtxR.csv"), delimiter=",")
distL = np.loadtxt(os.path.join(path,"distL.csv"), delimiter=",")
distR = np.loadtxt(os.path.join(path,"distR.csv"), delimiter=",")
OmtxL = np.loadtxt(os.path.join(path,"OmtxL.csv"), delimiter=",")
OmtxR = np.loadtxt(os.path.join(path,"OmtxR.csv"), delimiter=",")

id = 19
img_l = cv2.imread(os.path.join(left_p, 'chessboard-L'+str(id)+'.png'))
img_r = cv2.imread(os.path.join(right_p, 'chessboard-R'+str(id)+'.png'))

hL, wL = img_l.shape[:2]
hR, wR = img_r.shape[:2]
mapxL, mapyL = cv2.initUndistortRectifyMap(mtxL, distL, None, OmtxL, (wL, hL), cv2.CV_16SC2)
mapxR, mapyR = cv2.initUndistortRectifyMap(mtxR, distR, None, OmtxR, (wR, hR), cv2.CV_16SC2)

dstL = cv2.remap(img_l, mapxL, mapyL, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
dstR = cv2.remap(img_r, mapxR, mapyR, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

h, w = dstL.shape[:2]
print('width : ' + str(w))
print('heght : ' + str(h))
cv2.line(img_l, (int(wL/2), 0), (int(wL/2), hL), (255, 0, 0), 2)
cv2.line(img_l, (0, int(hL/2)), (wL, int(hL/2)), (255, 0, 0), 2)
cv2.line(dstL, (int(w/2), 0), (int(w/2), h), (255, 0, 0), 2)
cv2.line(dstL, (0, int(h/2)), (w, int(h/2)), (255, 0, 0), 2)

cv2.line(img_r, (int(wR/2), 0), (int(wR/2), hR), (255, 0, 0), 2)
cv2.line(img_r, (0, int(hR/2)), (wR, int(hR/2)), (255, 0, 0), 2)
cv2.line(dstR, (int(w/2), 0), (int(w/2), h), (255, 0, 0), 2)
cv2.line(dstR, (0, int(h/2)), (w, int(h/2)), (255, 0, 0), 2)

#Draw Red lines
for line in range(0, int(dstL.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
    dstL[line * 20, :] = (0, 0, 255)

for line in range(0, int(img_l.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
    img_l[line * 20, :] = (0, 255, 0)
    # Draw Red lines

for line in range(0, int(dstR.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
    dstR[line * 20, :] = (0, 0, 255)

for line in range(0, int(img_r.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
    img_r[line * 20, :] = (0, 255, 0)

cv2.imshow('corrected_l', dstL)
cv2.imshow('image_l', img_l)

cv2.imshow('corrected_r', dstR)
cv2.imshow('image_r', img_r)

cv2.waitKey(0)

'''
# Call the two cameras
CamR = cv2.VideoCapture(1)  # Wenn 1 then Right Cam and wenn 2 Left Cam
CamL = cv2.VideoCapture(2)
while True:
    # Start Reading Camera images
    retR, frameR = CamR.read()
    retL, frameL = CamL.read()

    #####
    hR, wR = frameR.shape[:2]
    hL, wL = frameL.shape[:2]
    # undistort
    mapxL, mapyL = cv2.initUndistortRectifyMap(mtxL, distL, None, OmtxL, (wL, hL), cv2.CV_16SC2)
    dstL = cv2.remap(frameL, mapxL, mapyL, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    mapxR, mapyR = cv2.initUndistortRectifyMap(mtxR, distR, None, OmtxR, (wR, hR), cv2.CV_16SC2)
    dstR = cv2.remap(frameR, mapxR, mapyR, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    #####
    # Draw Red lines
    for line in range(0, int(dstR.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
        dstL[line * 20, :] = (0, 0, 255)
        dstR[line * 20, :] = (0, 0, 255)

    for line in range(0, int(frameR.shape[0] / 20)):  # Draw the Lines on the images Then numer of line is defines by the image Size/20
        frameL[line * 20, :] = (0, 255, 0)
        frameR[line * 20, :] = (0, 255, 0)

    # Show the Undistorted images
    cv2.imshow('Both Images', np.hstack([dstL, dstR]))
    cv2.imshow('Normal', np.hstack([frameL, frameR]))

    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()

'''