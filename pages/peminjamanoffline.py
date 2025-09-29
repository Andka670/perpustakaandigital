import streamlit as st
from supabase import create_client
from datetime import datetime, date
import pandas as pd

# ----------------------------
# Supabase Config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}
.block-container {
    max-width: 80% !important;
    padding: 2% 5% !important;
}
.styled-table {
    border-collapse: collapse;
    width: 100%;
}
.styled-table th {
    background-color: #f9f4f0;
    color: brown;
    padding: 8px;
}
.styled-table td {
    padding: 8px;
    border-top: 1px solid #ddd;
}
.red { background-color: #f8d7da; color: #721c24; }
.green { background-color: #d4edda; color: #155724; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Judul Halaman
# ----------------------------
st.title("🔄 Pengembalian Buku")

# ----------------------------
# Ambil data peminjaman
# ----------------------------
try:
    peminjaman_data = supabase.table("peminjaman").select(
        "id_peminjaman, id_user, id_buku, status, denda, tanggal_kembali, akun(username), buku(judul)"
    ).execute().data
except Exception as e:
    st.error(f"❌ Gagal mengambil data peminjaman: {e}")
    peminjaman_data = []

if not peminjaman_data:
    st.info("ℹ️ Tidak ada data peminjaman.")
else:
    # Buat daftar user
    user_options = {p['id_user']: p['akun']['username'] for p in peminjaman_data}
    selected_user = st.selectbox(
        "Pilih User",
        options=list(user_options.keys()),
        format_func=lambda x: f"{user_options[x]} (ID: {x})"
    )

    # Filter buku yang dipinjam user terpilih
    buku_user = [p for p in peminjaman_data if p['id_user'] == selected_user]

    # Dropdown buku
    buku_options = {p['id_peminjaman']: f"{p['buku']['judul']} (ID: {p['id_peminjaman']})" for p in buku_user}
    selected_peminjaman_id = st.selectbox(
        "Pilih Buku",
        options=list(buku_options.keys()),
        format_func=lambda x: buku_options[x]
    )

    # Tombol kembalikan
    if st.button("Kembalikan Buku"):
        try:
            peminjaman_selected = next((p for p in buku_user if p['id_peminjaman'] == selected_peminjaman_id), None)
            if peminjaman_selected:
                # Hitung denda otomatis
                tanggal_kembali = datetime.strptime(peminjaman_selected["tanggal_kembali"], "%Y-%m-%d").date()
                today = date.today()
                hari_terlambat = (today - tanggal_kembali).days
                denda = 10000 * hari_terlambat if hari_terlambat > 0 else 0

                # Update status dan denda
                supabase.table("peminjaman").update({
                    "status": "sudah dikembalikan",
                    "denda": denda
                }).eq("id_peminjaman", selected_peminjaman_id).execute()

                # Tambah stok buku
                buku_id = peminjaman_selected['id_buku']
                buku_data = supabase.table("buku").select("stok").eq("id_buku", buku_id).execute().data
                if buku_data:
                    new_stok = buku_data[0]["stok"] + 1
                    supabase.table("buku").update({"stok": new_stok}).eq("id_buku", buku_id).execute()

                st.success(f"✅ Buku **{peminjaman_selected['buku']['judul']}** dikembalikan! Denda: Rp {denda:,}\n📚 Stok buku sekarang: {new_stok}")
        except Exception as e:
            st.error(f"❌ Gagal mengembalikan buku: {e}")

    # Tampilkan tabel peminjaman user
    table_rows = []
    for p in buku_user:
        denda_calc = p.get("denda") or 0
        # Jika status dipinjam dan melewati tanggal_kembali, hitung denda
        if p['status'] == "dipinjam":
            tanggal_kembali = datetime.strptime(p["tanggal_kembali"], "%Y-%m-%d").date()
            hari_terlambat = (date.today() - tanggal_kembali).days
            if hari_terlambat > 0:
                denda_calc = 10000 * hari_terlambat
        table_rows.append({
            "Judul Buku": p['buku']['judul'],
            "Status": p['status'],
            "Tanggal Kembali": p['tanggal_kembali'],
            "Denda (Rp)": denda_calc,
            "Class": "red" if (p['status'] == "dipinjam" and denda_calc > 0) else ("green" if (p['status'] == "sudah dikembalikan" and denda_calc > 0) else "")
        })

    # Buat DataFrame untuk tabel
    df = pd.DataFrame(table_rows)
    # Buat HTML tabel custom dengan warna
    html_table = "<table class='styled-table'><tr>"
    for col in df.columns[:-1]:
        html_table += f"<th>{col}</th>"
    html_table += "</tr>"

    for _, row in df.iterrows():
        class_row = row["Class"]
        html_table += f"<tr class='{class_row}'>"
        for col in df.columns[:-1]:
            html_table += f"<td>{row[col]}</td>"
        html_table += "</tr>"
    html_table += "</table>"

    st.markdown(html_table, unsafe_allow_html=True)
