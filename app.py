import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o")
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

# Tema otomatis berdasarkan jam dunia nyata
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
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background: linear-gradient(to bottom, #87ceeb, #ffffff);
            height: 100%;
            margin: 0;
            overflow: hidden;
            color: brown !important;
        }
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
        @keyframes glow {0% {opacity:0.8; transform:scale(1);} 100% {opacity:1; transform:scale(1.05);} }
        .star {position:absolute;width:3px;height:3px;background:white;border-radius:50%; animation:twinkle 2s infinite ease-in-out;}
        @keyframes twinkle {0%,100%{opacity:0.2;}50%{opacity:1;}}
        .profil-text,h1,h2,h3,h4,label,.book-title,.book-meta,.book-desc {color:white !important;}
        div[data-testid="stButton"]>button {background-color:#333;color:white;}
        .book-card {background:#1a1a1a; color:white;}
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
/* Animasi judul, tombol, card, tabel, dll (sama seperti kode awal) */
</style>
""", unsafe_allow_html=True)

# =====================================================
# Title
# =====================================================
st.markdown("<div class='main-title'>Perpustakaan Digital</div><br>", unsafe_allow_html=True)

# =====================================================
# Navigasi
# =====================================================
menu_options = {
    "📚 Daftar Buku": "daftarbuku",
    "📋 Peminjaman Saya": "peminjamansaya",
    "⚙️ Profil": "profil"
}
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
        buku_data = supabase.table("buku").select(
            "id_buku, judul, penulis, tahun, genre, stok, cover_url, pdf_url, deskripsi"
        ).execute().data
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")

    if buku_data:
        buku_data = [b for b in buku_data if b.get("cover_url") and b["cover_url"].strip()]
        if not buku_data:
            st.info("ℹ️ Tidak ada buku dengan cover yang tersedia.")
        else:
            st.markdown("### 🔍 Cari Buku")
            col1, col2 = st.columns(2)
            with col1:
                judul_options = ["Semua"] + sorted({b["judul"] for b in buku_data if b.get("judul")})
                pilih_judul = st.selectbox("Pilih Judul Buku", judul_options, key="filter_judul")
            with col2:
                genre_options = ["Semua"] + sorted({b.get("genre","-") for b in buku_data})
                pilih_genre = st.selectbox("Pilih Genre", genre_options, key="filter_genre")
            buku_data = [b for b in buku_data if (pilih_judul=="Semua" or b.get("judul")==pilih_judul) and (pilih_genre=="Semua" or b.get("genre")==pilih_genre)]

            st.markdown("<hr>", unsafe_allow_html=True)
            num_cols = 3
            rows = [buku_data[i:i+num_cols] for i in range(0,len(buku_data),num_cols)]
            for row in rows:
                cols = st.columns(num_cols, gap="medium")
                for i, buku in enumerate(row):
                    with cols[i]:
                        st.markdown("<div class='book-card'>", unsafe_allow_html=True)
                        try:
                            signed_cover = supabase.storage.from_("uploads").create_signed_url(buku["cover_url"],3600)["signedURL"]
                            st.markdown(f"<div class='cover-box'><img src='{signed_cover}'/></div>", unsafe_allow_html=True)
                        except: pass
                        st.markdown(f"<div class='book-title'>{buku['judul']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='book-meta'>✍️ {buku['penulis']} | 📅 {buku['tahun']} | 🏷️ {buku.get('genre','-')} | 📦 Stok: {buku.get('stok','-')}</div>", unsafe_allow_html=True)
                        if buku.get("deskripsi"):
                            deskripsi_pendek = buku["deskripsi"][:150]+("..." if len(buku["deskripsi"])>150 else "")
                            st.markdown(f"<div class='book-desc'>{deskripsi_pendek}</div>", unsafe_allow_html=True)
                            with st.expander("📖 Selengkapnya"):
                                st.write(buku["deskripsi"])
                        if buku.get("pdf_url") and buku["pdf_url"].strip():
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
        pinjam_data = supabase.table("peminjaman").select("*, buku(judul, penulis, tahun, genre)").eq("id_user", user["id_user"]).order("tanggal_pinjam", desc=True).execute().data
    except Exception as e:
        pinjam_data = []
        st.error(f"❌ Gagal mengambil data peminjaman: {e}")
    if not pinjam_data:
        st.info("ℹ️ Kamu belum pernah meminjam buku.")
    else:
        table_data = []
        for p in pinjam_data:
            buku = p.get("buku", {})
            table_data.append({
                "Judul Buku": buku.get("judul","(Tanpa Judul)"),
                "Penulis": buku.get("penulis","-"),
                "Tahun": buku.get("tahun","-"),
                "Genre": buku.get("genre","-"),
                "Tanggal Pinjam": p["tanggal_pinjam"],
                "Tanggal Kembali": p.get("tanggal_kembali","-"),
                "Status": p["status"],
                "Denda (Rp)": p.get("denda",0)
            })
        df = pd.DataFrame(table_data)
        def color_denda(row):
            if row["Denda (Rp)"]>0:
                if row["Status"].lower()=="dipinjam": return ["color:red" if col=="Denda (Rp)" else "" for col in df.columns]
                elif row["Status"].lower()=="sudah dikembalikan": return ["color:green" if col=="Denda (Rp)" else "" for col in df.columns]
            return [""]*len(df.columns)
        st.dataframe(df.style.apply(color_denda,axis=1), use_container_width=True)

# =====================================================
# Halaman Profil
# =====================================================
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")
    st.markdown(f"<p class='profil-text'>👤 Username: {user['username']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='profil-text'>🆔 ID User: {user['id_user']}</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🎨 Tema Tampilan")
    tema = st.radio("Pilih Tema", ["Siang","Malam"], index=0 if st.session_state.tema=="Siang" else 1)
    if tema != st.session_state.tema:
        st.session_state.tema = tema
        load_theme_css()
    st.markdown("---")
    st.subheader("🔑 Ubah Password")
    st.markdown("<div class='input-animate'>", unsafe_allow_html=True)
    with st.form("ubah_password_form"):
        old_pw = st.text_input("Password Lama", type="password")
        new_pw = st.text_input("Password Baru", type="password")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password")
        submit_pw = st.form_submit_button("💾 Simpan Password")
    st.markdown("</div>", unsafe_allow_html=True)
    if submit_pw:
        if not old_pw or not new_pw or not confirm_pw:
            st.error("⚠️ Semua field wajib diisi!")
        elif new_pw != confirm_pw:
            st.error("❌ Konfirmasi password tidak cocok!")
        else:
            try:
                db_user = supabase.table("akun").select("password").eq("id_user",user["id_user"]).single().execute()
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

# =====================================================
# Footer
# =====================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:brown;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
