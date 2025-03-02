"""This module contains necessary function needed"""

# Import necessary modules
import streamlit as st
import joblib
import numpy as np


@st.cache_resource()
def load_model():
    # 加载模型
    return joblib.load('./model_classifier_randomForest.pkl')


# 在应用中调用缓存函数
model = load_model()


def predict(features):
    # Predict the value
    prediction = model.predict(features)

    return prediction
