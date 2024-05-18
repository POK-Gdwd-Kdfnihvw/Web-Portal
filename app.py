import numpy as np
import pickle
from flask import Flask, request, render_template

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
