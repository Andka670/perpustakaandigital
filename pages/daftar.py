import streamlit as st
from supabase import create_client, Client
import time

# ----------------------------
# Supabase config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Daftar", page_icon="📝", layout="centered")
st.markdown("""
<style>
/* Hilangkan sidebar */
section[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
# ----------------------------
# CSS styling (mirip login.py)
# ----------------------------
st.markdown("""
<style>
/* Background animasi */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2, #ff758c, #ff7eb3);
    background-size: 600% 600%;
    animation: gradientBG 5s ease infinite;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Card transparan */
.block-container {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 30px 50px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Foto profil animasi */
@keyframes float {
    0% { transform: translateY(20px); }
    50% { transform: translateY(50px); }
    100% { transform: translateY(20px); }
}
.animated-photo {
    animation: float 3s ease-in-out infinite;
    border-radius:50%;
    border:6px solid white;
    width:150px;
    box-shadow: 0 0 25px rgba(255,255,255,0.6);
}
/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6a11cb, #2575fc);
    color: white;
    box-shadow: 0 0 15px rgba(37,117,252,0.9);
}
section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: bold;
}
/* Judul DAFTAR */
.register-title {
    font-weight: bold;
    color: white;
    font-size: 50px;
    border-bottom: 4px solid white;
    padding-bottom: 5px;
    text-align: center;
}

/* Subtitle animasi */
.animated-subtitle {
    font-size: 18px;
    margin-top: 8px;
    margin-bottom: 30px;
    font-style: italic;
    font-weight: bold;
    color: #f5f5f5;
    animation: colorchange 4s infinite;
}
@keyframes colorchange {
    0% { color: #FFD700; }
    25% { color: #00FA9A; }
    50% { color: #1E90FF; }
    75% { color: #FF4500; }
    100% { color: #FFD700; }
}

/* Input */
.stTextInput>div>div>input {
    background: rgba(255, 255, 255, 0.25);
    border: none !important;
    border-radius: 10px;
    padding: 12px;
    color: #222;
    font-weight: bold;
    transition: 0.3s ease;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25); 
}
.stTextInput>div>div>input:hover,
.stTextInput>div>div>input:focus {
    box-shadow: 0 0 15px rgba(106, 17, 203, 0.8),
                0 0 30px rgba(37, 117, 252, 0.7);
    transform: scale(1.03);
}

/* Tombol gradient */
.stButton>button {
    padding: 10px 297px;
    border-radius: 12px;
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: white;
    font-weight: bold;
    font-size: 20px;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 25px rgba(0,0,0,0.35);
}
.stButton>button:hover {
    background: linear-gradient(90deg, #2575fc, #6a11cb);
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(37,117,252,0.9),
                0 0 35px rgba(106,17,203,0.8);
}
/* Tombol daftar */
.stButton[data-st-key="register_btn"] > button {
    width: 100% !important;
    height: 70px !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Judul + Foto + Subtitle
# ----------------------------
st.markdown("""
<div style="display:flex; align-items:center; justify-content:center; flex-direction:column; gap:10px;">
    <img class="animated-photo" 
         src="https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png"
         style="margin-bottom:30px;">
    <div class="register-title" style="margin-top:10px;">DAFTAR</div>
    <div class="animated-subtitle">📚 Buat akun baru untuk mengakses Perpustakaan Digital Payakarta 📚</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Input username & password
# ----------------------------
st.markdown('<div style="text-align:left;font-size:20px;color:white;font-weight:bold">👤 USERNAME:</div>', unsafe_allow_html=True)
username = st.text_input("", placeholder="Masukkan username")
st.markdown('<div style="text-align:left;font-size:20px;color:white;font-weight:bold">🔒 PASSWORD:</div>', unsafe_allow_html=True)
password = st.text_input("", placeholder="Masukkan password", type="password")

# ----------------------------
# Tombol daftar
# ----------------------------
if st.button("Daftar", key="register_btn"):
    if username.strip() == "" or password.strip() == "":
        st.warning("⚠️ Username dan password tidak boleh kosong.")
    else:
        existing_user = supabase.table("akun").select("*").eq("username", username).execute()
        if existing_user.data:
            st.error("❌ Username sudah digunakan, silakan pilih username lain.")
        else:
            response = supabase.table("akun").insert({"username": username, "password": password}).execute()
            if response.data:
                st.success("✅ Akun berhasil dibuat! Silakan login.")
                time.sleep(2)
                st.switch_page("pages/login.py")
            else:
                st.error("❌ Gagal membuat akun, coba lagi.")

# ----------------------------
# Link ke halaman login
# ----------------------------
st.markdown(
    "<div style='text-align:center; font-size:15px; color:black; font-weight:bold'>Sudah punya akun?</div>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([2.20,2,1])
with col2:
    st.page_link("pages/login.py", label="Klik disini")

# ----------------------------
# Footer
# ----------------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:white;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
