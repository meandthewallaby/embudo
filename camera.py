import v4l2capture
import select
import cv2.cv as cv

CAM_WIDTH = 1280
CAM_HEIGHT = 960

class Camera:
    def __init__(self, device="/dev/video0"):
        self.device = device
        self.cam = v4l2capture.Video_device(device)
        self.cam.set_format(CAM_WIDTH, CAM_HEIGHT)
        self.cam.set_brightness(0)
        self.cam.set_exposure_auto(0) #Auto Mode
        self.cam.create_buffers(1)

    def start(self):
        self.cam.start()

    def capture_frame(self):
        try:
            img = None
            self.cam.queue_all_buffers()
            raw_image = None
            for i in range(5):
                try:
                    select.select((self.cam,),(),())
                    raw_image = self.cam.read()
                    break
                except IOError:
                    raw_image = None
                    continue
            if raw_image is not None:
                img = cv.CreateImageHeader((CAM_WIDTH, CAM_HEIGHT), cv.IPL_DEPTH_8U, 3)
                cv.SetData(img, raw_image)
                cv.CvtColor(img, img, cv.CV_RGB2BGR)
                return img                    
        except IOError:
            log.error("Could not take picture due to IOError")
            pass

    def capture_image(self, filename):
        try:
            img = None
            self.cam.start()
            self.cam.queue_all_buffers()
            raw_image = None
            for i in range(5):
                try:
                    select.select((self.cam,),(),())
                    raw_image = self.cam.read()
                    break
                except IOError:
                    raw_image = None
                    continue
            if raw_image is not None:
                img = cv.CreateImageHeader((CAM_WIDTH, CAM_HEIGHT), cv.IPL_DEPTH_8U, 3)
                cv.SetData(img, raw_image)
                cv.CvtColor(img, img, cv.CV_RGB2BGR)
                cv.SaveImage(filename, img)
                return True                    
        except IOError:
            log.error("Could not take picture due to IOError")
            pass
        self.cam.stop()
        return False

    def set_exposure(self,exposure):
        self.cam.set_exposure_absolute(exposure)

    def get_exposure(self):
        self.cam.get_exposure_absolute()

    def reopen(self):
        self.__init__(self.device)

    def close(self):
        self.cam.stop()
        self.cam.close()
