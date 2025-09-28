import streamlit as st
from supabase import create_client
from datetime import datetime

# ----------------------------
# Supabase Config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
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
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: ellipsis;
}

div[data-testid="stButton"] > button:hover {background-color: #45a049; transform: scale(1.05);}
div[data-testid="stButton"] > button:active {transform: scale(0.95);}
section[data-testid="stSidebar"] {display: none !important;}

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
# Navigasi seperti settings.py
# ----------------------------
left_col, right_col = st.columns([1,6])

with left_col:
    if st.button("ℹ️ Info Akun", use_container_width=True):
        st.switch_page("pages/admin.py")

menu_options = {
    "📚 Tambah/Ubah Buku": "pages/tambahbuku.py",
    "📋 Data Buku&User": "pages/daftarpeminjaman.py",
    "🖊️ Peminjaman Offline": "pages/peminjamanoffline.py",
    "🔄 Pengembalian": "pages/pengembalian.py",
    "⚙️ Settings": "pages/settings.py"
}

with right_col:
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
# Form tambah/update stok buku
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
            existing = supabase.table("buku").select("*")\
                .eq("judul", judul)\
                .eq("penulis", penulis)\
                .eq("tahun", tahun)\
                .eq("genre", genre).execute().data

            if existing:
                book_id = existing[0]["id_buku"]
                new_stok = existing[0]["stok"] + int(stok)
                supabase.table("buku").update({"stok": new_stok}).eq("id_buku", book_id).execute()
                st.success(f"✅ Stok buku '{judul}' berhasil diperbarui menjadi {new_stok}")
            else:
                same_title = supabase.table("buku").select("*").eq("judul", judul).execute().data
                if same_title:
                    st.warning(f"⚠️ Judul '{judul}' sudah ada dengan kombinasi berbeda. Tidak bisa menambahkan stok.")
                else:
                    cover_url = None
                    pdf_url = None
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

                    if file_cover:
                        cover_name = f"{timestamp}_{file_cover.name}"
                        supabase.storage.from_("uploads").upload(
                            f"covers/{cover_name}",
                            file_cover.read(),
                            {"content-type": f"image/{file_cover.type.split('/')[-1]}"}
                        )
                        cover_url = f"covers/{cover_name}"

                    if file_pdf:
                        pdf_name = f"{timestamp}_{file_pdf.name}"
                        supabase.storage.from_("uploads").upload(
                            f"pdfs/{pdf_name}",
                            file_pdf.read(),
                            {"content-type": "application/pdf"}
                        )
                        pdf_url = f"pdfs/{pdf_name}"

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
                    st.success("✅ Buku baru berhasil ditambahkan!")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

# ----------------------------
# Form ubah detail buku
# ----------------------------
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("Ubah Detail Buku")

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
    cover_file_edit = st.file_uploader("Ganti Cover (opsional)", type=["jpg","png"], key="edit_cover")
    pdf_file_edit = st.file_uploader("Ganti PDF (opsional)", type=["pdf"], key="edit_pdf")

    if st.button("Update Detail Buku"):
        update_book = True
        if edit_judul != book_edit["judul"]:
            existing_title = supabase.table("buku").select("*").eq("judul", edit_judul).execute().data
            if existing_title:
                st.warning(f"⚠️ Judul '{edit_judul}' sudah ada! Pilih judul lain.")
                update_book = False

        if update_book:
            cover_url = book_edit["cover_url"]
            pdf_url = book_edit["pdf_url"]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            if cover_file_edit:
                cover_name = f"{timestamp}_{cover_file_edit.name}"
                supabase.storage.from_("uploads").upload(
                    f"covers/{cover_name}", 
                    cover_file_edit.read(),
                    {"content-type": f"image/{cover_file_edit.type.split('/')[-1]}"}
                )
                cover_url = f"covers/{cover_name}"

            if pdf_file_edit:
                pdf_name = f"{timestamp}_{pdf_file_edit.name}"
                supabase.storage.from_("uploads").upload(
                    f"pdfs/{pdf_name}", 
                    pdf_file_edit.read(),
                    {"content-type": "application/pdf"}
                )
                pdf_url = f"pdfs/{pdf_name}"

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
