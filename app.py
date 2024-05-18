import numpy as np
import pickle
from flask import Flask, request, render_template
from firebase import firebase
import random

config = {
  "apiKey": "AIzaSyC_k0e0dZ9A4UZDAa09C1oS6yNqxCqEGnU",
  "authDomain": "pok-gdwd-kdfnihvw.firebaseapp.com",
  "projectId": "pok-gdwd-kdfnihvw",
  "storageBucket": "pok-gdwd-kdfnihvw.appspot.com",
  "messagingSenderId": "785250750960",
  "appId": "1:785250750960:web:d25863e1ba88c778934d35",
  "measurementId": "G-9H5GZK475C",
  "databaseURL": "https://pok-gdwd-kdfnihvw-default-rtdb.firebaseio.com/"
}

firebase_url = 'https://pok-gdwd-kdfnihvw-default-rtdb.firebaseio.com/'
firebase_app = firebase.FirebaseApplication(firebase_url, None)

result = firebase_app.get('/users', None)
print(result)

model = pickle.load(open('model_heart_disease.pkl', 'rb')) 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('db.html')

@app.route('/signup', methods =['POST'])
def signup():
    data = dict(request.form)
    x = random.randint(1,1000)
    email = data['email']
    password = data['password']

    raw = {'id': x, 'email': email, 'password': password}

    response = firebase_app.post('/users', raw)
    print(response)

    return render_template('register.html')

@app.route('/predict', methods =['POST'])
def predict():
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]

    prediction = model.predict(array_features)
    output = prediction
    
    if output == 1:
        return render_template('db.html', 
                               result = 'Heart disease: Unlikely')
    else:
        return render_template('db.html', 
                               result = 'Heart disease: Likely')

if __name__ == '__main__':
    app.run()
