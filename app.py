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
# Session State Defaults
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Tema otomatis berdasarkan waktu
if "tema" not in st.session_state:
    hour = datetime.now().hour
    st.session_state.tema = "Siang" if 6 <= hour < 18 else "Malam"

if "page" not in st.session_state:
    st.session_state.page = "daftarbuku"

# =====================================================
# Cek Login
# =====================================================
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")

user = st.session_state["user"]

# =====================================================
# Fungsi Load Tema Global
# =====================================================
def load_theme_css():
    if st.session_state.tema == "Siang":
        css = """
        <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {background: linear-gradient(to bottom, #87ceeb, #ffffff); color: brown !important;}
        .sun {position:absolute; top:50px; left:70%; width:120px; height:120px;
            background: radial-gradient(circle, #FFD700 60%, #FFA500 100%);
            border-radius:50%; box-shadow:0 0 80px 20px rgba(255,223,0,0.7);
            animation: shine 6s ease-in-out infinite alternate;}
        @keyframes shine {0% {transform: scale(1); opacity:0.9;} 100% {transform: scale(1.1); opacity:1;}}
        .cloud {position:absolute; background: radial-gradient(circle at 30% 30%, #fff 70%, #f0f0f0 100%);
            border-radius:50%; opacity:0.9; animation: moveClouds 60s linear infinite;}
        .cloud::before, .cloud::after {content:""; position:absolute; background:inherit; border-radius:50%;}
        .cloud::before {width:80px; height:80px; top:-20px; left:-40px;}
        .cloud::after {width:60px; height:60px; top:-10px; right:-30px;}
        .cloud.large {width:200px; height:100px;}
        .cloud.medium {width:150px; height:75px;}
        .cloud.small {width:100px; height:50px;}
        @keyframes moveClouds {0% {left:-300px;} 100% {left:110%;}}
        </style>
        <div class="sun"></div>
        <div class="cloud large" style="top:120px; left:10%;"></div>
        <div class="cloud medium" style="top:200px; left:40%;"></div>
        <div class="cloud small" style="top:300px; left:70%;"></div>
        """
    else:
        css = """
        <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {background:linear-gradient(to bottom,#0d1b2a,#000000); color:white !important;}
        .moon {position:absolute; top:60px; left:70%; width:100px; height:100px;
            background: radial-gradient(circle,#fdfd96 60%,#f4e04d 100%); border-radius:50%;
            box-shadow:0 0 60px 10px rgba(255,255,200,0.6);
            animation: glow 5s ease-in-out infinite alternate;}
        @keyframes glow {0% {opacity:0.8; transform:scale(1);} 100% {opacity:1; transform:scale(1.05);}}
        .star {position:absolute;width:3px;height:3px;background:white;border-radius:50%; animation:twinkle 2s infinite ease-in-out;}
        @keyframes twinkle {0%,100%{opacity:0.2;}50%{opacity:1;}}
        </style>
        <div class="moon"></div>
        <div class="star" style="top:20px; left:30%;"></div>
        <div class="star" style="top:100px; left:50%;"></div>
        <div class="star" style="top:200px; left:70%;"></div>
        <div class="star" style="top:150px; left:20%;"></div>
        <div class="star" style="top:300px; left:60%;"></div>
        """
    st.markdown(css, unsafe_allow_html=True)

load_theme_css()

