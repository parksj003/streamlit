import yfinance as yf
import streamlit as st

st.title(""" 간단한 주식 차즈 종가(closing price) 와 거래량 (volume) 보기 - 태슬라""")
Stock_Symbol = 'TSLA'
StockData = yf.Ticker(Stock_Symbol)
StockChart = StockData.history(period = '1d', start='2019-7-2',end='2020-5-11')
st.line_chart(StockChart.Close)
st.line_chart(StockChart.Volume)
