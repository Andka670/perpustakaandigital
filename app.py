import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0."
    "Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
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
st.markdown(
    """
<style>
/* Title Animasi */
@keyframes titleFadeIn {
    0% {opacity:0; transform:translateY(-20px) scale(0.9);}
    50% {opacity:0.5; transform:translateY(0) scale(1.05);}
    100% {opacity:1; transform:translateY(0) scale(1);}
}
@keyframes gradientText {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.main-title {
    text-align:center;
    font-size:52px;
    font-weight:bold;
    background: linear-gradient(270deg, #ff6a00, #ee0979, #2575fc, #6a11cb);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleFadeIn 1.2s ease-in-out, gradientText 6s ease infinite;
    text-shadow: 0px 0px 8px rgba(165,42,42,0.5);
}
h1, h2, h3, h4 {color: brown !important;}
.book-card {
    display:flex; flex-direction:column; justify-content:space-between;
    height:100%; padding:12px; border-radius:14px; background:brown;
    box-shadow:0 3px 8px rgba(0,0,0,0.1); animation:fadeIn 0.6s ease-in-out;
}
.cover-box {
    width:100%; aspect-ratio:3/4; overflow:hidden; border-radius:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.2); margin-bottom:10px;
}
.cover-box img {width:100%; height:100%; object-fit:cover;}
.book-title {
    font-weight:bold; font-size:16px; margin:8px 0; flex-grow:1;
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
    overflow:hidden; text-overflow:ellipsis; min-height:50px;
}
.book-meta {font-size:13px; color:black; margin-bottom:10px;}
.read-btn {
    display:inline-block; width:100%; min-height:45px; padding:12px 0;
    background:linear-gradient(270deg, #2575fc, #6a11cb); background-size:200% 200%;
    color:white !important; text-decoration:none; border-radius:12px;
    font-weight:bold; text-align:center; margin-top:auto; transition:all 0.4s ease-in-out;
    animation:gradientShift 4s ease infinite;
}
.read-btn:hover {
    background-position:right center; transform:scale(1.05) rotate(-1deg);
    box-shadow:0 6px 16px rgba(0,0,0,0.25);
}
</style>
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

if "page" not in st.session_state:
    st.session_state.page = "daftarbuku"

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
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")

    if buku_data:
        st.markdown("### 🔍 Cari Buku")
        col1, col2 = st.columns(2)

        with col1:
            judul_options = ["Semua"] + sorted({b["judul"] for b in buku_data if b.get("judul")})
            pilih_judul = st.selectbox("Pilih Judul Buku", judul_options, key="filter_judul")

        with col2:
            genre_options = ["Semua"] + sorted({b.get("genre", "-") for b in buku_data})
            pilih_genre = st.selectbox("Pilih Genre", genre_options, key="filter_genre")

        buku_data = [
            b for b in buku_data
            if (pilih_judul == "Semua" or b.get("judul") == pilih_judul)
            and (pilih_genre == "Semua" or b.get("genre") == pilih_genre)
        ]

        st.markdown("<hr>", unsafe_allow_html=True)

        num_cols = 3
        rows = [buku_data[i:i + num_cols] for i in range(0, len(buku_data), num_cols)]

        for row in rows:
            cols = st.columns(num_cols, gap="medium")
            for i, buku in enumerate(row):
                with cols[i]:
                    st.markdown("<div class='book-card'>", unsafe_allow_html=True)

                    # ✅ cover hanya muncul kalau ada
                    if buku.get("cover_url") and buku["cover_url"].strip():
                        try:
                            signed_cover = supabase.storage.from_("uploads").create_signed_url(
                                buku["cover_url"], 3600
                            )["signedURL"]
                            st.markdown(
                                f"<div class='cover-box'><img src='{signed_cover}'/></div>",
                                unsafe_allow_html=True
                            )
                        except:
                            pass

                    # ✅ tampilkan judul kalau ada
                    if buku.get("judul"):
                        st.markdown(
                            f"<div class='book-title'>{buku['judul']}</div>",
                            unsafe_allow_html=True
                        )

                    # ✅ meta hanya kalau ada data
                    meta_parts = []
                    if buku.get("penulis"): meta_parts.append(f"✍️ {buku['penulis']}")
                    if buku.get("tahun"): meta_parts.append(f"📅 {buku['tahun']}")
                    if buku.get("genre"): meta_parts.append(f"🏷️ {buku['genre']}")
                    if buku.get("stok") is not None: meta_parts.append(f"📦 Stok: {buku['stok']}")

                    if meta_parts:
                        st.markdown(
                            f"<div class='book-meta'>{' | '.join(meta_parts)}</div>",
                            unsafe_allow_html=True
                        )

                    # ✅ tombol baca hanya kalau ada pdf
                    if buku.get("pdf_url") and buku["pdf_url"].strip():
                        try:
                            signed_pdf = supabase.storage.from_("uploads").create_signed_url(
                                buku["pdf_url"], 3600
                            )["signedURL"]
                            st.markdown(
                                f"<a class='read-btn' href='{signed_pdf}' target='_blank'>📕 Baca Buku</a>",
                                unsafe_allow_html=True
                            )
                        except:
                            pass

                    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# (Halaman Peminjaman Saya dan Profil tetap sama seperti file aslimu)
# =====================================================
