import streamlit as st
from flask import Flask, render_template, request
import pickle
import pandas as pd
import sklearn

st.title("Getting started streamlit")
st.write("test")

app = Flask(__name__)

def transform_age(ages):
    new_data = []
    for i in ages:
        if i >= 46 :
            new_data.append(3)
        elif i >= 26:
            new_data.append(2)
        else:
            new_data.append(1)
    return new_data


def transform_hangout(htimes):
    new_data = []
    for i in htimes:
        if i > 2 :
            new_data.append(1)
        else :
            new_data.append(0)
    return new_data

def transform_data(data):
    data['age'] = transform_age(data['age'])
    data['hang_out'] = transform_hangout(data['hang_out'])
    data['gender'] = [ 0 if i == 'Female'   else 1  for i in data['gender']  ]
    return data

def predict(new_data):
    result =''
    filename = 'svm_model.clf'
    clf = pickle.load(open(filename, 'rb'))
    new_df = pd.DataFrame(new_data)
    result = clf.predict(new_df)
    #print(result)
    return 'Not apply for membership' if result[0] == 0 else 'Apply to membership'

@app.route('/')
def index():
    if request.method == 'POST':
        age = int(request.form['age'])  
        gender = request.form['gender']    
        htime = int(request.form['htime'])  
        try:
            # Create new data dictionary
            new_data = {'age': [age],'gender': [gender], 'hang_out':[htime]}        
        except:
            return 'Error'
    else:
        return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)