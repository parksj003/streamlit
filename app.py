# import yfinance as yf
# import streamlit as st

# st.title(""" 간단한 주식 차즈 종가(closing price) 와 거래량 (volume) 보기 - 태슬라""")
# Stock_Symbol = 'TSLA'
# StockData = yf.Ticker(Stock_Symbol)
# StockChart = StockData.history(period = '1d', start='2019-7-2',end='2020-5-11')
# st.line_chart(StockChart.Close)
# st.line_chart(StockChart.Volume)

import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

iris = datasets.load_iris()

st.write(""" # 붓꽃 (Iris Flower) 예측 웹 앱""")
st.sidebar.header('입력값')

def user_input_features():
    sepal_length = st.sidebar.slider('꽃받침 (Sepal) 길이',4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('꽃받침 (Sepal) 넓이',2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('꽃잎 (Petal) length',1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('꽃잎 (Petal) width',0.1, 2.5, 0.2)
    
    data = {'sepal_length': sepal_length, 'sepal_width':sepal_width,'petal_length':petal_length,'petal_width':petal_width}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

st.subheader('사용자입력 파라미터')
st.write(df)

iris =  datasets.load_iris()
X = iris.data
Y = iris.target

clf = RandomForestClassifier()
clf.fit(X, Y)

prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

st.subheader('클래스 레이블 및 해당 색인 번호')
st.write(iris.target_names)

st.subheader('예측')
st.write(iris.target_names[prediction])
st.write(prediction)

st.subheader('예측 확률')
st.write(prediction_proba)
