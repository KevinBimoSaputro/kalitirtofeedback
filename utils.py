import pandas as pd
import streamlit as st
import pytz
from datetime import datetime

def set_markdown():
    return """
    <style>
        .stMetricValue-positif {
            background-color: green;
            color: white;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            font-size: 20px;
        }
        .stMetricValue-netral {
            background-color: yellow;
            color: black;
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
    </style>
    """

def process_feedback_history(feedback_history):
    try:
        # Konversi ke DataFrame
        df = pd.DataFrame(feedback_history)
        
        # Tambahkan kolom nomor
        df.insert(0, 'no', range(1, len(df) + 1))
        
        # Konversi tanggal dengan penanganan error yang lebih baik
        try:
            # Coba konversi tanggal tanpa timezone
            df['date'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            # Jika gagal, gunakan format yang lebih sederhana
            try:
                df['date'] = [datetime.fromisoformat(d.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') for d in df['created_at']]
            except Exception as e2:
                # Fallback: gunakan created_at apa adanya
                df['date'] = df['created_at']
        
        # Hapus kolom created_at
        if 'created_at' in df.columns:
            df = df.drop('created_at', axis=1)
        
        return df
    except Exception as e:
        st.error(f"Error in process_feedback_history: {e}")
        # Fallback: kembalikan data asli
        return pd.DataFrame(feedback_history)

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')
