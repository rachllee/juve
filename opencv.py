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
import json 
import threading

# send data to dataflow.py
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('juve-402715', 'juve')

'''
# Socket setup
host = 'localhost'  # Update to your server's IP
port = 5500        # Update to your desired port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = 'istilldontknowwhatthisis'
socketio = SocketIO(app)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 25)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

@socketio.on('connect')
def handle_connect():
    print('connected')

@app.route('/')
def index():
    return render_template('index.html')


def send_data_to_pubsub(coordinates_batch):
    coordinates_json = json.dumps(coordinates_batch)
    if coordinates_json:
        coordinates_data = coordinates_json.encode('utf-8')
        publisher.publish(topic_path, data=coordinates_data)


FRAME_DELAY = 0.05  # delay between frames, you can adjust
RESIZE_DIM = (640, 480)  # reduce frame dimensions, adjust as necessary
BATCH_SIZE = 10

def process_frames():
    coordinates_batch = []
    while True:
        coordinates = {}

        success, frame = cap.read()
        if not success:
            continue

        #frame = cv2.resize(frame, RESIZE_DIM)

        # Convert frame to RGB format (MediaPipe requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect pose landmarks
        results = pose.process(rgb_frame)

        coordinates_batch.append(coordinates)

        # Draw pose landmarks on the frame
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            right_hand_landmark = results.pose_landmarks.landmark[15]
            rHand_x = int(right_hand_landmark.x * frame.shape[1])
            rHand_y = int(right_hand_landmark.y * frame.shape[0])


            cv2.circle(frame, (rHand_x, rHand_y), 20, (0,255,0), -1)

            for landmark in results.pose_landmarks.landmark:
                landmark_x = int(landmark.x * frame.shape[1])
                landmark_y = int(landmark.y * frame.shape[0])
                coordinates.update({'x': landmark_x, 'y': landmark_y})
            

        # Convert the frame to JPEG format to send over the socket
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        socketio.emit('video_frame', frame_bytes) ##goes to index.html
        socketio.emit('coordinates', {'coordinates': coordinates}) ##goes to dataflow.py
        coordinates_json = json.dumps(coordinates)

        coordinates_batch.append(coordinates_json)

        if len(coordinates_batch) == BATCH_SIZE:
            threading.Thread(target=send_data_to_pubsub, args=(coordinates_batch,)).start()
            coordinates_batch = []

        '''
        # Forward received data to Pub/Sub
        if coordinates_json:
            coordinates_data = coordinates_json.encode('utf-8')
            publisher.publish(topic_path, data=coordinates_data)
        '''
        time.sleep(FRAME_DELAY)


if __name__ == '__main__':
    thread = Thread(target=process_frames)
    thread.daemon = True
    thread.start()
    socketio.run(app)
