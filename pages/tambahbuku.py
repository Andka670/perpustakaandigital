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
# Genre Options
# =====================================================
genre_options = ["Novel", "Komik", "Edukasi", "Sejarah", "Teknologi", "Lainnya"]

# =====================================================
# Form Tambah Buku
# =====================================================
st.title("📚 Manajemen Buku Perpustakaan")

st.subheader("➕ Tambah Buku Baru")
judul = st.text_input("Judul Buku")
penulis = st.text_input("Penulis")
tahun = st.number_input("Tahun Terbit", min_value=0, max_value=2100, step=1)
stok = st.number_input("Jumlah Stok", min_value=0, step=1)
genre = st.selectbox("Genre", genre_options)
deskripsi = st.text_area("Deskripsi")

cover_file = st.file_uploader("Upload Cover (jpg/png)", type=["jpg", "png"], key="new_cover")
pdf_file = st.file_uploader("Upload PDF Buku", type=["pdf"], key="new_pdf")

if st.button("Tambah Buku"):
    cover_url, pdf_url = "", ""

    # Upload cover ke Supabase Storage
    if cover_file is not None:
        file_bytes = cover_file.read()
        file_name = f"covers/{datetime.now().strftime('%Y%m%d%H%M%S')}_{cover_file.name}"
        supabase.storage.from_("covers").upload(file_name, file_bytes)
        cover_url = supabase.storage.from_("covers").get_public_url(file_name)

    # Upload PDF ke Supabase Storage
    if pdf_file is not None:
        file_bytes = pdf_file.read()
        file_name = f"pdfs/{datetime.now().strftime('%Y%m%d%H%M%S')}_{pdf_file.name}"
        supabase.storage.from_("pdfs").upload(file_name, file_bytes)
        pdf_url = supabase.storage.from_("pdfs").get_public_url(file_name)

    supabase.table("buku").insert({
        "judul": judul,
        "penulis": penulis,
        "tahun": int(tahun),
        "stok": int(stok),
        "genre": genre,
        "deskripsi": deskripsi,
        "cover_url": cover_url,
        "pdf_url": pdf_url
    }).execute()

    st.success(f"✅ Buku '{judul}' berhasil ditambahkan!")

# =====================================================
# Form Ubah Detail Buku
# =====================================================
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("✏️ Ubah Detail Buku")

judul_ubah = st.text_input("Masukkan Judul Buku untuk diubah", key="cari_judul")
if st.button("Cari Buku"):
    try:
        book = supabase.table("buku").select("*").eq("judul", judul_ubah).execute().data
        if book:
            st.session_state.edit = book[0]
        else:
            st.warning("Buku tidak ditemukan")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")

if "edit" in st.session_state:
    book_edit = st.session_state.edit
    edit_judul = st.text_input("Judul Baru", value=book_edit["judul"], key="edit_judul")
    edit_penulis = st.text_input("Penulis Baru", value=book_edit["penulis"], key="edit_penulis")
    edit_tahun = st.number_input("Tahun Terbit Baru", value=book_edit["tahun"], key="edit_tahun")
    edit_stok = st.number_input("Stok Baru", value=book_edit["stok"], key="edit_stok")
    edit_genre = st.selectbox("Genre Baru", genre_options, index=genre_options.index(book_edit["genre"]), key="edit_genre")
    edit_deskripsi = st.text_area("Deskripsi Baru", value=book_edit["deskripsi"], key="edit_deskripsi")

    # Tampilkan preview lama
    if book_edit.get("cover_url"):
        st.image(book_edit["cover_url"], width=150, caption="Cover Lama")
    if book_edit.get("pdf_url"):
        st.markdown(f"[📖 Lihat PDF Lama]({book_edit['pdf_url']})")

    # Upload file baru
    new_cover = st.file_uploader("Upload Cover Baru (jpg/png)", type=["jpg", "png"], key="edit_cover")
    new_pdf = st.file_uploader("Upload PDF Baru", type=["pdf"], key="edit_pdf")

    if st.button("Update Detail Buku"):
        cover_url = book_edit.get("cover_url", "")
        pdf_url = book_edit.get("pdf_url", "")

        # Jika ada cover baru
        if new_cover is not None:
            file_bytes = new_cover.read()
            file_name = f"covers/{datetime.now().strftime('%Y%m%d%H%M%S')}_{new_cover.name}"
            supabase.storage.from_("covers").upload(file_name, file_bytes)
            cover_url = supabase.storage.from_("covers").get_public_url(file_name)

        # Jika ada PDF baru
        if new_pdf is not None:
            file_bytes = new_pdf.read()
            file_name = f"pdfs/{datetime.now().strftime('%Y%m%d%H%M%S')}_{new_pdf.name}"
            supabase.storage.from_("pdfs").upload(file_name, file_bytes)
            pdf_url = supabase.storage.from_("pdfs").get_public_url(file_name)

        supabase.table("buku").update({
            "judul": edit_judul,
            "penulis": edit_penulis,
            "tahun": int(edit_tahun),
            "stok": int(edit_stok),
            "genre": edit_genre,
            "deskripsi": edit_deskripsi,
            "cover_url": cover_url,
            "pdf_url": pdf_url
        }).eq("id_buku", book_edit["id_buku"]).execute()

        st.success(f"✅ Buku '{edit_judul}' berhasil diperbarui!")
        del st.session_state.edit
