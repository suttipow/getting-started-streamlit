import streamlit as st
from flask import Flask, render_template, request
import pickle
import pandas as pd
import sklearn

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

#st.title("Membership Prediction App")

#age = st.number_input("Enter your age:", min_value=0)
#gender = st.selectbox("Select your gender", ["Male", "Female"])
#htime = st.number_input("Enter your average weekly hangout time (hours):", min_value=0)

#if st.button("Predict Membership Eligibility"):
#  try:
#    new_data = {'age': [age], 'gender': [gender], 'hang_out': [htime]}
#    new_data = transform_data(new_data)
#    result = predict(new_data)
#    st.write(result)
#  except ValueError:
#    st.error("Please enter valid numbers for age and hangout time.")

# Title with colored background using markdown syntax
title = """
<h1 style='background-color: #F0F0F0; color: blue; text-align: center; padding: 10px; border-radius: 5px;'>Membership Prediction App</h1>
"""

st.markdown(title, unsafe_allow_html=False)  # Set unsafe_allow_html to False

age = st.number_input("Enter your age:", min_value=0)
gender = st.selectbox("Select your gender", ["Male", "Female"])
htime = st.number_input("Enter your average weekly hangout time (hours):", min_value=0)

if st.button("Predict Membership Eligibility"):
  try:
    new_data = {'age': [age], 'gender': [gender], 'hang_out': [htime]}
    new_data = transform_data(new_data)
    result = predict(new_data)
    st.write(result)
  except ValueError:
    st.error("Please enter valid numbers for age and hangout time.")

