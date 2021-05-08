import cv2
from threading import Thread, Lock
from multiprocessing import Process, Queue, Event
import time
from pathlib import Path
import os


class Camera:

    last_frame = None
    last_ready = None
    lock = Lock()

    def __init__(self, rtsp_link):
        capture = cv2.VideoCapture(rtsp_link)
        thread = Thread(target=self.rtsp_cam_buffer, args=(capture,), name="rtsp_read_thread")
        thread.daemon = True
        thread.start()

    def rtsp_cam_buffer(self, capture):
        while True:
            with self.lock:
                self.last_ready, self.last_frame = capture.read()

    def getFrame(self):
        if (self.last_ready is not None) and (self.last_frame is not None):
            return self.last_frame.copy()
        else:
            return None


def create_camera(rtsp_link, path):
    rows = 5  # number of rows
    columns = 3  # number od columns
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    id_save = 0
    video_stream1 = Camera(rtsp_link)
    while True:
        frame = video_stream1.getFrame()
        if frame is not None:
            cv2.imshow(rtsp_link, frame)
            grayR = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            retR, cornersR = cv2.findChessboardCorners(grayR, (rows, columns), None)
            if (retR == True):
                corners2R = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)  # Refining the Position
                cv2.drawChessboardCorners(grayR, (rows, columns), corners2R, retR)
                cv2.imshow(rtsp_link, grayR)
                if cv2.waitKey(0) & 0xFF == ord('s'):  # Press 's' to save
                    str_id_image = str(id_save)
                    print('Images ' + str_id_image + ' saved for right and left cameras')
                    cv2.imwrite(os.path.join(path, 'chessboard-R' + str_id_image + '.png'), frame)
                    id_save = id_save + 1
                else:
                    print('Images not saved')
        pressedkey = cv2.waitKey(1) & 0xff
        if pressedkey == ord('q'):
            break
        time.sleep(0.01)
    cv2.destroyAllWindows()


def multiprocess(rtsp_link1, rtsp_link2, right_p, left_p):
    process1 = Process(target=create_camera, args=(rtsp_link1, right_p), name=f"proceso_{rtsp_link1}")
    process2 = Process(target=create_camera, args=(rtsp_link2, left_p), name=f"proceso_{rtsp_link2}")
    process1.daemon = True
    process2.daemon = True
    process1.start()
    process2.start()
    process1.join()
    process2.join()


if __name__ == '__main__':
    square_size = 40  # 40 mm size of square
    path = Path().absolute()
    path = os.path.join(path, str(square_size) + 'mm_test')
    Path(path).mkdir(parents=True, exist_ok=True)
    left_p = os.path.join(path, 'left')
    right_p = os.path.join(path, 'right')
    Path(left_p).mkdir(parents=True, exist_ok=True)
    Path(right_p).mkdir(parents=True, exist_ok=True)

    q = Queue(maxsize=1)
    stop_process = Event()

    rtsp_link1 = "rtsp://admin:123456@192.168.1.168/sub"
    rtsp_link2 = "rtsp://admin:123456@192.168.1.169/sub"

    multiprocess(rtsp_link1, rtsp_link2, right_p, left_p)
