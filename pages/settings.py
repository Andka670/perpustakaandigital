import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta
import time

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
.block-container {max-width:79% !important; padding:70px 10px; background: rgba(255,255,255,0.12); backdrop-filter:blur(12px); border-radius:18px; box-shadow:0 8px 32px rgba(0,0,0,0.3);}
div[data-testid="stButton"] > button {height:75px; width:100% !important; border-radius:12px; font-size:16px; font-weight:bold; background-color:#4CAF50; color:white; border:none; transition:all 0.3s ease; box-shadow:0 4px 6px rgba(0,0,0,0.2);}
div[data-testid="stButton"] > button:hover {background-color:#45a049; transform:scale(1.05); box-shadow:0 6px 12px rgba(0,0,0,0.3);}
div[data-testid="stButton"] > button:active {transform:scale(0.95); box-shadow:0 2px 4px rgba(0,0,0,0.2);}
.animated-title {font-size:40px; font-weight:bold; color:black; text-align:center; display:inline-block; animation:moveTitle 3s infinite alternate ease-in-out;}
@keyframes moveTitle {0% {transform:translateX(-20px); color:#333;} 50% {transform:translateX(20px); color:#4CAF50;} 100% {transform:translateX(-20px); color:#333;}}
</style>
""", unsafe_allow_html=True)

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
        if st.button(name, key=f"nav_{i}", use_container_width=True):
            st.switch_page(page_path)

# ----------------------------
# Judul
# ----------------------------
st.markdown("<h1 class='animated-title'>⚙️ Settings</h1>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ----------------------------
# Input jumlah hari
# ----------------------------
hari = st.number_input(
    "Berapa hari penyimpanan buku dikembalikan sebelum dihapus?",
    min_value=1,
    value=30
)

# ----------------------------
# Hapus otomatis data sudah dikembalikan
# ----------------------------
try:
    peminjaman_data = supabase.table("peminjaman").select("*").eq("status", "sudah dikembalikan").execute().data
    if peminjaman_data:
        deleted_count = 0
        threshold_date = datetime.now() - timedelta(days=hari)
        for p in peminjaman_data:
            tanggal_kembali = datetime.strptime(p["tanggal_kembali"], "%Y-%m-%d")
            if tanggal_kembali <= threshold_date:
                supabase.table("peminjaman").delete().eq("id_user", p["id_user"]).eq("id_buku", p["id_buku"]).execute()
                deleted_count += 1
        if deleted_count > 0:
            st.success(f"✅ Berhasil menghapus {deleted_count} data peminjaman yang sudah dikembalikan lebih dari {hari} hari.")
        else:
            st.info("📭 Tidak ada data yang perlu dihapus.")
except Exception as e:
    st.error(f"❌ Gagal menghapus data: {e}")

# ----------------------------
# Ganti password admin
# ----------------------------
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("🔑 Ganti Password Admin")

new_admin_pass = st.text_input("Password Baru Admin", type="password", placeholder="Masukkan password baru")
confirm_admin_pass = st.text_input("Konfirmasi Password Admin", type="password", placeholder="Konfirmasi password baru")

if st.button("Ganti Password Admin", key="admin_pass_btn"):
    if not new_admin_pass.strip() or not confirm_admin_pass.strip():
        st.warning("⚠️ Harap isi semua field.")
    elif new_admin_pass != confirm_admin_pass:
        st.error("❌ Password baru dan konfirmasi tidak cocok.")
    else:
        try:
            # Update password admin
            update_resp = supabase.table("akun").update({"password": new_admin_pass}).eq("username", "admin").execute()
            if update_resp.data:
                st.success("✅ Password admin berhasil diubah!")
            else:
                st.error("❌ Gagal mengubah password admin.")
        except Exception as e:
            st.error(f"❌ Terjadi error: {e}")

# ----------------------------
# Tombol Logout
# ----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
if st.button("🚪 Logout", type="primary"):
    st.session_state.clear()  # hapus semua session
    st.success("✅ Anda berhasil logout, kembali ke halaman login...")
    st.switch_page("pages/login.py")
