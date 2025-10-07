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
.animated-title {font-size:40px; font-weight:bold; color:black; text-align:center; display:inline-block; animation:moveTitle 3s infinite alternate ease-in-out;}
@keyframes moveTitle {0% {transform:translateX(-20px); color:#333;} 50% {transform:translateX(20px); color:#4CAF50;} 100% {transform:translateX(-20px); color:#333;}}
</style>
""", unsafe_allow_html=True)
st.markdown(
    "<div class='main-title'>Admin Perpustakaan</div><br>",
    unsafe_allow_html=True
)
# ----------------------------
# Navigasi horizontal
# ----------------------------
menu_options = {
    "ℹ️ Info Akun": "pages/admin.py",
    "📚 Tambah/Ubah Buku": "pages/tambahbuku.py",
    "📋 Data Buku&User": "pages/daftarpeminjaman.py",
    "🖊️ Peminjaman": "pages/peminjamanoffline.py",
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
# Hapus otomatis data sudah dikembalikan dan ditolak
# ----------------------------
try:
    deleted_count = 0
    threshold_date = datetime.now() - timedelta(days=hari)

    # ----------------------------
    # Hapus data dengan status "sudah dikembalikan"
    # ----------------------------
    peminjaman_kembali = supabase.table("peminjaman").select("*").eq("status", "sudah dikembalikan").execute().data
    if peminjaman_kembali:
        for p in peminjaman_kembali:
            try:
                tanggal_kembali = datetime.strptime(p["tanggal_kembali"], "%Y-%m-%d")
                if tanggal_kembali <= threshold_date:
                    supabase.table("peminjaman").delete()\
                        .eq("id_user", p["id_user"])\
                        .eq("id_buku", p["id_buku"])\
                        .execute()
                    deleted_count += 1
            except Exception:
                continue  # Lewati jika tanggal tidak valid

    # ----------------------------
    # Hapus data ajuan yang "ditolak" lebih dari X hari
    # ----------------------------
    ajuan_ditolak = supabase.table("peminjaman").select("*").eq("ajuan", "ditolak").execute().data
    if ajuan_ditolak:
        for p in ajuan_ditolak:
            try:
                # Gunakan created_at sebagai acuan umur ajuan
                created_at_str = p.get("created_at")
                if created_at_str:
                    created_at = datetime.strptime(created_at_str.split("T")[0], "%Y-%m-%d")
                    if created_at <= threshold_date:
                        supabase.table("peminjaman").delete()\
                            .eq("id_user", p["id_user"])\
                            .eq("id_buku", p["id_buku"])\
                            .execute()
                        deleted_count += 1
            except Exception:
                continue

    # ----------------------------
    # Pesan hasil
    # ----------------------------
    if deleted_count > 0:
        st.success(f"🗑️ Berhasil menghapus {deleted_count} data peminjaman/ajuan yang sudah melewati {hari} hari.")
    else:
        st.info("📭 Tidak ada data yang perlu dihapus saat ini.")

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
# =====================================================
# Footer
# =====================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:green;'>© 2025 Perpustakaan Digital Payakarta</center>",
    unsafe_allow_html=True
)
