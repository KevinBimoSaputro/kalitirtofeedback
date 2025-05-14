import pandas as pd
import streamlit as st
import pytz
import io

def process_feedback_history(data):
    df = pd.DataFrame(data)
    
    # Pastikan kolom created_at ada
    if 'created_at' not in df.columns:
        st.error("Kolom 'created_at' tidak ditemukan dalam data")
        return df
    
    try:
        # Coba konversi tanggal tanpa timezone
        df['date'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        st.warning(f"Error saat konversi tanggal: {e}")
        # Fallback: gunakan created_at apa adanya
        df['date'] = df['created_at']
    
    # Hapus kolom created_at jika ada
    if 'created_at' in df.columns:
        df.drop(columns=['created_at'], inplace=True)
    
    # Tambahkan kolom nomor
    df.insert(0, 'no', range(1, len(df) + 1))
    
    return df

def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
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
