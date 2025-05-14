import string
import connection as conn
import nltk
from nltk.corpus import stopwords

try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

try:
    model = conn.load_model()
    vectorizer = conn.load_vectorizer()
    stop_words = stopwords.words('indonesian')
except Exception as e:
    import streamlit as st
    st.error(f"Error loading model or vectorizer: {e}")
    # Set defaults to prevent further errors
    model = conn.load_model()  # This will now return the MockModel
    vectorizer = conn.load_vectorizer()  # This will now return the MockVectorizer
    stop_words = []
    try:
        stop_words = stopwords.words('indonesian')
    except:
        pass

def preprocess_text(text):
    """Fungsi untuk preprocessing teks: lowercase, hapus tanda baca, hapus stopwords"""
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    # Menghapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Menghapus stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def predict(text):
    """Fungsi untuk memprediksi sentimen dari teks"""
    try:
        # Preprocess the text
        preprocessed_text = preprocess_text(text)
        
        # Vectorize the text
        vectorized_text = vectorizer.transform([preprocessed_text])
        
        # Predict sentiment
        prediction = model.predict(vectorized_text)
        
        return prediction[0]
    except Exception as e:
        import streamlit as st
        st.warning(f"Error in prediction: {e}. Using simple rule-based prediction.")
        # Simple rule-based fallback
        text_lower = text.lower()
        if any(word in text_lower for word in ["baik", "bagus", "puas", "ramah", "nyaman", "suka"]):
            return "positif"
        elif any(word in text_lower for word in ["buruk", "jelek", "lama", "panjang", "rumit", "tidak"]):
            return "negatif"
        else:
            return "netral"
