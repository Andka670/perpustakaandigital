import streamlit as st
from supabase import create_client
from datetime import datetime

# ----------------------------
# Supabase Config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# CSS dan Animasi
# ----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 79% !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding-top: 90px;
    padding-bottom: 50px;
}
div[data-testid="stButton"] > button {
    min-height: 50px;
    padding: 25px 25px;
    border-radius: 25px;
    font-size: 16px;
    font-weight: bold;
    background-color: #4CAF50;
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stButton"] > button:hover {background-color: #45a049; transform: scale(1.05);}
div[data-testid="stButton"] > button:active {transform: scale(0.95);}
.animated-title {
    font-size: 40px;
    font-weight: bold;
    color: black;
    text-align: center;
    display: inline-block;
    animation: moveTitle 3s infinite alternate ease-in-out;
}
@keyframes moveTitle {
    0% { transform: translateX(-20px); color: #333; }
    50% { transform: translateX(20px); color: #4CAF50; }
    100% { transform: translateX(-20px); color: #333; }
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Navigasi
# ----------------------------
menu_options = {
    "ℹ️ Info Akun": "pages/admin.py",
    "📚 Tambah/Ubah Buku": "pages/tambahbuku.py",
    "📋 Data Buku&User": "pages/daftarpeminjaman.py",
    "🖊️ Peminjaman Offline": "pages/peminjamanoffline.py",
    "🔄 Pengembalian": "pages/pengembalian.py",
    "⚙️ Settings": "pages/settings.py"
}
cols = st.columns(len(menu_options))
for i, (name, page_path) in enumerate(menu_options.items()):
    with cols[i]:
        if st.button(name, use_container_width=True):
            st.switch_page(page_path)

# ----------------------------
# Judul Halaman
# ----------------------------
st.markdown("<h1 class='animated-title'>📚 Tambah Buku</h1>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ----------------------------
# Form Tambah Buku
# ----------------------------
with st.form("form_tambah_buku"):
    judul = st.text_input("Judul Buku")
    penulis = st.text_input("Penulis")
    tahun = st.number_input("Tahun Terbit", min_value=1900, max_value=2100, step=1)
    stok = st.number_input("Stok Buku", min_value=1, step=1)
    genre_options = ["Fiksi", "Non-Fiksi", "Sains", "Teknologi", "Sejarah", "Biografi", "Fantasi", "Lainnya"]
    genre = st.selectbox("Genre", genre_options)
    deskripsi = st.text_area("Deskripsi")
    file_cover = st.file_uploader("Upload Cover (jpg/png)", type=["jpg", "png"])
    file_pdf = st.file_uploader("Upload PDF (buku)", type=["pdf"])
    submitted = st.form_submit_button("Tambah Buku")

if submitted:
    if not (judul and penulis and tahun and stok and genre):
        st.warning("⚠️ Mohon lengkapi semua kolom yang wajib.")
    else:
        try:
            supabase.table("buku").insert({
                "judul": judul,
                "penulis": penulis,
                "tahun": int(tahun),
                "stok": int(stok),
                "genre": genre,
                "deskripsi": deskripsi
            }).execute()
            st.success("✅ Buku baru berhasil ditambahkan!")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

# ----------------------------
# Form Update Stok
# ----------------------------
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("📦 Update Stok Buku")

try:
    buku_list = supabase.table("buku").select("id_buku, judul, stok").execute().data
    if buku_list:
        buku_dict = {f"{b['judul']} (stok: {b['stok']})": b for b in buku_list}
        selected_buku = st.selectbox("Pilih Buku", list(buku_dict.keys()))
        jumlah_tambah = st.number_input("Jumlah Tambahan Stok", min_value=1, step=1)
        if st.button("Update Stok"):
            buku = buku_dict[selected_buku]
            new_stok = buku["stok"] + int(jumlah_tambah)
            supabase.table("buku").update({"stok": new_stok}).eq("id_buku", buku["id_buku"]).execute()
            st.success(f"✅ Stok buku '{buku['judul']}' berhasil diperbarui menjadi {new_stok}")
    else:
        st.info("Belum ada data buku.")
except Exception as e:
    st.error(f"❌ Gagal mengambil data buku: {e}")
