import streamlit as st
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
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")
st.markdown("""
<style>
/* Hilangkan sidebar */
section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# CSS styling
# ----------------------------
st.markdown("""
<style>
/* Background animasi utama */
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
/* Buku jatuh */
.book {
    position: absolute;
    width: 80px;
    height: 80px;
    background-image: url('https://img.pikbest.com/png-images/20250110/aged-torn-book-pages-_11365988.png!w700wp'); /* icon buku */
    background-size: cover;
    top: -50px;
    animation-name: fall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}
@keyframes fall {
    0% { transform: translateY(-300px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
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

/* Judul LOGIN */
.login-title {
    font-weight: bold;
    color: white;
    font-size: 55px;
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
    padding: 10px 299px;
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
/* Tombol login */
.stButton[data-st-key="login_btn"] > button {
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
    <div class="login-title" style="margin-top:10px;">LOGIN</div>
    <div class="animated-subtitle">✨ Selamat Datang di Perpustakaan Digital Payakarta ✨</div>
</div>
""", unsafe_allow_html=True)
# Tambahkan HTML untuk beberapa buku
st.markdown("""
<div class="book" style="left:10%; animation-duration:6s;"></div>
<div class="book" style="left:30%; animation-duration:8s;"></div>
<div class="book" style="left:50%; animation-duration:5s;"></div>
<div class="book" style="left:70%; animation-duration:7s;"></div>
<div class="book" style="left:90%; animation-duration:6.5s;"></div>
""", unsafe_allow_html=True)
# ----------------------------
# Input username & password
# ----------------------------
st.markdown('<div style="text-align:left;font-size:20px;color:white;font-weight:bold">👤 USERNAME:</div>', unsafe_allow_html=True)
username = st.text_input("", placeholder="Masukkan username")
st.markdown('<div style="text-align:left;font-size:20px;color:white;font-weight:bold">🔒 PASSWORD:</div>', unsafe_allow_html=True)
password = st.text_input("", placeholder="Masukkan password", type="password")

# ----------------------------
# Tombol Lupa Password
# ----------------------------
col1, col2, col3 = st.columns([18,5,1])
with col2:
    st.page_link("pages/ubahpw.py", label="Lupa Password?", use_container_width=True)

# ----------------------------
# Tombol login
# ----------------------------
if st.button("Login", key="login_btn"):
    if username and password:
        response = supabase.table("akun").select("*")\
            .eq("username", username).eq("password", password).execute()
        if response.data:
            user = response.data[0]
            # simpan semua info user ke session
            st.session_state['logged_in'] = True
            st.session_state['user'] = {
                "id_user": user.get("id_user"),
                "username": user["username"],
                "level": user.get("level", "member")
            }

            st.success(f"✅ Selamat datang, {user['username']}!")

            # redirect sesuai level
            if user.get('level') == 'admin':
                st.switch_page("pages/admin.py")
            else:
                st.switch_page("app.py")
        else:
            st.error("❌ Username atau password anda salah.")
    else:
        st.warning("⚠️ Harap isi username dan password anda.")

# ----------------------------
# Link ke halaman register
# ----------------------------
st.markdown(
    "<div style='text-align:center; font-size:15px; color:black; font-weight:bold'>Belum punya akun?</div>",
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([2.20,2,1])
with col2:
    st.page_link("pages/daftar.py", label="Klik disini")

# ----------------------------
# Footer
# ----------------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:white;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
