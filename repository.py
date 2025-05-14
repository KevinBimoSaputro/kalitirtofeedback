import connection as conn
import streamlit as st

db = conn.load_database()

def insert_data(data):
    db.insert(data).execute()

def get_count_by_prediction(prediction, start_date, end_date):
    try:
        data = db.select("*", count="exact") \
            .eq("prediction", prediction) \
            .gte("created_at", start_date) \
            .lte("created_at", end_date) \
            .limit(1) \
            .execute()
        return data.count
    except Exception as e:
        st.error(f"Error in get_count_by_prediction: {e}")
        return 0

def get_feedback_history(start_date, end_date):
    try:
        # Debug: Print parameter yang diterima
        st.write(f"Debug - get_feedback_history called with: start_date={start_date}, end_date={end_date}")
        
        data = db.select("feedback, prediction, created_at") \
            .gte("created_at", start_date) \
            .lte("created_at", end_date) \
            .order("created_at", desc=False) \
            .execute()
        
        # Debug: Print jumlah data yang ditemukan
        st.write(f"Debug - get_feedback_history found {len(data.data)} records")
        
        return data.data
    except Exception as e:
        st.error(f"Error in get_feedback_history: {e}")
        return []
