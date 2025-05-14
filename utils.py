import pandas as pd
import streamlit as st

def process_feedback_history(data):
    df = pd.DataFrame(data)
    
    # Pendekatan sederhana tanpa konversi timezone
    if 'created_at' in df.columns:
        df['date'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df.drop(columns=['created_at'], inplace=True)
    
    df.insert(0, 'no', range(1, len(df) + 1))
    return df

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def set_markdown():
    return st.markdown("""
    <style>
        .stMetricValue-positif {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-negatif {
            background-color: #F44336;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-netral {
            background-color: #FFC107;
            color: black;
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
