import streamlit as st
from flask import Flask, render_template, request
import pickle
import pandas as pd
import sklearn

st.title("Getting started streamlit")
st.write("test main app")

app = Flask(__name__)

def index():
    return("Hello world")

