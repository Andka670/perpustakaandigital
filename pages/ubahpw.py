import streamlit as st
import time
from supabase import create_client, Client

# ----------------------------
# Supabase config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Ubah Password", page_icon="🔑", layout="centered")

st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none; }
.stApp {background: linear-gradient(135deg, #667eea, #764ba2, #ff758c, #ff7eb3); background-size: 600% 600%; animation: gradientBG 5s ease infinite;}
@keyframes gradientBG {0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; }}

.block-container {background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(12px); border-radius: 18px; padding: 30px 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);}

@keyframes float {0% { transform: translateY(20px); } 50% { transform: translateY(30px); } 100% { transform: translateY(20px); }}
.animated-photo {animation: float 3s ease-in-out infinite; border-radius:50%; border:6px solid white; width:150px; box-shadow: 0 0 25px rgba(255,255,255,0.6);}

.login-title {font-weight: bold; color: white; font-size: 50px; text-align: center;}
.animated-subtitle {font-size: 18px; margin-top: 8px; margin-bottom: 25px; font-style: italic; font-weight: bold; color: #f5f5f5; animation: colorchange 4s infinite;}
@keyframes colorchange {0% { color: #FFD700; } 25% { color: #00FA9A; } 50% { color: #1E90FF; } 75% { color: #FF4500; } 100% { color: #FFD700; }}

.stTextInput>div>div>input {background: rgba(255, 255, 255, 0.25); border: none !important; border-radius: 10px; padding: 12px; color: #222; font-weight: bold; transition: 0.3s ease; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);}
.stTextInput>div>div>input:hover, .stTextInput>div>div>input:focus {box-shadow: 0 0 15px rgba(106, 17, 203, 0.8), 0 0 30px rgba(37, 117, 252, 0.7); transform: scale(1.03);}

.stButton>button {padding: 12px 0; border-radius: 12px; background: linear-gradient(90deg, #6a11cb, #2575fc); color: white; font-weight: bold; font-size: 20px; border: none; transition: all 0.3s ease; box-shadow: 0 4px 25px rgba(0,0,0,0.35); width: 100%;}
.stButton>button:hover {background: linear-gradient(90deg, #2575fc, #6a11cb); transform: scale(1.05); box-shadow: 0 0 20px rgba(37,117,252,0.9), 0 0 35px rgba(106,17,203,0.8);}
.stButton[data-st-key="ubah_btn"] > button {height: 70px !important;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header + Logo + Subtitle
# ----------------------------
st.markdown("""
<div style="display:flex; align-items:center; justify-content:center; flex-direction:column; gap:10px; margin-bottom:30px;">
    <img class="animated-photo" src="https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png">
    <div class="login-title">CHANGE PASSWORD</div>
    <div class="animated-subtitle">🔑 Masukkan username, ID user, dan password baru Anda</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Card ubah password
# ----------------------------
st.markdown('<div class="lupa-pass-card">', unsafe_allow_html=True)

username = st.text_input("Username", placeholder="Masukkan username")
id_user = st.text_input("ID User", placeholder="Masukkan ID user")
new_pass = st.text_input("Password Baru", type="password", placeholder="Masukkan password baru")
confirm_pass = st.text_input("Konfirmasi Password Baru", type="password", placeholder="Konfirmasi password baru")

# Proteksi username admin
if username.strip().lower() == "admin":
    st.warning("⚠️ Username 'admin' tidak boleh diubah passwordnya lewat halaman ini.")

if st.button("Ganti Password", key="ubah_btn"):
    if not username.strip() or not id_user.strip() or not new_pass.strip() or not confirm_pass.strip():
        st.warning("⚠️ Harap isi semua field.")
    elif new_pass != confirm_pass:
        st.error("❌ Password baru dan konfirmasi tidak cocok.")
    elif username.strip().lower() == "admin":
        st.error("❌ Username 'admin' tidak boleh diubah passwordnya lewat halaman ini.")
    else:
        # cek apakah username & id_user sesuai
        existing_user = supabase.table("akun").select("*").eq("username", username).eq("id_user", id_user).execute()
        if existing_user.data:
            # update password
            update_response = supabase.table("akun").update({"password": new_pass}).eq("username", username).eq("id_user", id_user).execute()
            if update_response.data:
                st.success("✅ Password berhasil diubah! Mengarahkan ke login...")
                time.sleep(2)
                st.switch_page("pages/login.py")
            else:
                st.error("❌ Gagal mengubah password. Silakan coba lagi.")
        else:
            st.error("❌ Username atau ID user tidak ditemukan.")

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:white;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
