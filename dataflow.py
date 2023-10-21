import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromPubSub, WriteToText
import socket
from google.cloud import firestore
import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('juve-402715-dbcaa4d0233d.json')
firebase_admin.initialize_app(cred)

db = firestore.Client()

def add_user(first_name, last_name, email, username, password): #when you click create account, call this method
    user_ref = db.collection('users').document(username)
    user = user_ref.get()

    if user.exists:
        print(f"User {username} already exists!")

    user_ref.set({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'scores': []
    })

def add_score_to_user(username, score):
    user_ref = db.collection('users').document(username)
    user = user_ref.get()
    scores = user.to_dict().get('scores', [])
    scores.append(score)
    user_ref.update({'scores': scores})

def get_scores(username):
    user = db.collection('users').document(username).get()
    if user.exists:
        return user.to_dict().get('scores', [])
    else:
        return None
    
def run():
    pipeline_options = PipelineOptions()

    with beam.Pipeline(options=pipeline_options) as p:
        (p | 'ReadFromPubSub' >> ReadFromPubSub(topic='projects/juve-402715/topics/juve')
           | 'ProcessCoordinates' >> beam.ParDo(ProcessCoordinates())
           | 'LogResults' >> WriteToText('gs://juve_bucket/output_dir')
           | 'WriteToFirestore' >> beam.ParDo(WriteToFirestoreFn())
        )

class ProcessCoordinates(beam.DoFn):
    def __init__(self):
        self.score = 0

    def process(self, element):
        coords = json.loads(element.decode('utf-8'))

        if 'end_of_game' in coords and coords['end_of_game']:
            # Send the score to Firestore and reset the score
            db = firestore.Client()
            game_data = {
                "timestamp": firestore.SERVER_TIMESTAMP,
                "score": self.score
            }
            db.collection("scores").add(game_data)
            self.score = 0
        else:
            #... [other collision detection logic]


class WriteToFirestoreFn(beam.DoFn):
    def process(self, element):
        # Logic to write `element` (which is the count of collisions) to Firestore
        pass

if __name__ == "__main__":
    run()
