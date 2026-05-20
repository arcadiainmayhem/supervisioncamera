from flask import Flask , Response
import cv2
from camera_constants import *
from camera_manager import CameraManager



app = Flask(__name__)
camera = CameraManager() #instance camera manager
camera.start() #start camera

@app.route("/health")

#GET HEALTH
def health():
    if camera.isAvailable:
        return {"status" : "ok"} , 200
    return {"status" : "Camera Unavailable"},503


@app.route("/frame")
def frame():
    try:
        image = camera.capture()

        if image is None:
            return {"error":"capture failed"}, 503
        
        success , jpeg = cv2.imencode(".jpg" , image)

        if not success:
            return {"error" : "encode failed"}, 503
        

        return Response(jpeg.tobytes(), mimetype = "image/jpeg")
    except Exception as e:
        print(f"[CAMERASERVER] Frame request failed: {e}")
        return {"error": str(e)},500

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = SERVER_PORT) #0.0.0.0 means it'll listen to all interfaces ( ethernet / wifi )