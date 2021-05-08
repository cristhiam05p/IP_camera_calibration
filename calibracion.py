import numpy as np
import cv2
from pathlib import Path
import os

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

rows = 5  # number of rows
columns = 3  # number od columns
square_size = 40  # 40 mm size of square

# Prepare object points
objp = np.zeros((rows*columns, 3), np.float32)
objp[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)*square_size   # 20 mm size of square

# Arrays to store object points and image points from all images
objpoints = []   # 3d points in real world space
imgpointsR = []   # 2d points in image plane
imgpointsL = []

path = Path().absolute()
path = os.path.join(path, str(square_size) + 'mm')
left_p = os.path.join(path, 'left')
right_p = os.path.join(path, 'right')

# Start calibration from the camera
print('Starting calibration for the 2 cameras... ')
# Call all saved images
number_images = len([name for name in os.listdir(left_p)])
for i in range(0, number_images):
    t = str(i)
    ChessImaR = cv2.imread(os.path.join(right_p, 'chessboard-R'+t+'.png'), 0)    # Right side
    ChessImaL = cv2.imread(os.path.join(left_p, 'chessboard-L'+t+'.png'), 0)    # Left side
    retR, cornersR = cv2.findChessboardCorners(ChessImaR, (rows, columns), None)  # Define the number of chees corners we are looking for
    retL, cornersL = cv2.findChessboardCorners(ChessImaL, (rows, columns), None)  # Left side
    if (True == retR) & (True == retL):
        objpoints.append(objp)
        cv2.cornerSubPix(ChessImaR, cornersR, (11, 11), (-1, -1), criteria)
        cv2.cornerSubPix(ChessImaL, cornersL, (11, 11), (-1, -1), criteria)
        imgpointsR.append(cornersR)
        imgpointsL.append(cornersL)

#   Right Side
# mtxR = intrinsic matrix Right camera
# distR = distortion coefficients Right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, ChessImaR.shape[::-1], None, None)
hR, wR = ChessImaR.shape[:2]
# OmtxR = optimal new camera intrinsic matrix based on the free scaling parameter. Right camera
OmtxR, roiR = cv2.getOptimalNewCameraMatrix(mtxR, distR, (wR, hR), 1, (wR, hR))

#   Left Side
# mtxL = intrinsic matrix Left camera
# distL = distortion coefficients Left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, ChessImaL.shape[::-1], None, None)
hL, wL = ChessImaL.shape[:2]
# OmtxL = optimal new camera intrinsic matrix based on the free scaling parameter. Left camera
OmtxL, roiL = cv2.getOptimalNewCameraMatrix(mtxL, distL, (wL, hL), 1, (wL, hL))

flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
retS, MLS, dLS, MRS, dRS, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpointsL, imgpointsR, mtxL, distL,  mtxR, distR,
                                                           ChessImaR.shape[::-1], criteria_stereo, flags)
# StereoRectify function
rectify_scale = -1  # if 0 image croped, if 1 image not croped
RL, RR, PL, PR, Q, roiL, roiR = cv2.stereoRectify(MLS, dLS, MRS, dRS, ChessImaR.shape[::-1], R, T, rectify_scale,
                                                  (-1, -1))  # last paramater is alpha, if 0= croped, if 1= not croped
# initUndistortRectifyMap function
Left_Stereo_Map = cv2.initUndistortRectifyMap(MLS, dLS, RL, PL, ChessImaR.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map = cv2.initUndistortRectifyMap(MRS, dRS, RR, PR, ChessImaR.shape[::-1], cv2.CV_16SC2)

np.savetxt(os.path.join(path, "mtxL.csv"), mtxL, delimiter=",", fmt='%10.8f')
np.savetxt(os.path.join(path, "mtxR.csv"), mtxR, delimiter=",", fmt='%10.8f')
np.savetxt(os.path.join(path, "distL.csv"), distL, delimiter=",", fmt='%10.8f')
np.savetxt(os.path.join(path, "distR.csv"), distR, delimiter=",", fmt='%10.8f')
np.savetxt(os.path.join(path, "OmtxL.csv"), OmtxL, delimiter=",", fmt='%10.8f')
np.savetxt(os.path.join(path, "OmtxR.csv"), OmtxR, delimiter=",", fmt='%10.8f')

map1R = Right_Stereo_Map[0]  # 3d
map2R = Right_Stereo_Map[1]  # 2d
map1L = Left_Stereo_Map[0]  # 3d
map2L = Left_Stereo_Map[1]  # 2d

np.savetxt(os.path.join(path, "map2L.csv"), map2L, delimiter=",")
np.savetxt(os.path.join(path, "map2R.csv"), map2R, delimiter=",")
with open(os.path.join(path, "map1R.csv"), 'w') as outfile:
    for slice_2d in map1R:
        np.savetxt(outfile, slice_2d, delimiter=",")
        outfile.write('# New slice\n')
with open(os.path.join(path, "map1L.csv"), 'w') as outfile:
    for slice_2d in map1L:
        np.savetxt(outfile, slice_2d, delimiter=",")
        outfile.write('# New slice\n')




