import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from threading import Thread
import datetime, time
import os, sys
import numpy as np
import atexit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'istilldontknowwhatthisis'
socketio = SocketIO(app)
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FPS, 20)


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

@socketio.on('connect')
def handle_connect():
    print('connected')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(process_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def process_frames():
    while True:
        success, frame = cap.read()
        if success:
       
            # Convert frame to RGB format (MediaPipe requires RGB input)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect pose landmarks
            results = pose.process(rgb_frame)

            # Draw pose landmarks on the frame
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            # Convert the frame to JPEG format to send over the socket
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            #socketio.emit('video_frame', frame_bytes)
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        #socketio.emit('video_frame', frame_bytes)
        

if __name__ == '__main__':
    thread = Thread(target=process_frames)
    thread.daemon = True
    thread.start()
    socketio.run(app)
