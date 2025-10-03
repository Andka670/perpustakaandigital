import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Perpustakaan Digital",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# CSS Style
# =====================================================
def render_theme_css(theme: str):
    if theme == "Siang":
        st.markdown(
            """
<style>
/* Background Siang */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(to bottom, #87ceeb, #ffffff);
    height: 100%;
    margin: 0;
    overflow: hidden;
}

/* Matahari */
.sun {
    position: absolute;
    top: 50px;
    left: 70%;
    width: 120px;
    height: 120px;
    background: radial-gradient(circle, #FFD700 60%, #FFA500 100%);
    border-radius: 50%;
    box-shadow: 0 0 80px 20px rgba(255, 223, 0, 0.7);
    animation: shine 6s ease-in-out infinite alternate;
}
@keyframes shine {
    0% { transform: scale(1); opacity: 0.9; }
    100% { transform: scale(1.1); opacity: 1; }
}

/* Awan */
.cloud {
    position: absolute;
    background: radial-gradient(circle at 30% 30%, #fff 70%, #f0f0f0 100%);
    border-radius: 50%;
    opacity: 0.9;
    animation: moveClouds 60s linear infinite;
}
.cloud::before, .cloud::after {
    content: "";
    position: absolute;
    background: inherit;
    border-radius: 50%;
}
.cloud::before { width: 80px; height: 80px; top: -20px; left: -40px; }
.cloud::after  { width: 60px; height: 60px; top: -10px; right: -30px; }
.cloud.large  { width: 200px; height: 100px; }
.cloud.medium { width: 150px; height: 75px; }
.cloud.small  { width: 100px; height: 50px; }

@keyframes moveClouds {
    0% { left: -300px; }
    100% { left: 110%; }
}

/* Burung */
.bird {
    position: absolute;
    width: 40px;
    height: 40px;
    background: transparent;
    animation: fly 25s linear infinite;
}
.bird::before, .bird::after {
    content: "";
    position: absolute;
    width: 30px;
    height: 10px;
    border-top: 3px solid black;
    border-radius: 50%;
    top: 15px;
}
.bird::before { left: -25px; transform: rotate(-20deg); }
.bird::after  { right: -25px; transform: rotate(20deg); }

@keyframes fly {
    0% { left: -100px; }
    50% { left: 50%; }
    100% { left: 110%; }
}

/* Hujan */
.rain {
    position: absolute;
    width: 100%;
    height: 100%;
    pointer-events: none;
}
.raindrop {
    position: absolute;
    width: 2px;
    height: 15px;
    background: rgba(0,0,255,0.4);
    bottom: 100%;
    animation: fall linear infinite;
}
@keyframes fall {
    0%   { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(110vh); opacity: 0; }
}
</style>

<div class="sun"></div>
<!-- Awan -->
<div class="cloud large" style="top:80px; animation-delay:0s;"></div>
<div class="cloud medium" style="top:150px; animation-delay:20s;"></div>
<div class="cloud small" style="top:250px; animation-delay:40s;"></div>
<div class="cloud medium" style="top:320px; animation-delay:10s;"></div>
<div class="cloud small" style="top:400px; animation-delay:30s;"></div>
<!-- Burung -->
<div class="bird" style="top:100px; animation-delay:0s;"></div>
<div class="bird" style="top:200px; animation-delay:5s;"></div>
<div class="bird" style="top:300px; animation-delay:10s;"></div>
<div class="bird" style="top:150px; animation-delay:15s;"></div>
<!-- Hujan -->
<div class="rain">
  <div class="raindrop" style="left:10%; animation-duration:1s; animation-delay:0s;"></div>
  <div class="raindrop" style="left:30%; animation-duration:1.2s; animation-delay:0.2s;"></div>
  <div class="raindrop" style="left:50%; animation-duration:0.9s; animation-delay:0.4s;"></div>
  <div class="raindrop" style="left:70%; animation-duration:1.3s; animation-delay:0.1s;"></div>
  <div class="raindrop" style="left:90%; animation-duration:1s; animation-delay:0.3s;"></div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:  # Malam
        st.markdown(
            """
<style>
/* Background Malam */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(to bottom, #0d0d1a, #1a1a33);
    height: 100%;
    margin: 0;
    overflow: hidden;
}

/* Bulan */
.moon {
    position: absolute;
    top: 60px;
    left: 70%;
    width: 100px;
    height: 100px;
    background: radial-gradient(circle, #fff 60%, #ddd 100%);
    border-radius: 50%;
    box-shadow: 0 0 60px 15px rgba(255,255,200,0.5);
}

/* Bintang */
.star {
    position: absolute;
    width: 3px;
    height: 3px;
    background: white;
    border-radius: 50%;
    animation: twinkle 2s infinite ease-in-out alternate;
}
@keyframes twinkle {
    from { opacity: 0.2; }
    to { opacity: 1; }
}

/* Komet */
.comet {
    position: absolute;
    width: 3px;
    height: 3px;
    background: gold;
    border-radius: 50%;
    box-shadow: -100px -30px 15px 5px rgba(255,215,0,0.7);
    animation: cometFly 6s linear infinite;
}
@keyframes cometFly {
    0% { top: 50px; left: -100px; opacity: 0; }
    10% { opacity: 1; }
    50% { top: 200px; left: 50%; opacity: 1; }
    100% { top: 400px; left: 110%; opacity: 0; }
}
</style>

<div class="moon"></div>
<div class="star" style="top:80px; left:20%; animation-delay:0s;"></div>
<div class="star" style="top:150px; left:40%; animation-delay:1s;"></div>
<div class="star" style="top:200px; left:60%; animation-delay:2s;"></div>
<div class="star" style="top:300px; left:30%; animation-delay:3s;"></div>
<div class="star" style="top:350px; left:70%; animation-delay:4s;"></div>
<div class="comet"></div>
""",
            unsafe_allow_html=True,
        )

# =====================================================
# Cek Login
# =====================================================
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")

user = st.session_state["user"]

# =====================================================
# Navigasi
# =====================================================
menu_options = {
    "📚 Daftar Buku": "daftarbuku",
    "📋 Peminjaman Saya": "peminjamansaya",
    "⚙️ Profil": "profil"
}
if "page" not in st.session_state:
    st.session_state.page = "daftarbuku"

cols_nav = st.columns(len(menu_options), gap="medium")
for i, (name, page_name) in enumerate(menu_options.items()):
    with cols_nav[i]:
        if st.button(name, key=f"nav_{page_name}"):
            st.session_state.page = page_name

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================
# Halaman Profil
# =====================================================
if st.session_state.page == "profil":
    st.title("⚙️ Profil")

    st.markdown(f"👤 Username: {user['username']}")
    st.markdown(f"🆔 ID User: {user['id_user']}")

    if user.get("nama_lengkap"):
        st.markdown(f"📛 Nama Lengkap: {user['nama_lengkap']}")

    # Pilih tema
    st.subheader("🎨 Tema Profil")
    theme_choice = st.radio("Pilih Tema:", ["Siang", "Malam"], key="theme_profile")
    render_theme_css(theme_choice)

    st.markdown("---")
    st.subheader("🔑 Ubah Password")
    with st.form("ubah_password_form"):
        old_pw = st.text_input("Password Lama", type="password")
        new_pw = st.text_input("Password Baru", type="password")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password")
        submit_pw = st.form_submit_button("💾 Simpan Password")

    if submit_pw:
        if not old_pw or not new_pw or not confirm_pw:
            st.error("⚠️ Semua field wajib diisi!")
        elif new_pw != confirm_pw:
            st.error("❌ Konfirmasi password tidak cocok!")
        else:
            try:
                db_user = supabase.table("akun").select("password").eq("id_user", user["id_user"]).single().execute()
                if not db_user.data or db_user.data["password"] != old_pw:
                    st.error("❌ Password lama salah!")
                else:
                    supabase.table("akun").update({"password": new_pw}).eq("id_user", user["id_user"]).execute()
                    st.success("✅ Password berhasil diperbarui!")
            except Exception as e:
                st.error(f"❌ Gagal mengubah password: {e}")

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")
