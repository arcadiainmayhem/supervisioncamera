import cv2
import numpy as np
from camera_constants import *
from picamera2 import Picamera2

from libcamera import controls

class CameraManager:

    def __init__(self):
        self.cam = None # To hold camera object
        self.isAvailable = False #Flag for availability states




    def start(self):
        
        if DEV_MODE:
            print("[CAMERAMANAGER] In Dev Mode : Camera Not Connected")
            return
        #try except
        try:
            #try and clear camera object
            if self.cam is not None: # means theres camera object
                #clear camera and start fresh
                try:
                    self.stop()
                except:
                    pass
                self.cam = None
            #setup camera resolution 

            #new camera object
            self.cam = Picamera2()
            #new camera config
            config = self.cam.create_still_configuration(
                main={
                    "size" : RESOLUTION,
                    "format" : CAM_FORMAT,
                }
            )
            #set camera config
            self.cam.configure(config)
            #start camera
            self.cam.start()    
            #focus + delay
            time.sleep(1.0)                       # let the actuator come ready
            print(self.cam.camera_controls)
            self.cam.set_controls({"AfMode": controls.AfModeEnum.Manual,
                                   "LensPosition":LENS_POSITION})
            #flip flag
            self.isAvailable = True
            
            print("[CAMERAMANAGER] CAMERA STARTED" )

            import time
            time.sleep(2)                                    # let AF settle
            pos = self.cam.capture_metadata().get("LensPosition")
            print(f"[CAMERAMANAGER] AF settled at LensPosition: {pos}")

        except Exception as e:
            print(f"[CAMERAMANAGER] Camera failed to start : {e}")
            self.isAvailable = False

    def capture(self):
        #if no cam object, return None
        if not self.isAvailable:
            print("[CAMERAMANAGER] Capture Failed - camera no available")
            return None
        
        try:
            frame = self.cam.capture_array()
            return frame
        except Exception as e:
            print(f"[CAMERAMANAGER] Capture failed {e}")
            self.isAvailable = False
            return None

    def preview(self):
        if not SHOW_PREVIEW:
            return
        
        try :
            frame = self.capture()

            if frame is not None:
                cv2.imshow("Camera Preview" , frame)
                cv2.waitKey(1)
        except Exception as e:
            print(f"[CAMERAMANAGER] Preview Failed: {e}")

    def stop(self):
        try:
            if self.cam:
                self.cam.stop()
                self.cam.close()
                self.cam = None
                self.isAvailable = False
                print("[CAMERAMANAGER] Camera Stopped")
        except Exception as e:
            print(f"[CAMERAMANAGER] Stop Failed {e}")
            self.cam = None
            self.isAvailable = False