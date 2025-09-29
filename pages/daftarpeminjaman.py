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

[data-testid="stDataFrame"] table td {
    text-align: left !important;
}
[data-testid="stDataFrame"] table th {
    text-align: left !important;
}
</style>
""", unsafe_allow_html=True)

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
    if row["Status"] == "dipinjam" and row["Denda (Rp)"] > 0:
        return ["color: red" if col == "Denda (Rp)" else "" for col in row.index]
    elif row["Status"] == "sudah dikembalikan" and row["Denda (Rp)"] > 0:
        return ["color: green" if col == "Denda (Rp)" else "" for col in row.index]
    else:
        return ["" for _ in row.index]

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
        user_list = sorted(list({p["id_user"] for p in peminjaman_data}))
        buku_list = sorted(list({p["id_buku"] for p in peminjaman_data}))
        selected_user = st.selectbox("Filter by ID User", ["Semua"] + user_list)
        selected_buku = st.selectbox("Filter by ID Buku", ["Semua"] + buku_list)
        filtered_data = peminjaman_data
        if selected_user != "Semua":
            filtered_data = [p for p in filtered_data if p["id_user"] == selected_user]
        if selected_buku != "Semua":
            filtered_data = [p for p in filtered_data if p["id_buku"] == selected_buku]

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
                "Status": p["status"],
                "Denda (Rp)": p.get("denda", 0)
            })
        if table_dikembalikan:
            df_dikembalikan = pd.DataFrame(table_dikembalikan)
            st.dataframe(df_dikembalikan.style.apply(highlight_denda, axis=1), use_container_width=True)

            # Convert ke Excel
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
# Tabel Buku
# ----------------------------
st.subheader("📚 Daftar Buku")
try:
    buku_data = supabase.table("buku").select("*").execute().data
    if buku_data:
        buku_table = []
        for b in buku_data:
            buku_table.append({
                "ID Buku": b["id_buku"],
                "Judul": b["judul"],
                "Penulis": b["penulis"],
                "Tahun": b["tahun"],
                "Stok": b["stok"],
                "Genre": b["genre"],
                "Deskripsi": b["deskripsi"]
            })
        st.dataframe(pd.DataFrame(buku_table), use_container_width=True)
    else:
        st.info("📭 Belum ada data buku.")
except Exception as e:
    st.error(f"❌ Gagal mengambil data buku: {e}")
