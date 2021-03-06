import streamlit as st
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
from fastai.text.all import *

def initiate_model():

    root = "C:/Users/user/GitHub/Sentiment_Analysis_on_Financial_News_Headlines"

    with open(f"Data/dls/dls_clas", "rb") as f:
        dls_clas = pickle.load(f)

    inferer = f"Inferer"

    path = Path(root + f"Data/labelled")

    learn = text_classifier_learner(dls_clas, AWD_LSTM, drop_mult=0.5, metrics=accuracy).to_fp16()

    learn.load(inferer)

    return(learn)

if "model" not in st.session_state:

    st.session_state["model"] = initiate_model()

learn = st.session_state["model"]
metrics_df = pd.read_csv("Data/csv/metrics.csv")

st.title("Sentiment Analysis of Financial Headlines")

st.header("LSTM Model Metrics")

col1, col2 = st.columns([2,1])

st.markdown("""
<style>
.big-font {
    font-size:200px !important;
    }
</style>
""", unsafe_allow_html=True)

with col1:

    st.write(metrics_df)

st.header("Let's Predict!")

headline = st.text_input("Please, insert the headline you want to classify:", value="", placeholder="Headline")

if headline != "":

    pred = learn.predict(headline)

    if pred[0] == "positive":

        output = "POSITIVE"
        st.markdown(f'<p style="color:green;font-size:200px">{output}</p>', unsafe_allow_html=True)

    elif pred[0] == "negative":

        output = "NEGATIVE"
        st.markdown(f'<p style="color:red;font-size:200px">{output}</p>', unsafe_allow_html=True)







