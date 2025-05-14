import pandas as pd
import streamlit as st
import pytz
import io

def process_feedback_history(data):
    df = pd.DataFrame(data)

    jakarta_tz = pytz.timezone('Asia/Jakarta')
    df['date'] = pd.to_datetime(df['created_at']).dt.tz_convert(jakarta_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    df.drop(columns=['created_at'], inplace=True)
    df.insert(0, 'no', range(1, len(df) + 1))
    return df

def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def set_markdown():
    return st.markdown("""
    <style>
        .stMetricValue-positif {
            background-color: green;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-negatif {
            background-color: red;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-netral {
            background-color: yellow;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricLabel {
            font-size: 16px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
