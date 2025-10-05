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
st.markdown(""" <style>
/* Hilangkan sidebar */
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}

/* Perlebar container utama */
.block-container {
    max-width: 79% !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding-top: 90px;
    padding-bottom: 50px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
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
/* Tombol navigasi */
div[data-testid="stButton"] > button {
    min-height: 75px;
    width: 100% !important;
    border-radius: 12px;
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
div[data-testid="stButton"] > button:hover {
    background-color: #45a049;
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}
div[data-testid="stButton"] > button:active {
    transform: scale(0.95);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Animasi teks judul */
.animated-title {
    font-size: 40px;
    font-weight: bold;
    color: black;
    text-align: center;
    display: inline-block;
    animation: moveTitle 3s infinite alternate ease-in-out;
}
@keyframes moveTitle {
    0%   { transform: translateX(-20px); color: #333; }
    50%  { transform: translateX(20px);  color: #4CAF50; }
    100% { transform: translateX(-20px); color: #333; }
}
/* Input & Selectbox */
div[data-baseweb="select"], div[data-baseweb="input"] {
    border-radius: 12px;
    border: 2px solid #4CAF50;
    padding: 5px;
}
</style> """, unsafe_allow_html=True)
st.markdown(
    "<div class='main-title'>Admin Perpustakaan</div><br>",
    unsafe_allow_html=True
)
# ----------------------------
# Navigasi horizontal
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
# Judul halaman
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
    genre_options = ["Fiksi","Non-Fiksi","Sains","Teknologi","Sejarah","Biografi","Fantasi","Lainnya"]
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
            cover_path = None
            pdf_path = None

            # Upload cover
            if file_cover is not None:
                file_bytes = file_cover.read()
                cover_path = f"covers/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_cover.name}"
                supabase.storage.from_("uploads").upload(
                    cover_path,
                    file_bytes,
                    {"content-type": file_cover.type}
                )

            # Upload PDF
            if file_pdf is not None:
                file_bytes = file_pdf.read()
                pdf_path = f"pdfs/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_pdf.name}"
                supabase.storage.from_("uploads").upload(
                    pdf_path,
                    file_bytes,
                    {"content-type": "application/pdf"}
                )

            # Simpan data buku
            supabase.table("buku").insert({
                "judul": judul,
                "penulis": penulis,
                "tahun": int(tahun),
                "stok": int(stok),
                "genre": genre,
                "deskripsi": deskripsi,
                "cover_url": cover_path,   # simpan path
                "pdf_url": pdf_path        # simpan path
            }).execute()
            st.success("✅ Buku baru berhasil ditambahkan!")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

# ----------------------------
# Form Update Stok Buku
# ----------------------------
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("📦 Update Stok Buku")

try:
    buku_list = supabase.table("buku").select("id_buku, judul, stok").execute().data
    if buku_list:
        buku_dict = {f"{b['judul']} (stok: {b['stok']})": b for b in buku_list}
        selected_buku = st.selectbox("Pilih Buku", list(buku_dict.keys()))

        # Pilih aksi: tambah atau kurang stok
        aksi = st.radio("Aksi Stok", ["Tambah", "Kurangi"])
        jumlah = st.number_input("Jumlah", min_value=1, step=1)

        if st.button("Update Stok"):
            buku = buku_dict[selected_buku]
            if aksi == "Tambah":
                new_stok = buku["stok"] + int(jumlah)
            else:  # Kurangi stok
                if jumlah > buku["stok"]:
                    st.warning(f"⚠️ Jumlah pengurangan melebihi stok saat ini ({buku['stok']})!")
                    new_stok = buku["stok"]
                else:
                    new_stok = buku["stok"] - int(jumlah)

            supabase.table("buku").update({"stok": new_stok}).eq("id_buku", buku["id_buku"]).execute()
            st.success(f"✅ Stok buku '{buku['judul']}' berhasil diperbarui menjadi {new_stok}")
    else:
        st.info("Belum ada data buku.")
except Exception as e:
    st.error(f"❌ Gagal mengambil data buku: {e}")

