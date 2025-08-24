import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ahmad Strategys", layout="wide")
st.title("📈 Ahmad Strategys")
st.markdown("داشبورد بک‌تست استراتژی‌های معاملاتی")

# آپلود فایل داده‌ها
uploaded_file = st.file_uploader("📂 فایل CSV قیمت‌ها رو آپلود کن", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # سیگنال ساده: خرید وقتی قیمت بالا می‌ره
    df['Signal'] = df['Close'].diff().apply(lambda x: 1 if x > 0 else -1)
    df['Return'] = df['Signal'].shift(1) * df['Close'].pct_change()
    df['Equity'] = (1 + df['Return']).cumprod()

    # نمودار Equity
    st.subheader("📊 نمودار رشد سرمایه")
    st.line_chart(df['Equity'])

    # خلاصه معاملات
    st.subheader("📋 خلاصه معاملات")
    total_trades = df['Signal'].count()
    total_profit = df['Equity'].iloc[-1] - 1
    win_rate = (df['Return'] > 0).mean() * 100
    drawdown = (df['Equity'].cummax() - df['Equity']).max()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("تعداد معاملات", total_trades)
    col2.metric("بازده کل", f"{total_profit*100:.2f}%")
    col3.metric("نرخ برد", f"{win_rate:.2f}%")
    col4.metric("بیشترین افت سرمایه", f"{drawdown*100:.2f}%")

    # جدول معاملات
    st.subheader("📑 جزئیات معاملات")
    df_trades = df[['Signal', 'Close', 'Return']].dropna().copy()
    df_trades['Type'] = df_trades['Signal'].apply(lambda x: 'Long' if x == 1 else 'Short')
    df_trades['Profit'] = df_trades['Return'] * 100
    st.dataframe(df_trades[['Type', 'Close', 'Profit']].reset_index())

    # خروجی اکسل
    st.download_button("📥 دانلود نتایج", df_trades.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")