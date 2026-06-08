from flask import Flask , Response
import time
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

def generate_frames():
    global last_frame_time
    while True:
        try:
            time.sleep(1/STREAM_FRAME_RATE)
            frame = camera.capture()
            if frame is None:
                print("[CAMERASERVER] Stream - no frame, stopping")
                break
            last_frame_time = time.time() #update on each frame

            success , jpeg = cv2.imencode(".jpg" , frame)

            if not success:
                print("[CAMERASERVER] Stream - encode failed  stopping")
                break

            yield (b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' +
                jpeg.tobytes() + b'\r\n')
            
        except Exception as e:
            print(f"[CAMERASERVER] Stream failed : {e}")
            break

@app.route("/frame")
def frame():
    try:
        image = camera.capture()

        if image is None:
            return {"error":"capture failed"}, 503
        
        success , jpeg = cv2.imencode(".jpg" , image)

        if not success:
            return {"error" : "encode failed"}, 503
        

        return Response(
            jpeg.tobytes(), 
            mimetype = "image/jpeg"
            )
    
    except Exception as e:
        print(f"[CAMERASERVER] Frame request failed: {e}")
        return {"error": str(e)},500


@app.route('/stream')

def stream():
    try:
        return Response(
            generate_frames(),
            mimetype = "multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as e:
        print(f"[CAMERASERVER] Stream route failed : {e}")
        return {"error" : str(e)},500

@app.route('/status')

def status():
    return {
        "camera" : "ok" if camera.isAvailable else "unavailable",
        "last_frame" : last_frame_time,
        "stream_age_seconds":round(time.time() - last_frame_time , 1) if last_frame_time else None
    }, 200

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = SERVER_PORT, threaded= True) #0.0.0.0 means it'll listen to all interfaces ( ethernet / wifi )