import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# ----------------------------
# Supabase Config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Perpustakaan Digital", page_icon="📚", layout="wide")

# ----------------------------
# CSS Background + Animasi
# ----------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f0f0f0, #ffffff);
}
@keyframes titleFadeIn {
    0% {opacity:0; transform:translateY(-20px) scale(0.9);}
    50% {opacity:0.5; transform:translateY(0) scale(1.05);}
    100% {opacity:1; transform:translateY(0) scale(1);}
}
.main-title {
    text-align:center; color:brown; font-size:48px;
    font-weight:bold; animation:titleFadeIn 1.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Cek Login
# ----------------------------
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")

user = st.session_state["user"]

# ----------------------------
# Navigasi
# ----------------------------
menu_options = {
    "📚 Daftar Buku": "daftarbuku",
    "📋 Peminjaman Saya": "peminjamansaya",
    "⚙️ Profil": "profil"
}
if "page" not in st.session_state:
    st.session_state.page = "daftarbuku"

cols_nav = st.columns(len(menu_options), gap="medium")
for i, (name, page_name) in enumerate(menu_options.items()):
    with cols_nav[i]:
        if st.button(name, key=f"nav_{page_name}"):
            st.session_state.page = page_name
st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------
# Halaman Daftar Buku
# ----------------------------
if st.session_state.page == "daftarbuku":
    st.title("📖 Daftar Buku Tersedia")
    try:
        buku_data = supabase.table("buku").select("*").execute().data
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")

    if buku_data:
        judul_options = ["Semua"] + sorted({b["judul"] for b in buku_data if b.get("judul")})
        pilih_judul = st.selectbox("Pilih Judul Buku", judul_options, key="filter_judul")

        genre_options = ["Semua"] + sorted({b.get("genre", "-") for b in buku_data})
        pilih_genre = st.selectbox("Pilih Genre", genre_options, key="filter_genre")

        buku_data = [
            b for b in buku_data
            if (pilih_judul == "Semua" or b.get("judul") == pilih_judul)
            and (pilih_genre == "Semua" or b.get("genre") == pilih_genre)
        ]

        num_cols = 3
        rows = [buku_data[i:i+num_cols] for i in range(0, len(buku_data), num_cols)]
        for row in rows:
            cols = st.columns(num_cols, gap="medium")
            for i, buku in enumerate(row):
                with cols[i]:
                    st.markdown(f"**{buku['judul']}**")
                    st.caption(f"✍️ {buku['penulis']} | 📅 {buku['tahun']} | 🏷️ {buku.get('genre','-')}")

# ----------------------------
# Halaman Peminjaman Saya
# ----------------------------
elif st.session_state.page == "peminjamansaya":
    st.title("📋 Peminjaman Saya")
    try:
        pinjam_data = (
            supabase.table("peminjaman")
            .select("*, buku(judul, penulis, tahun, genre)")
            .eq("id_user", user["id_user"])
            .order("tanggal_pinjam", desc=True)
            .execute()
            .data
        )
    except Exception as e:
        pinjam_data = []
        st.error(f"❌ Gagal mengambil data peminjaman: {e}")

    if not pinjam_data:
        st.info("ℹ️ Kamu belum pernah meminjam buku.")
    else:
        table_data = []
        for p in pinjam_data:
            buku = p.get("buku", {})
            table_data.append({
                "Judul Buku": buku.get("judul", "-"),
                "Penulis": buku.get("penulis", "-"),
                "Tahun": buku.get("tahun", "-"),
                "Genre": buku.get("genre", "-"),
                "Tanggal Pinjam": p["tanggal_pinjam"],
                "Tanggal Kembali": p.get("tanggal_kembali", "-"),
                "Status": p["status"],
                "Denda (Rp)": p.get("denda", 0)
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df)

# ----------------------------
# Halaman Profil
# ----------------------------
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")
    st.write(f"👤 Username: **{user['username']}**")
    st.write(f"🆔 ID User: **{user['id_user']}**")

    st.markdown("---")
    st.subheader("🗑️ Hapus Akun")
    if st.button("❌ Hapus Akun Saya"):
        try:
            # cek apakah user masih ada pinjaman aktif
            pinjam_aktif = (
                supabase.table("peminjaman")
                .select("id_user")
                .eq("id_user", user["id_user"])
                .eq("status", "dipinjam")
                .execute()
                .data
            )

            if pinjam_aktif:
                st.error("⚠️ Akun tidak bisa dihapus, masih ada buku yang sedang dipinjam!")
            else:
                # hapus akun, peminjaman.id_user akan NULL (jika FK pakai ON DELETE SET NULL)
                supabase.table("akun").delete().eq("id_user", user["id_user"]).execute()
                st.success("✅ Akun berhasil dihapus. Kamu akan dialihkan ke halaman login.")
                st.session_state.clear()
                st.switch_page("pages/login.py")

        except Exception as e:
            st.error(f"❌ Gagal menghapus akun: {e}")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# ----------------------------
# Footer
# ----------------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color:brown;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
