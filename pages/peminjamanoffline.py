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
# Hilangkan sidebar
# ----------------------------
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# CSS Styling
# ----------------------------
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Navigasi Atas (tidak diubah)
# ----------------------------
menu_options = {
    "📚 Tambah/Ubah Buku": "pages/tambahbuku.py",
    "📋 Tabel User&Buku": "pages/daftarpeminjaman.py",
    "🖊️ Peminjaman Offline": "pages/peminjamanoffline.py",
    "🔄 Pengembalian": "pages/pengembalian.py",
    "⚙️ Settings": "pages/settings.py"
}

left_col, right_col = st.columns([1, 6])
with left_col:
    if st.button("ℹ️ Info Akun", use_container_width=True):
        st.switch_page("pages/admin.py")
with right_col:
    cols = st.columns(len(menu_options))
    for i, (name, page_path) in enumerate(menu_options.items()):
        with cols[i]:
            if st.button(name, use_container_width=True):
                st.switch_page(page_path)

# ----------------------------
# Judul Halaman
# ----------------------------
st.markdown("<h1 class='animated-title'>🖊️ Peminjaman Offline</h1>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ----------------------------
# Ambil data user & buku dari database
# ----------------------------
users = supabase.table("akun").select("id_user, username").execute()
books = supabase.table("buku").select("id_buku, judul, stok").execute()

user_options = {f"{u['id_user']} - {u['username']}": u["id_user"] for u in users.data} if users.data else {}
book_options = {b["judul"]: {"id_buku": b["id_buku"], "stok": b["stok"]} for b in books.data} if books.data else {}

# ----------------------------
# Form Peminjaman Offline (tambah nomor & alamat)
# ----------------------------
with st.form("form_peminjaman_offline"):
    user_label = st.selectbox("👤 Pilih User", list(user_options.keys())) if user_options else None
    buku_judul = st.selectbox("📚 Pilih Buku", list(book_options.keys())) if book_options else None
    nomor = st.text_input("📞 Nomor HP")
    alamat = st.text_area("🏠 Alamat")
    tanggal_pinjam = st.date_input("📅 Tanggal Pinjam", datetime.now())
    tanggal_kembali = st.date_input("📅 Tanggal Kembali")
    submit = st.form_submit_button("💾 Simpan Peminjaman")

# ----------------------------
# Proses Simpan
# ----------------------------
if submit:
    if not user_label or not buku_judul:
        st.error("❌ Data user atau buku tidak tersedia.")
    elif not nomor.strip() or not alamat.strip():
        st.error("❌ Harap isi nomor dan alamat.")
    else:
        user_id = user_options[user_label]
        selected_book = book_options[buku_judul]

        if selected_book["stok"] <= 0:
            st.error(f"❌ Stok buku '{buku_judul}' habis, tidak bisa dipinjam.")
        else:
            try:
                # Insert ke peminjaman termasuk nomor & alamat
                data = {
                    "id_user": user_id,
                    "id_buku": selected_book["id_buku"],
                    "nomor": nomor,
                    "alamat": alamat,
                    "tanggal_pinjam": str(tanggal_pinjam),
                    "tanggal_kembali": str(tanggal_kembali),
                    "status": "dipinjam"
                }
                supabase.table("peminjaman").insert(data).execute()

                # Update stok buku
                new_stok = selected_book["stok"] - 1
                supabase.table("buku").update({"stok": new_stok}).eq("id_buku", selected_book["id_buku"]).execute()

                st.success(
                    f"✅ Peminjaman berhasil!\n\n"
                    f"- User: `{user_label}`\n"
                    f"- Nomor: `{nomor}`\n"
                    f"- Alamat: `{alamat}`\n"
                    f"- Buku: `{buku_judul}`\n"
                    f"- Status: dipinjam\n"
                    f"- Sisa Stok: {new_stok}"
                )
            except Exception as e:
                st.error(f"❌ Gagal mencatat peminjaman: {e}")
