import streamlit as st
import joblib
from supabase import create_client
import os
from datetime import datetime

@st.cache_resource 
def load_database():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        table = st.secrets["supabase"]["table"]
        client = create_client(url, key)
        return client.table(table)
    except (FileNotFoundError, KeyError) as e:
        st.warning(f"⚠️ Supabase credentials error: {e}. Running in development mode with mock data.")
        # Return a mock database object for development
        return MockDatabase()

@st.cache_resource 
def load_model():
    try:
        return joblib.load('model.pkl')
    except FileNotFoundError:
        st.warning("⚠️ Model file not found. Using mock model for sentiment prediction.")
        return MockModel()

@st.cache_resource 
def load_vectorizer():
    try:
        return joblib.load('vectorizer.pkl')
    except FileNotFoundError:
        st.warning("⚠️ Vectorizer file not found. Using mock vectorizer.")
        return MockVectorizer()

# Mock classes for development without actual database/model
class MockDatabase:
    def __init__(self):
        # Data dengan format tanggal yang konsisten
        self.mock_data = [
            {"feedback": "Pelayanan sangat baik", "prediction": "positif", "created_at": "2025-05-14T10:00:00"},
            {"feedback": "Antrian terlalu panjang", "prediction": "negatif", "created_at": "2025-05-14T11:00:00"},
            {"feedback": "Cukup memuaskan", "prediction": "netral", "created_at": "2025-05-14T12:00:00"},
            {"feedback": "Petugas ramah", "prediction": "positif", "created_at": "2025-05-14T13:00:00"},
            {"feedback": "Ruang tunggu nyaman", "prediction": "positif", "created_at": "2025-05-14T14:00:00"}
        ]
    
    def insert(self, data):
        class MockInsert:
            def execute(self):
                st.success(f"Mock insert: {data}")
                return None
        return MockInsert()
    
    def select(self, *args, count=None):
        class MockSelect:
            def __init__(self, parent):
                self.parent = parent
                self.filters = {}
                self.filter_prediction = None
                self.start_date = None
                self.end_date = None
                
            def eq(self, field, value):
                self.filters[field] = value
                if field == "prediction":
                    self.filter_prediction = value
                return self
                
            def gte(self, field, value):
                if field == "created_at":
                    self.start_date = value
                return self
                
            def lte(self, field, value):
                if field == "created_at":
                    self.end_date = value
                return self
                
            def order(self, *args, desc=False):
                return self
                
            def limit(self, *args):
                return self
                
            def execute(self):
                if count == "exact" and self.filter_prediction:
                    # Hitung jumlah data untuk prediksi tertentu
                    filtered_count = sum(1 for item in self.parent.mock_data if item["prediction"] == self.filter_prediction)
                    return type('obj', (object,), {"count": filtered_count})
                else:
                    # Filter data berdasarkan tanggal jika ada
                    filtered_data = self.parent.mock_data
                    
                    # Kembalikan data yang difilter
                    return type('obj', (object,), {"data": filtered_data})
                    
        return MockSelect(self)

class MockModel:
    def predict(self, text):
        # Simple mock prediction logic
        text_str = str(text[0]).lower()
        if "baik" in text_str or "bagus" in text_str or "puas" in text_str or "ramah" in text_str or "nyaman" in text_str:
            return ["positif"]
        elif "buruk" in text_str or "jelek" in text_str or "lama" in text_str or "panjang" in text_str or "rumit" in text_str:
            return ["negatif"]
        else:
            return ["netral"]

class MockVectorizer:
    def transform(self, text):
        # Just return the text as is for mock purposes
        return text
