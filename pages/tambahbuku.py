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
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}
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
</style> """, unsafe_allow_html=True)

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

# ----------------------------
# Form ubah detail buku
# ----------------------------
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
    edit_genre = st.selectbox(
        "Genre Baru",
        genre_options,
        index=genre_options.index(book_edit["genre"]) if book_edit.get("genre") in genre_options else 0,
        key="edit_genre"
    )
    edit_deskripsi = st.text_area("Deskripsi Baru", value=book_edit["deskripsi"], key="edit_deskripsi")

    # Upload cover/pdf baru
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

        # Cover baru
        if new_cover is not None:
            file_bytes = new_cover.read()
            cover_path = f"covers/{datetime.now().strftime('%Y%m%d%H%M%S')}_{new_cover.name}"
            supabase.storage.from_("uploads").upload(
                cover_path,
                file_bytes,
                {"content-type": new_cover.type}
            )
            update_data["cover_url"] = cover_path

        # PDF baru
        if new_pdf is not None:
            file_bytes = new_pdf.read()
            pdf_path = f"pdfs/{datetime.now().strftime('%Y%m%d%H%M%S')}_{new_pdf.name}"
            supabase.storage.from_("uploads").upload(
                pdf_path,
                file_bytes,
                {"content-type": "application/pdf"}
            )
            update_data["pdf_url"] = pdf_path

        # Update database
        supabase.table("buku").update(update_data).eq("id_buku", book_edit["id_buku"]).execute()
        st.success(f"✅ Buku '{edit_judul}' berhasil diperbarui!")
        del st.session_state.edit
