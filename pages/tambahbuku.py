# =====================================================
# Halaman Tambah Buku
# =====================================================
elif st.session_state.page == "tambahbuku":
    st.title("➕ Tambah Buku")

    # ----------------- Form Tambah Buku Baru -----------------
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
            # Upload cover
            cover_url = None
            if cover:
                supabase.storage.from_("uploads").upload(cover.name, cover.getvalue())
                cover_url = cover.name

            # Upload PDF
            pdf_url = None
            if pdf:
                supabase.storage.from_("uploads").upload(pdf.name, pdf.getvalue())
                pdf_url = pdf.name

            # Insert ke tabel buku
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

    # ----------------- Form Update Stok Buku -----------------
    st.subheader("📦 Update Stok Buku")

    try:
        buku_data = supabase.table("buku").select("id_buku, judul, stok").execute().data
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")

    if buku_data:
        # Buat list untuk selectbox
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
