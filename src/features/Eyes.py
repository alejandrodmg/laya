from picamera import PiCamera
import time
import os
import glob

class Camera():
    
    def __init__(self, img='img', video='video'):
        self.img_file = img
        self.video_file = video
        self.img_path = '../img/'+img+'.jpg'
        self.video_path = '../video/'+video+'.h264'

    def clean_directory(self, directory):
        files = glob.glob(directory)
        for f in files:
            os.remove(f)

    def take_photo(self):
        self.clean_directory('../img/*')
        with PiCamera() as cam:
            cam.start_preview()
            time.sleep(0.5)
            cam.capture(self.img_path)
            cam.stop_preview()
            cam.close()

    def shoot_video(self, length=5):
        self.clean_directory('../video/*')
        with PiCamera() as cam:
            cam.start_preview()
            cam.start_recording(self.video_path)
            time.sleep(length)
            cam.stop_recording()
            cam.stop_preview()
            cam.close()
            os.system('MP4Box -add ../video/{fn}.h264 ../video/{fn}.mp4'.\
                    format(fn=self.video_file))
            os.remove('../video/{fn}.h264'.\
                    format(fn=self.video_file))
