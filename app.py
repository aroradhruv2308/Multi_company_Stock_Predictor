import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model
import pandas_datareader as pdr
# import keras
from sklearn.preprocessing import MinMaxScaler
key = "c678441c30275c3b3f5e1733353e459a5433234f"
# print(keras._version_)
scaler = MinMaxScaler(feature_range=(0, 1))
regressor = load_model('regressor.h5')


def collect_data(company):
    df = pdr.get_data_tiingo(company, api_key=key)
    df.to_csv(company + '.csv')
    df = pd.read_csv(company + '.csv')
    df1 = df.reset_index()['close']
    # df1 = df1.to_numpy()
    size = len(df1)
    df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))
    X_input = df1[size-60:].reshape(1, -1, 1)
    # print(X_input.shape)
    # print("After Scaling")
    print(X_input.shape)
    print(X_input[0, :5, 0])
    return X_input


def predict_stock(company, days):
    X_input = collect_data(company)
    y_pred = scaler.inverse_transform(regressor.predict(X_input))
    return y_pred


def main():
    st.title("Stock Predictor")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Stock Predictor App</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    company = st.text_input("Company", "Type Here")
    days = st.text_input("Days", "Type Here")
    result = "Try Again Later"
    if st.button("Predict"):
        result = predict_stock(company, days)
    st.success('The Output is {}'.format(result))


if _name_ == '_main_':
    main()
