import camera, accel
import threading
import cv2

if __name__ == "__main__":
    accelerometer = accel.Accelerometer(bus=1)
    cam0 = cv2.VideoCapture(0)
    cam1 = cv2.VideoCapture(1)
    cam2 = cv2.VideoCapture(2)

    cam0.set(3, 1280)
    cam0.set(4, 720)
    cam1.set(3, 1280)
    cam1.set(4, 720)
    cam2.set(3, 1280)
    cam2.set(4, 720)
    
    fourcc = cv2.cv.CV_FOURCC(*'MJPG')
    out0 = cv2.VideoWriter('/tmp/out0.avi', fourcc, 29.97, (1280, 720))
    out1 = cv2.VideoWriter('/tmp/out1.avi', fourcc, 29.97, (1280, 720))
    out2 = cv2.VideoWriter('/tmp/out2.avi', fourcc, 29.97, (1280, 720))

    frames = 0

    while(frames < 300):
        if cam0.isOpened() and cam1.isOpened() and cam2.isOpened():
            ret0, frame0 = cam0.read()
            ret1, frame1 = cam1.read()
            ret2, frame2 = cam2.read()
            if ret0 and ret1 and ret2:
                accelerometer.calc_pitch_and_roll()
                print "Frame {}: Pitch {}, Roll {}".format(frames, accelerometer.pitch, accelerometer.roll)
                out0.write(frame0)
                out1.write(frame1)
                out2.write(frame2)
                frames += 1
    cam0.release()
    cam1.release()
    cam2.release()
    out0.release()
    out1.release()
    out2.release()
    cv2.destroyAllWindows()

