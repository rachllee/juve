import cv2
import mediapipe as mp
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import datetime, time
import os, sys
import numpy as np
from google.cloud import pubsub_v1
import socket

# send data to dataflow.py
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('juve-402715', 'juve')

# Socket setup
host = 'localhost'  # Update to your server's IP
port = 12345        # Update to your desired port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'istilldontknowwhatthisis'
socketio = SocketIO(app)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

@socketio.on('connect')
def handle_connect():
    print('connected')

@app.route('/')
def index():
    return render_template('index.html')

def process_frames():
    while True:
        coordinates = []

        for landmark in landmarks_data:
            coordinates.append({'x':landmark['x'], 'y': landmark['y']})

        success, frame = cap.read()
       
        # Convert frame to RGB format (MediaPipe requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect pose landmarks
        results = pose.process(rgb_frame)

        # Draw pose landmarks on the frame
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            right_hand_landmark = results.pose_landmarks.landmark[15]
            rHand_x = int(right_hand_landmark.x * frame.shape[1])
            rHand_y = int(right_hand_landmark.y * frame.shape[0])

            cv2.circle(frame, (rHand_x, rHand_y), 20, (0,255,0), -1)
            

        # Convert the frame to JPEG format to send over the socket
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        socketio.emit('video_frame', frame_bytes) ##goes to index.html
        socketio.emit('coordinates', {'coordinates': coordinates}) ##goes to dataflow.py
        

        # Forward received data to Pub/Sub
        if coordinates:
            publisher.publish(topic_path, data=coordinates)


if __name__ == '__main__':
    thread = Thread(target=process_frames)
    thread.daemon = True
    thread.start()
    socketio.run(app)
