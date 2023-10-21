import cv2
import mediapipe as mp
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import datetime, time
import os, sys
import numpy as np

global capture,rec_frame, switch, rec, out 
capture=0
switch=1
rec=0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'istilldontknowwhatthisis'
socketio = SocketIO(app)


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
pTime = 0


@socketio.on('connect')
def handle_connect():
    print('connected')

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

def process_frames():
    print('Processing frames')
    global out, capture,rec_frame
    pTime = time.time()

    while True:
        

        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        # print(results.pose_landmarks)

        

        landmarks_data = []

        if results.pose_landmarks:

            rightPalm_landmark = results.pose_landmark.landmark[19]
            rightPalm_x = rightPalm_landmark.rightPalm_x
            rightPalm_y = rightPalm_landmark.y


            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w,c = img.shape
                print(id, lm)
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
                landmarks_data.append({'id': id, 'x':cx, 'y': cy})


        cTime = time.time()
        fps = 1 / (cTime-pTime)
        pTime = cTime

        if (rec):
            rec_frame=imgRGB
            cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            #cv2.setWindowProperty("Image", cv2.WND_PROP_OPENGL, cv2.WINDOW_NORMAL)
            #cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

        socketio.emit('pose_data', {
            'rightPalm_x':rightPalm_x,
            'rightPalm_y': rightPalm_y,
            'other': landmarks_data
        })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    thread = Thread(target=process_frames)
    thread.daemon = True
    thread.start()
    socketio.run(app)