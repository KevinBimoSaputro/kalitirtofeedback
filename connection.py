import streamlit as st
import joblib
from supabase import create_client
import os

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
    def insert(self, data):
        class MockInsert:
            def execute(self):
                st.success(f"Mock insert: {data}")
                return None
        return MockInsert()
    
    def select(self, *args, count=None):
        class MockSelect:
            def eq(self, *args):
                return self
            def gte(self, *args):
                return self
            def lte(self, *args):
                return self
            def order(self, *args, desc=False):
                return self
            def limit(self, *args):
                return self
            def execute(self):
                # Return mock data
                mock_data = {
                    "count": 5,
                    "data": [
                        {"feedback": "Pelayanan sangat baik", "prediction": "positif", "created_at": "2025-05-14T10:00:00"},
                        {"feedback": "Antrian terlalu panjang", "prediction": "negatif", "created_at": "2025-05-14T11:00:00"},
                        {"feedback": "Cukup memuaskan", "prediction": "netral", "created_at": "2025-05-14T12:00:00"},
                        {"feedback": "Petugas ramah", "prediction": "positif", "created_at": "2025-05-14T13:00:00"},
                        {"feedback": "Ruang tunggu nyaman", "prediction": "positif", "created_at": "2025-05-14T14:00:00"}
                    ]
                }
                return type('obj', (object,), mock_data)
        return MockSelect()

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
