import streamlit as st
from supabase import create_client, Client
import random

# ----------------------------
# Supabase config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# ----------------------------
# Hapus sidebar & background default
# ----------------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none;}
main {background: transparent !important;}
.block-container {background: transparent !important; padding:0 !important; box-shadow: none !important;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Generate stars
# ----------------------------
def generate_stars_html(n=150):
    stars = ""
    for _ in range(n):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(1, 3)
        duration = random.uniform(2, 5)
        stars += f'<div class="star" style="top:{top}vh; left:{left}vw; width:{size}px; height:{size}px; animation-duration:{duration}s;"></div>'
    return stars

stars_html = generate_stars_html()

# ----------------------------
# CSS Aurora + Meteor + Stars + Card
# ----------------------------
st.markdown(f"""
<style>
html, body {{
    margin:0; padding:0; height:100%; width:100%; overflow:hidden;
}}
.stApp {{
    position: relative; height:100vh; width:100vw;
    background: linear-gradient(135deg, #667eea, #764ba2, #ff758c, #ff7eb3);
    background-size: 600% 600%;
    animation: gradientBG 10s ease infinite;
}}
@keyframes gradientBG {{
    0% {{ background-position:0% 50%; }}
    50% {{ background-position:100% 50%; }}
    100% {{ background-position:0% 50%; }}
}}

/* Stars */
.star {{
    position: absolute;
    background:white;
    border-radius:50%;
    opacity:0.8;
    animation: twinkle linear infinite alternate;
}}
@keyframes twinkle {{0% {{opacity:0.2;}} 100% {{opacity:1;}}}}

/* Meteors */
.meteor {{
    position:absolute;
    width:2px;
    height:80px;
    background: linear-gradient(45deg, white, rgba(255,255,255,0));
    transform: rotate(45deg);
    animation: fall linear infinite;
}}
@keyframes fall {{
    0% {{transform: translateX(0) translateY(0); opacity:0;}}
    20% {{opacity:1;}}
    100% {{transform: translateX(var(--x)) translateY(var(--y)); opacity:0;}}
}}

/* Card login */
.login-card {{
    position: absolute;
    top:50%; left:50%;
    transform: translate(-50%, -50%);
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 30px 50px;
    text-align: center;
    z-index: 10;
    box-shadow:0 8px 32px rgba(0,0,0,0.3);
    width:400px;
}}

/* Foto profil animasi */
@keyframes float {{
    0% {{ transform: translateY(20px); }}
    50% {{ transform: translateY(50px); }}
    100% {{ transform: translateY(20px); }}
}}
.animated-photo {{
    animation: float 3s ease-in-out infinite;
    border-radius:50%;
    border:6px solid white;
    width:150px;
    box-shadow:0 0 25px rgba(255,255,255,0.6);
}}

/* Judul LOGIN */
.login-title {{
    font-weight:bold;
    color:white;
    font-size:55px;
    border-bottom:4px solid white;
    padding-bottom:5px;
}}

/* Subtitle animasi */
.animated-subtitle {{
    font-size:18px;
    margin:8px 0 30px 0;
    font-style:italic;
    font-weight:bold;
    color:#f5f5f5;
    animation: colorchange 4s infinite;
}}
@keyframes colorchange {{
    0% {{ color:#FFD700; }}
    25% {{ color:#00FA9A; }}
    50% {{ color:#1E90FF; }}
    75% {{ color:#FF4500; }}
    100% {{ color:#FFD700; }}
}}

/* Input & tombol */
.stTextInput>div>div>input {{
    background: rgba(255,255,255,0.25); border:none; border-radius:10px; padding:12px; color:#222; font-weight:bold; margin-bottom:10px;
}}
.stButton>button {{
    padding:10px 0; border-radius:12px; background:linear-gradient(90deg,#6a11cb,#2575fc);
    color:white; font-weight:bold; font-size:20px; border:none; width:100%; height:50px;
}}
.stButton>button:hover {{
    background:linear-gradient(90deg,#2575fc,#6a11cb); transform:scale(1.05);
}}
</style>

<div id="stars-container">{stars_html}</div>
<div class="meteor" style="top:-50px; left:10vw; --x:80vw; --y:60vh; animation-duration:2.5s;"></div>
<div class="meteor" style="top:-100px; left:40vw; --x:70vw; --y:50vh; animation-duration:3s;"></div>
<div class="meteor" style="top:-150px; left:70vw; --x:90vw; --y:70vh; animation-duration:2s;"></div>
""", unsafe_allow_html=True)

# ----------------------------
# Card login
# ----------------------------
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown("""
<img class="animated-photo" src="https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png">
<div class="login-title">LOGIN</div>
<div class="animated-subtitle">✨ Selamat Datang di Perpustakaan Digital Payakarta ✨</div>
""", unsafe_allow_html=True)

username = st.text_input("👤 USERNAME:", placeholder="Masukkan username")
password = st.text_input("🔒 PASSWORD:", placeholder="Masukkan password", type="password")

if st.button("Login"):
    if username and password:
        response = supabase.table("akun").select("*").eq("username", username).eq("password", password).execute()
        if response.data:
            user = response.data[0]
            st.session_state['logged_in'] = True
            st.session_state['user'] = {"id_user": user.get("id_user"), "username": user["username"], "level": user.get("level","member")}
            st.success(f"✅ Selamat datang, {user['username']}!")
        else:
            st.error("❌ Username atau password salah.")
    else:
        st.warning("⚠️ Harap isi username dan password.")

st.markdown('</div>', unsafe_allow_html=True)