# ----------------------------
# Ubah Detail Buku
# ----------------------------
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("✏️ Ubah Detail Buku")
try:
    buku_list = supabase.table("buku").select("id_buku, judul, genre, tahun, stok, deskripsi, cover_url, pdf_url, penulis").execute().data
    if buku_list:
        buku_dict = {f"{b['judul']} (ID: {b['id_buku']})": b for b in buku_list}
        selected_buku = st.selectbox("Pilih Buku untuk Diubah", list(buku_dict.keys()), key="pilih_buku_ubah")
        if st.button("Pilih Buku"):
            st.session_state.edit = buku_dict[selected_buku]
    else:
        st.info("Belum ada data buku untuk diubah.")
except Exception as e:
    st.error(f"❌ Gagal memuat daftar buku: {e}")

if "edit" in st.session_state:
    book_edit = st.session_state.edit
    st.markdown("---")
    st.subheader(f"📖 Mengedit: **{book_edit.get('judul', 'Tanpa Judul')}** (ID: {book_edit.get('id_buku', '-')})")

    # Preview cover lama sebagai link teks
    if book_edit.get("cover_url"):
        try:
            cover_url = book_edit["cover_url"]
            st.markdown(f"[🖼️ Cover Saat Ini]({cover_url})", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ Tidak bisa menampilkan cover: {e}")

    # Preview PDF lama
    if book_edit.get("pdf_url"):
        try:
            pdf_url = book_edit["pdf_url"]
            st.markdown(f"[📄 PDF Saat Ini]({pdf_url})", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ Tidak bisa menampilkan PDF: {e}")

    # Input edit
    edit_judul = st.text_input("Judul Baru", value=book_edit.get("judul", ""), key="edit_judul")
    edit_penulis = st.text_input("Penulis Baru", value=book_edit.get("penulis", ""), key="edit_penulis")
    edit_tahun = st.number_input("Tahun Terbit Baru", value=book_edit.get("tahun", 2000), key="edit_tahun")
    edit_stok = st.number_input("Stok Baru", value=book_edit.get("stok", 1), key="edit_stok")
    genre_options = ["Fiksi","Non-Fiksi","Sains","Teknologi","Sejarah","Biografi","Fantasi","Lainnya"]
    edit_genre = st.selectbox(
        "Genre Baru",
        genre_options,
        index=genre_options.index(book_edit.get("genre", genre_options[0])) if book_edit.get("genre") in genre_options else 0,
        key="edit_genre"
    )
    edit_deskripsi = st.text_area("Deskripsi Baru", value=book_edit.get("deskripsi", ""), key="edit_deskripsi")

    new_cover = st.file_uploader("Upload Cover Baru (jpg/png)", type=["jpg", "png"], key="edit_cover")
    new_pdf = st.file_uploader("Upload PDF Baru", type=["pdf"], key="edit_pdf")

    if st.button("Update Detail Buku"):
        update_data = {
            "judul": edit_judul,
            "penulis": edit_penulis,
            "tahun": int(edit_tahun),
            "stok": int(edit_stok),
            "genre": edit_genre,
            "deskripsi": edit_deskripsi
        }

        if new_cover:
            file_bytes = new_cover.read()
            file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{new_cover.name}"
            supabase.storage.from_("uploads").upload(f"covers/{file_name}", file_bytes, {"content-type": new_cover.type})
            update_data["cover_url"] = supabase.storage.from_("uploads").get_public_url(f"covers/{file_name}").public_url

        if new_pdf:
            file_bytes = new_pdf.read()
            file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{new_pdf.name}"
            supabase.storage.from_("uploads").upload(f"pdfs/{file_name}", file_bytes, {"content-type": "application/pdf"})
            update_data["pdf_url"] = supabase.storage.from_("uploads").get_public_url(f"pdfs/{file_name}").public_url

        supabase.table("buku").update(update_data).eq("id_buku", book_edit.get("id_buku")).execute()
        st.success(f"✅ Buku '{edit_judul}' berhasil diperbarui!")
        del st.session_state.edit

# ----------------------------
# Footer
# ----------------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:green;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
