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
# CSS untuk background & card
# ----------------------------
def generate_stars_html(n=150):
    return "".join(
        f'<div class="star" style="top:{random.uniform(0,100)}vh; left:{random.uniform(0,100)}vw; width:{random.uniform(1,3)}px; height:{random.uniform(1,3)}px; animation-duration:{random.uniform(2,5)}s;"></div>'
        for _ in range(n)
    )

stars_html = generate_stars_html()

st.markdown(f"""
<style>
/* Hapus background default Streamlit */
main {{
    background: transparent !important;
}}

/* Background gradient animasi */
.stApp {{
    background: linear-gradient(135deg, #667eea, #764ba2, #ff758c, #ff7eb3);
    background-size: 600% 600%;
    animation: gradientBG 10s ease infinite;
    position: relative;
    overflow: hidden;
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
@keyframes twinkle {{
    0% {{opacity:0.2;}}
    100% {{opacity:1;}}
}}

/* Meteor */
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
    position: relative;
    z-index: 10;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 30px 50px;
    text-align: center;
    margin:auto;
    max-width: 400px;
    margin-top: 50px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}}

/* Foto profil animasi */
.animated-photo {{
    animation: float 3s ease-in-out infinite;
    border-radius:50%;
    border:6px solid white;
    width:150px;
    box-shadow:0 0 25px rgba(255,255,255,0.6);
}}
@keyframes float {{
    0% {{ transform: translateY(20px); }}
    50% {{ transform: translateY(50px); }}
    100% {{ transform: translateY(20px); }}
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
    0% {{ color:white; }}
    25% {{ color:yellow; }}
    50% {{ color:white; }}
    75% {{ color:yellow; }}
    100% {{ color:white; }}
}}

/* Input */
.stTextInput>div>div>input {{
    background: rgba(255,255,255,0.25);
    border: none !important;
    border-radius: 10px;
    padding: 12px;
    color: #222;
    font-weight: bold;
}}

/* Tombol gradient */
.stButton>button {{
    padding:10px 0;
    border-radius:12px;
    background: linear-gradient(90deg,#6a11cb,#2575fc);
    color:white;
    font-weight:bold;
    font-size:20px;
    border:none;
    width:100%;
    height:50px;
}}
</style>

<!-- Stars -->
<div id="stars-container">
    {stars_html}
</div>

<!-- Meteors -->
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

# Input username & password
username = st.text_input("👤 USERNAME:", placeholder="Masukkan username")
password = st.text_input("🔒 PASSWORD:", placeholder="Masukkan password", type="password")

# Tombol lupa password
col1, col2, col3 = st.columns([18,5,1])
with col2:
    st.page_link("pages/ubahpw.py", label="Lupa Password?", use_container_width=True)

# Tombol login
if st.button("Login", key="login_btn"):
    if username and password:
        response = supabase.table("akun").select("*")\
            .eq("username", username).eq("password", password).execute()
        if response.data:
            user = response.data[0]
            st.session_state['logged_in'] = True
            st.session_state['user'] = {
                "id_user": user.get("id_user"),
                "username": user["username"],
                "level": user.get("level", "member")
            }
            st.success(f"✅ Selamat datang, {user['username']}!")
            if user.get('level') == 'admin':
                st.switch_page("pages/admin.py")
            else:
                st.switch_page("app.py")
        else:
            st.error("❌ Username atau password anda salah.")
    else:
        st.warning("⚠️ Harap isi username dan password anda.")

# Link ke halaman register
st.markdown(
    "<div style='text-align:center; font-size:15px; color:black; font-weight:bold'>Belum punya akun?</div>",
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([2.20,2,1])
with col2:
    st.page_link("pages/daftar.py", label="Klik disini")

# Footer
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:white;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
