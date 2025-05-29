# src/mi_proyecto/dashboard.py

import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("Dashboard Financiero: AAPL")

    df = pd.read_csv("static/data/historical.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # KPIs
    df["Retorno Diario"] = df["Close"].pct_change()
    df["Media Móvil 20"] = df["Close"].rolling(window=20).mean()
    df["Volatilidad 20"] = df["Close"].rolling(window=20).std()
    df["Retorno Acumulado"] = (1 + df["Retorno Diario"]).cumprod()
    df["Desviación Estándar"] = df["Close"].rolling(window=20).std()

    st.line_chart(df[["Close", "Media Móvil 20"]])
    st.line_chart(df[["Retorno Acumulado"]])
    st.line_chart(df[["Volatilidad 20"]])
    st.line_chart(df[["Desviación Estándar"]])

    st.write("Últimos valores de KPIs")
    st.dataframe(df.tail())

if __name__ == "__main__":
    main()
