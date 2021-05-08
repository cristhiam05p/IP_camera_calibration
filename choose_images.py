import cv2
from pathlib import Path
import os

id_image = 0
id_save = 0
rows = 5  # number of rows
columns = 3  # number od columns
square_size = 40  # 40 mm size of square
path = Path().absolute()
path = os.path.join(path, str(square_size) + 'mm')
Path(path).mkdir(parents=True, exist_ok=True)
left_p = os.path.join(path, 'left')
right_p = os.path.join(path, 'right')
Path(left_p).mkdir(parents=True, exist_ok=True)
Path(right_p).mkdir(parents=True, exist_ok=True)
path_R = r"C:\Users\Cristhiam\OneDrive - Universidad Nacional de Colombia\Desktop\Drone detection\Scripts\Stereo-Vision\ip_cameras\40mm_test\right"
path_L = r"C:\Users\Cristhiam\OneDrive - Universidad Nacional de Colombia\Desktop\Drone detection\Scripts\Stereo-Vision\ip_cameras\40mm_test\left"
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#rtsp_link1 = "rtsp://admin:123456@192.168.1.168/sub"
#rtsp_link2 = "rtsp://admin:123456@192.168.1.169/sub"

# Call the two cameras
#CamR = cv2.VideoCapture(rtsp_link1)   # 1 -> Right Camera
#CamL = cv2.VideoCapture(rtsp_link2)   # 2 -> Left Camera

while True:
    #retR, frameR = CamR.read()
    #retL, frameL = CamL.read()
    str_id_image = str(id_image)
    frameR = cv2.imread(os.path.join(path_R, 'chessboard-R'+str_id_image+'.png'))
    frameL = cv2.imread(os.path.join(path_L, 'chessboard-R' + str_id_image + '.png'))
    if frameR is not None and frameL is not None:
        cv2.imshow('imgR', frameR)
        cv2.imshow('imgL', frameL)

        grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
        grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        retR, cornersR = cv2.findChessboardCorners(grayR, (rows, columns), None)  # Define the number of chess corners (here 12 by 7) we are looking for with the right Camera
        retL, cornersL = cv2.findChessboardCorners(grayL, (rows, columns), None)  # Same with the left camera

        cv2.imshow('imgR', frameR)
        cv2.imshow('imgL', frameL)

        # If Chess board corners were found
        if (retR == True) & (retL == True):
            corners2R = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)    # Refining the Position
            corners2L = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)

            # Draw and display the corners
            cv2.drawChessboardCorners(grayR, (rows, columns), corners2R, retR)
            cv2.drawChessboardCorners(grayL, (rows, columns), corners2L, retL)

            cv2.imshow('VideoR', grayR)
            cv2.imshow('VideoL', grayL)

            if cv2.waitKey(0) & 0xFF == ord('s'):   # Press 's' to save
                str_id_image = str(id_save)
                print('Images ' + str_id_image + ' saved for right and left cameras')
                cv2.imwrite(os.path.join(right_p, 'chessboard-R'+str_id_image+'.png'), frameR)
                cv2.imwrite(os.path.join(left_p, 'chessboard-L'+str_id_image+'.png'), frameL)
                id_save = id_save+1
            else:
                print('Images not saved')
    id_image = id_image + 1
    if cv2.waitKey(1) & 0xFF == ord(' '):   # space bar to exit
        break

#CamR.release()
#CamL.release()
cv2.destroyAllWindows()