# =====================================================
# Global CSS Animasi & Komponen
# =====================================================
st.markdown("""
<style>
.main-title {text-align:center;font-size:52px;font-weight:bold;color:brown;}
.book-card{display:flex;flex-direction:column;padding:12px;border-radius:14px;background:brown;margin-bottom:20px;color:white;}
.cover-box img{width:100%;height:100%;object-fit:cover;border-radius:12px;}
.read-btn{display:inline-block;width:100%;padding:12px;background:#2575fc;color:white;text-align:center;border-radius:12px;text-decoration:none;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Title
# =====================================================
st.markdown("<div class='main-title'>Perpustakaan Digital</div><br>", unsafe_allow_html=True)

# =====================================================
# Navigasi
# =====================================================
menu_options = {"📚 Daftar Buku":"daftarbuku", "📋 Peminjaman Saya":"peminjamansaya", "⚙️ Profil":"profil"}
cols_nav = st.columns(len(menu_options), gap="medium")
for i, (name, page_name) in enumerate(menu_options.items()):
    with cols_nav[i]:
        if st.button(name, key=f"nav_{page_name}"):
            st.session_state.page = page_name
st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================
# Halaman Daftar Buku
# =====================================================
if st.session_state.page == "daftarbuku":
    st.title("📖 Daftar Buku Tersedia")
    try:
        buku_data = supabase.table("buku").select("*").execute().data
    except:
        buku_data = []
    if buku_data:
        num_cols = 3
        rows = [buku_data[i:i+num_cols] for i in range(0,len(buku_data),num_cols)]
        for row in rows:
            cols = st.columns(num_cols)
            for i, buku in enumerate(row):
                with cols[i]:
                    st.markdown("<div class='book-card'>", unsafe_allow_html=True)
                    if buku.get("cover_url"):
                        try:
                            signed_cover = supabase.storage.from_("uploads").create_signed_url(buku["cover_url"],3600)["signedURL"]
                            st.markdown(f"<div class='cover-box'><img src='{signed_cover}'/></div>", unsafe_allow_html=True)
                        except: pass
                    st.markdown(f"<b>{buku.get('judul','-')}</b>", unsafe_allow_html=True)
                    st.markdown(f"✍️ {buku.get('penulis','-')} | 📅 {buku.get('tahun','-')} | 🏷️ {buku.get('genre','-')} | Stok: {buku.get('stok','-')}")
                    if buku.get("pdf_url"):
                        try:
                            signed_pdf = supabase.storage.from_("uploads").create_signed_url(buku["pdf_url"],3600)["signedURL"]
                            st.markdown(f"<a class='read-btn' href='{signed_pdf}' target='_blank'>📕 Baca Buku</a>", unsafe_allow_html=True)
                        except: pass
                    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# Halaman Peminjaman Saya
# =====================================================
elif st.session_state.page == "peminjamansaya":
    st.title("📋 Peminjaman Saya")
    try:
        pinjam_data = supabase.table("peminjaman").select("*, buku(*)").eq("id_user", user["id_user"]).execute().data
    except:
        pinjam_data = []
    if pinjam_data:
        df = pd.DataFrame([{"Judul":p["buku"]["judul"], "Tanggal Pinjam":p["tanggal_pinjam"], "Tanggal Kembali":p.get("tanggal_kembali","-"), "Status":p["status"]} for p in pinjam_data])
        st.dataframe(df)
    else:
        st.info("Belum ada peminjaman.")

# =====================================================
# Halaman Profil
# =====================================================
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")
    st.write(f"👤 Username: {user['username']}")
    st.write(f"🆔 ID User: {user['id_user']}")
    st.markdown("---")
    st.subheader("🎨 Tema Tampilan")
    tema = st.radio("Pilih Tema", ["Siang","Malam"], index=0 if st.session_state.tema=="Siang" else 1)
    if tema != st.session_state.tema:
        st.session_state.tema = tema
        load_theme_css()
    st.markdown("---")
    st.subheader("🔑 Ubah Password")
    with st.form("ubah_password_form"):
        old_pw = st.text_input("Password Lama", type="password")
        new_pw = st.text_input("Password Baru", type="password")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password")
        submit_pw = st.form_submit_button("💾 Simpan Password")
    if submit_pw:
        if not old_pw or not new_pw or not confirm_pw:
            st.error("Semua field wajib diisi!")
        elif new_pw != confirm_pw:
            st.error("Konfirmasi password tidak cocok!")
        else:
            try:
                db_user = supabase.table("akun").select("password").eq("id_user",user["id_user"]).single().execute()
                if not db_user.data or db_user.data["password"] != old_pw:
                    st.error("Password lama salah!")
                else:
                    supabase.table("akun").update({"password": new_pw}).eq("id_user", user["id_user"]).execute()
                    st.success("Password berhasil diperbarui!")
            except Exception as e:
                st.error(f"Gagal mengubah password: {e}")
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# =====================================================
# Footer
# =====================================================
st.markdown("<br><hr><center style='color:brown;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
