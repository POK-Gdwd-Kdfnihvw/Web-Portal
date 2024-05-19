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

@app.route('/signup', methods =['POST'])
def signup():
    data = dict(request.form)
    email = data['email']
    password = data['password']

    raw = {'email': email, 'password': password}

    response = firebase_app.post('/users', raw)
    print(response)

    return render_template('register.html')

@app.route('/signin', methods=['POST'])
def signin():
    data = dict(request.form)
    email = data['username']
    password = data['password']

    result = firebase_app.get('/users', None)
    print(result)

    user_found = False
    for key, value in result.items():
        if value['email'] == email:
            user_found = True
            if value['password'] == password:
                return render_template('db.html')
            else:
                error_message = "Wrong Password"
                return render_template('login.html', error=error_message)
    if not user_found:
        error_message = "Invalid User"
        return render_template('login.html', error=error_message)

    return render_template('login.html')

@app.route('/predict', methods =['POST'])
def predict():
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]
    data = [int(i) for i in request.form.values()]
    print(data)

    prediction = model.predict(array_features)
    output = prediction
    
    if output == 1:
        return render_template('db.html', result = 'Heart disease: Unlikely', data = data, output = output)
    else:
        return render_template('db.html', result = 'Heart disease: Likely', data = data, output = output)

if __name__ == '__main__':
    app.run()
