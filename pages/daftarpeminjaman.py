import streamlit as st
from supabase import create_client
from datetime import datetime
import pandas as pd
from io import BytesIO

# ----------------------------
# Supabase Config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
</style>
""", unsafe_allow_html=True)
st.markdown(
    "<div class='main-title'>Admin Perpustakaan</div><br>",
    unsafe_allow_html=True
)
# ----------------------------
# Menu navigasi horizontal
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
        if st.button(name, key=f"nav_{i}", use_container_width=True):
            st.switch_page(page_path)

# ----------------------------
# Judul halaman
# ----------------------------
st.markdown("<h1 class='animated-title'>📋 Daftar User dan Buku</h1>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ----------------------------
# Fungsi highlight denda berdasar status
# ----------------------------
def highlight_denda(row):
    styles = [""] * len(row.index)
    if row["Denda (Rp)"] > 0:
        if row["Status"] == "dipinjam":
            styles = ["background-color: #ffcccc; color: brown; font-weight: bold;"] * len(row.index)
        elif row["Status"] == "sudah dikembalikan":
            styles = ["background-color: #ccffcc; color: green; font-weight: bold;"] * len(row.index)
    return styles


# ----------------------------
# Ambil data peminjaman
# ----------------------------
try:
    peminjaman_data = supabase.table("peminjaman").select(
        "id_peminjaman, id_user, id_buku, status, tanggal_pinjam, tanggal_kembali, denda, nomor, alamat, "
        "akun(username), "
        "buku(judul)"
    ).execute().data

    if peminjaman_data:
        # --- Filter ---
        user_list = sorted(list({p["id_user"] for p in peminjaman_data}))
        buku_list = sorted(list({p["id_buku"] for p in peminjaman_data}))
        pinjam_list = sorted(list({p["id_peminjaman"] for p in peminjaman_data}))

        selected_user = st.selectbox("Filter by ID User", ["Semua"] + user_list)
        selected_buku = st.selectbox("Filter by ID Buku", ["Semua"] + buku_list)
        selected_pinjam = st.selectbox("Filter by ID Peminjaman", ["Semua"] + pinjam_list)

        filtered_data = peminjaman_data
        if selected_user != "Semua":
            filtered_data = [p for p in filtered_data if p["id_user"] == selected_user]
        if selected_buku != "Semua":
            filtered_data = [p for p in filtered_data if p["id_buku"] == selected_buku]
        if selected_pinjam != "Semua":
            filtered_data = [p for p in filtered_data if p["id_peminjaman"] == selected_pinjam]

        denda_per_hari = 5000

        # ----------------------------
        # Tabel peminjaman: dipinjam
        # ----------------------------
        st.subheader("📌 Daftar Peminjaman Sedang Dipinjam")
        dipinjam_data = [p for p in filtered_data if p["status"] == "dipinjam"]
        table_dipinjam = []
        for p in dipinjam_data:
            denda = 0
            tanggal_kembali = datetime.strptime(p["tanggal_kembali"], "%Y-%m-%d")
            if datetime.now() > tanggal_kembali:
                terlambat = (datetime.now() - tanggal_kembali).days
                denda = terlambat * denda_per_hari
                supabase.table("peminjaman").update({"denda": denda}).eq("id_peminjaman", p["id_peminjaman"]).execute()
            table_dipinjam.append({
                "ID Peminjaman": p["id_peminjaman"],
                "User": p["akun"]["username"] if p.get("akun") else "-",
                "Nomor": p.get("nomor", "-"),
                "Alamat": p.get("alamat", "-"),
                "Judul Buku": p["buku"]["judul"] if p.get("buku") else "-",
                "Tanggal Pinjam": p["tanggal_pinjam"],
                "Tanggal Kembali": p["tanggal_kembali"],
                "ajuan": p["ajuan"],
                "Status": p["status"],
                "Denda (Rp)": denda
            })
        if table_dipinjam:
            df_dipinjam = pd.DataFrame(table_dipinjam)
            st.dataframe(df_dipinjam.style.apply(highlight_denda, axis=1), use_container_width=True)
        else:
            st.info("📭 Tidak ada peminjaman yang sedang berlangsung.")

        # ----------------------------
        # Tabel peminjaman: sudah dikembalikan + download Excel
        # ----------------------------
        st.subheader("📌 Daftar Peminjaman Sudah Dikembalikan")
        dikembalikan_data = [p for p in filtered_data if p["status"] == "sudah dikembalikan"]
        table_dikembalikan = []
        for p in dikembalikan_data:
            table_dikembalikan.append({
                "ID Peminjaman": p["id_peminjaman"],
                "User": p["akun"]["username"] if p.get("akun") else "-",
                "Nomor": p.get("nomor", "-"),
                "Alamat": p.get("alamat", "-"),
                "Judul Buku": p["buku"]["judul"] if p.get("buku") else "-",
                "Tanggal Pinjam": p["tanggal_pinjam"],
                "Tanggal Kembali": p["tanggal_kembali"],
                "ajuan": p["ajuan"],
                "Status": p["status"],
                "Denda (Rp)": p.get("denda", 0)
            })
        if table_dikembalikan:
            df_dikembalikan = pd.DataFrame(table_dikembalikan)
            st.dataframe(df_dikembalikan.style.apply(highlight_denda, axis=1), use_container_width=True)

            towrite = BytesIO()
            df_dikembalikan.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button(
                label="⬇️ Download Excel Peminjaman Dikembalikan",
                data=towrite,
                file_name="peminjaman_dikembalikan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("📭 Tidak ada peminjaman yang sudah dikembalikan.")

    else:
        st.info("📭 Belum ada data peminjaman.")
except Exception as e:
    st.error(f"❌ Gagal mengambil data peminjaman: {e}")

# ----------------------------
# Tabel Buku + Filter Selectbox
# ----------------------------
st.subheader("📚 Daftar Buku")

try:
    buku_data = supabase.table("buku").select("*").execute().data
    if buku_data:
        # Buat DataFrame dari data buku
        df_buku = pd.DataFrame(buku_data)

        # Ambil nilai unik untuk filter
        genre_list = ["Semua"] + sorted(df_buku["genre"].dropna().unique().tolist())
        penulis_list = ["Semua"] + sorted(df_buku["penulis"].dropna().unique().tolist())
        tahun_list = ["Semua"] + sorted(df_buku["tahun"].dropna().unique().tolist())

        # Buat kolom filter
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_genre = st.selectbox("🎭 Pilih Genre", genre_list)
        with col2:
            selected_penulis = st.selectbox("✍️ Pilih Penulis", penulis_list)
        with col3:
            selected_tahun = st.selectbox("📅 Pilih Tahun", tahun_list)

        # Filter DataFrame sesuai pilihan
        df_filtered = df_buku.copy()

        if selected_genre != "Semua":
            df_filtered = df_filtered[df_filtered["genre"] == selected_genre]
        if selected_penulis != "Semua":
            df_filtered = df_filtered[df_filtered["penulis"] == selected_penulis]
        if selected_tahun != "Semua":
            df_filtered = df_filtered[df_filtered["tahun"] == selected_tahun]

        # Pilih kolom yang ingin ditampilkan
        df_filtered = df_filtered[["id_buku", "judul", "penulis", "tahun", "stok", "genre", "deskripsi"]]
        df_filtered.columns = ["ID Buku", "Judul", "Penulis", "Tahun", "Stok", "Genre", "Deskripsi"]

        # Tampilkan hasil filter
        if not df_filtered.empty:
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.warning("📭 Tidak ada buku yang sesuai dengan filter yang dipilih.")
    else:
        st.info("📭 Belum ada data buku.")
except Exception as e:
    st.error(f"❌ Gagal mengambil data buku: {e}")

# =====================================================
# Footer
# =====================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:green;'>© 2025 Perpustakaan Digital Payakarta</center>",
    unsafe_allow_html=True
)
