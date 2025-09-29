import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# =====================================================
# Page Config
# =====================================================
st.set_page_config(page_title="Perpustakaan Digital", page_icon="📚", layout="wide")

# =====================================================
# CSS Style
# =====================================================
st.markdown("""
<style>
/* Animasi Title */
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
h1, h2, h3, h4 { color: brown !important; }
div[data-testid="stButton"] > button {
    width:100%; min-height:50px; padding:15px 0;
    border-radius:20px; font-size:16px; font-weight:bold;
    background-color:brown; color:white; border:none;
    margin-right:5px; transition:all 0.3s ease;
}
div[data-testid="stButton"] > button:hover {
    background-color:#45a049; transform:scale(1.05);
}
section[data-testid="stSidebar"] {display:none !important;}
.styled-table { border-collapse: collapse; width: 100%; }
.styled-table th {
    background-color: #f9f4f0;
    color: brown; padding: 8px;
}
.styled-table td {
    color: brown; padding: 8px;
    border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

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
    "➕ Tambah Buku": "tambahbuku",
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
        df = pd.DataFrame(buku_data)
        st.dataframe(df)

# =====================================================
# Halaman Peminjaman Saya
# =====================================================
elif st.session_state.page == "peminjamansaya":
    st.title("📋 Peminjaman Saya")
    try:
        pinjam_data = (
            supabase.table("peminjaman")
            .select("*, buku(judul, penulis, tahun, genre)")
            .eq("id_user", user["id_user"])
            .order("tanggal_pinjam", desc=True)
            .execute()
            .data
        )
    except Exception as e:
        pinjam_data = []
        st.error(f"❌ Gagal mengambil data peminjaman: {e}")
    if not pinjam_data:
        st.info("ℹ️ Kamu belum pernah meminjam buku.")
    else:
        df = pd.DataFrame([
            {
                "Judul Buku": p.get("buku", {}).get("judul", "-"),
                "Tanggal Pinjam": p["tanggal_pinjam"],
                "Tanggal Kembali": p.get("tanggal_kembali", "-"),
                "Status": p["status"],
                "Denda (Rp)": p.get("denda", 0),
            }
            for p in pinjam_data
        ])
        st.markdown(df.to_html(index=False, classes="styled-table"), unsafe_allow_html=True)

# =====================================================
# Halaman Tambah Buku (plus Update Stok)
# =====================================================
elif st.session_state.page == "tambahbuku":
    st.title("➕ Tambah Buku")

    # ---------- Form Tambah Buku Baru ----------
    with st.form("form_tambah_buku"):
        id_buku = st.text_input("ID Buku")
        judul = st.text_input("Judul Buku")
        penulis = st.text_input("Penulis")
        tahun = st.number_input("Tahun Terbit", min_value=0, step=1)
        genre = st.text_input("Genre")
        stok = st.number_input("Stok Awal", min_value=0, step=1)
        cover = st.file_uploader("Upload Cover Buku", type=["jpg", "jpeg", "png"])
        pdf = st.file_uploader("Upload File Buku (PDF)", type=["pdf"])
        submit_buku = st.form_submit_button("📥 Simpan Buku")

    if submit_buku:
        try:
            cover_url = cover.name if cover else None
            pdf_url = pdf.name if pdf else None
            if cover:
                supabase.storage.from_("uploads").upload(cover.name, cover.getvalue())
            if pdf:
                supabase.storage.from_("uploads").upload(pdf.name, pdf.getvalue())
            supabase.table("buku").insert({
                "id_buku": id_buku,
                "judul": judul,
                "penulis": penulis,
                "tahun": tahun,
                "genre": genre,
                "stok": stok,
                "cover_url": cover_url,
                "pdf_url": pdf_url
            }).execute()
            st.success(f"✅ Buku '{judul}' berhasil ditambahkan!")
        except Exception as e:
            st.error(f"❌ Gagal menambahkan buku: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---------- Form Update Stok Buku ----------
    st.subheader("📦 Update Stok Buku")
    try:
        buku_data = supabase.table("buku").select("id_buku, judul, stok").execute().data
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")
    if buku_data:
        pilihan = {f"{b['id_buku']} - {b['judul']}": b for b in buku_data}
        pilih_buku = st.selectbox("Pilih Buku", list(pilihan.keys()))
        buku_terpilih = pilihan[pilih_buku]
        st.info(f"📖 Stok saat ini: **{buku_terpilih['stok']}**")
        stok_baru = st.number_input("Masukkan stok baru", min_value=0, step=1, value=buku_terpilih['stok'])
        if st.button("💾 Update Stok"):
            try:
                supabase.table("buku").update({"stok": stok_baru}).eq("id_buku", buku_terpilih["id_buku"]).execute()
                st.success(f"✅ Stok buku '{buku_terpilih['judul']}' berhasil diperbarui menjadi {stok_baru}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Gagal update stok: {e}")
    else:
        st.warning("⚠️ Belum ada data buku.")

# =====================================================
# Halaman Profil
# =====================================================
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")
    st.markdown(f"👤 Username: {user['username']}")
    st.markdown(f"🆔 ID User: {user['id_user']}")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# =====================================================
# Footer
# =====================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:brown;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
