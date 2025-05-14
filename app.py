import streamlit as st

# Set page config untuk tema terang - HARUS MENJADI PERINTAH STREAMLIT PERTAMA
st.set_page_config(
    page_title="Form Kritik dan Saran",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from datetime import datetime, date, time
import repository as repo
import utils as utils
import predict_text as predict
import plotly.express as px
import pandas as pd
import hashlib

# Fungsi untuk mengecek password
def check_password(username, password):
    # Daftar username dan password yang valid (dalam praktik nyata, ini sebaiknya disimpan di database)
    # Password disimpan dalam bentuk hash untuk keamanan
    valid_credentials = {
        "admin": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
        "petugas": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"  # 1234
    }
    
    # Hash password yang diinput
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Cek apakah username ada dan password sesuai
    return username in valid_credentials and valid_credentials[username] == hashed_password

# Inisialisasi session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# CSS untuk tema terang
st.markdown("""
<style>
    .stApp {
        background-color: white;
        color: #333333;
    }
    .stTextInput > div > div > input, .stDateInput > div > div > input {
        background-color: #f0f0f0;
        color: #333333;
    }
    .stChatInput > div > div > input {
        background-color: #f0f0f0;
        color: #333333;
    }
    .stDataFrame {
        background-color: white;
    }
    .stMarkdown {
        color: #333333;
    }
    /* Mengurangi margin dan padding untuk memadatkan layout */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    p {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Konfigurasi sidebar untuk login
with st.sidebar:
    st.title("Kelurahan Kalitirto")
    
    # Login form
    if not st.session_state.authenticated:
        st.subheader("Login Petugas")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Login berhasil! Selamat datang, {username}")
                    st.rerun()
                else:
                    st.error("Username atau password salah")
    else:
        st.success(f"Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

# Tampilan untuk pengguna umum (tidak login)
if not st.session_state.authenticated:
    # Container dengan padding minimal
    with st.container():
        st.title("Form Kritik dan Saran")
        
        # Mengurangi spasi dengan menghilangkan container tambahan
        st.write("Silakan isi form di bawah ini untuk memberikan kritik dan saran Anda. " \
        "Kami sangat menghargai masukan Anda untuk meningkatkan pelayanan kami. Terima kasih atas partisipasi Anda!")
        
        # Input chat langsung di bawah teks, tanpa spasi tambahan
        user_input = st.chat_input("Say something")
        if user_input:
            st.toast("Terima kasih atas kritik dan saran Anda!")
            prediction = predict.predict(user_input).lower()
            data = {
                "feedback": user_input,
                "prediction": prediction,
            }
            repo.insert_data(data)

# Tampilan untuk petugas (sudah login)
else:
    st.title("Dashboard Kritik dan Saran")
    
    with st.expander("Form Kritik dan Saran", expanded=False):
        st.write("Silakan isi form di bawah ini untuk memberikan kritik dan saran Anda. " \
        "Kami sangat menghargai masukan Anda untuk meningkatkan pelayanan kami. Terima kasih atas partisipasi Anda!")
        
        user_input = st.chat_input("Say something")
        if user_input:
            st.toast("Terima kasih atas kritik dan saran Anda!")
            prediction = predict.predict(user_input).lower()
            data = {
                "feedback": user_input,
                "prediction": prediction,
            }
            repo.insert_data(data)
    
    st.divider()
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("Statistik Sentimen")
    with col2:
        st.subheader("Filter Data")
        start_date_input = st.date_input("Tanggal Awal", value=date.today(), format="DD-MM-YYYY")
        end_date_input = st.date_input("Tanggal Akhir", value=date.today(), format="DD-MM-YYYY")
        
        # Convert to datetime with time
        start_date = datetime.combine(start_date_input, time.min).isoformat()
        end_date = datetime.combine(end_date_input, time.max).isoformat()
        
        # Add validation for date range
        if start_date_input > end_date_input:
            st.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir")
            start_date = datetime.combine(end_date_input, time.min).isoformat()
            end_date = datetime.combine(end_date_input, time.max).isoformat()
    
    # Dapatkan semua data feedback terlebih dahulu
    feedback_history = repo.get_feedback_history(start_date, end_date)
    
    # Hitung jumlah untuk setiap kategori sentimen dari data yang ada
    if feedback_history:
        # Konversi ke DataFrame untuk memudahkan penghitungan
        df = pd.DataFrame(feedback_history)
        
        # Hitung jumlah untuk setiap kategori
        positive = len(df[df['prediction'] == 'positif'])
        neutral = len(df[df['prediction'] == 'netral'])
        negative = len(df[df['prediction'] == 'negatif'])
    else:
        positive = 0
        neutral = 0
        negative = 0
    
    # Tampilkan metrik sentimen
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Positif", value=positive, delta=None, help="Positive feedback")
        st.markdown(f'<div style="background-color: #1B5E20; color: white; border-radius: 10px; padding: 5px; text-align: center; font-size: 20px;">Positif</div>', unsafe_allow_html=True)
    with col2:  
        st.metric(label="Netral", value=neutral, delta=None, help="Netral feedback")
        st.markdown(f'<div style="background-color: #F57F17; color: white; border-radius: 10px; padding: 5px; text-align: center; font-size: 20px;">Netral</div>', unsafe_allow_html=True)
    with col3:
        st.metric(label="Negatif", value=negative, delta=None, help="Negative feedback")
        st.markdown(f'<div style="background-color: #B71C1C; color: white; border-radius: 10px; padding: 5px; text-align: center; font-size: 20px;">Negatif</div>', unsafe_allow_html=True)
    
    # Tambahkan diagram pie
    st.subheader("Diagram Distribusi Sentimen")
    if positive + neutral + negative > 0:
        # Buat dataframe untuk diagram pie
        pie_data = pd.DataFrame({
            'Sentimen': ['Positif', 'Netral', 'Negatif'],
            'Jumlah': [positive, neutral, negative]
        })
        
        # Buat diagram pie dengan plotly - warna lebih gelap dan teks putih
        fig = px.pie(
            pie_data, 
            values='Jumlah', 
            names='Sentimen',
            color='Sentimen',
            color_discrete_map={
                'Positif': '#1B5E20',  # Hijau gelap
                'Netral': '#F57F17',   # Kuning gelap
                'Negatif': '#B71C1C'   # Merah gelap
            },
            title=f'Distribusi Sentimen ({start_date_input.strftime("%d-%m-%Y")} s/d {end_date_input.strftime("%d-%m-%Y")})'
        )
        
        # Konfigurasi teks di dalam pie - ukuran lebih besar, warna putih, dan tidak miring
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(
                size=16,  # Ukuran font lebih besar
                color='white',  # Warna teks putih
                family="Arial, sans-serif"  # Font normal (tidak miring)
            ),
            insidetextorientation='horizontal'  # Orientasi teks horizontal (tidak miring)
        )
        
        # Mengatur warna background diagram menjadi transparan
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#333333',
            legend=dict(
                font=dict(
                    size=14  # Ukuran font legend lebih besar
                )
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Tidak ada data untuk rentang tanggal {start_date_input.strftime('%d-%m-%Y')} sampai {end_date_input.strftime('%d-%m-%Y')}.")
    
    st.container(height=30, border=False)
    
    # Tampilkan tabel feedback
    st.subheader("Riwayat Feedback")
    if feedback_history:
        data = utils.process_feedback_history(feedback_history)
        st.dataframe(data, use_container_width=True, hide_index=True, height=400)
    else:
        st.warning(f"Tidak ada data untuk rentang tanggal {start_date_input.strftime('%d-%m-%Y')} sampai {end_date_input.strftime('%d-%m-%Y')}.")
