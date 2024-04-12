import streamlit as st
from flask import Flask, render_template, request
import pickle
import pandas as pd
import sklearn

st.title("Getting started streamlit")
st.write("test main app2")

app = Flask(__name__)

@app.route('/')
def index():
    return("Hello world")

