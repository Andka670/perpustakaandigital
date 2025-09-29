import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = (eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Perpustakaan Digital",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# CSS Style
# =====================================================
st.markdown(
    """
<style>
/* (CSS tetap sama persis, tidak diubah) */
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# Cek Login
# =====================================================
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")

user = st.session_state["user"]

# =====================================================
# Title
# =====================================================
st.markdown(
    "<div class='main-title'>Perpustakaan Digital</div><br>",
    unsafe_allow_html=True
)

# =====================================================
# Navigasi
# =====================================================
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

# =====================================================
# Halaman Daftar Buku
# =====================================================
if st.session_state.page == "daftarbuku":
    st.title("📖 Daftar Buku Tersedia")

    try:
        buku_data = supabase.table("buku").select("*").execute().data
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")

    if buku_data:
        st.markdown("### 🔍 Cari Buku")
        col1, col2 = st.columns(2)

        with col1:
            judul_options = ["Semua"] + sorted({b["judul"] for b in buku_data if b.get("judul")})
            pilih_judul = st.selectbox("Pilih Judul Buku", judul_options, key="filter_judul")

        with col2:
            genre_options = ["Semua"] + sorted({b.get("genre", "-") for b in buku_data})
            pilih_genre = st.selectbox("Pilih Genre", genre_options, key="filter_genre")

        buku_data = [
            b for b in buku_data
            if (pilih_judul == "Semua" or b.get("judul") == pilih_judul)
            and (pilih_genre == "Semua" or b.get("genre") == pilih_genre)
        ]

        st.markdown("<hr>", unsafe_allow_html=True)

        num_cols = 3
        rows = [buku_data[i:i + num_cols] for i in range(0, len(buku_data), num_cols)]

        for row in rows:
            cols = st.columns(num_cols, gap="medium")
            for i, buku in enumerate(row):
                # ✅ hanya tampilkan card kalau ada cover_url atau pdf_url
                if not ((buku.get("cover_url") and buku["cover_url"].strip()) or 
                        (buku.get("pdf_url") and buku["pdf_url"].strip())):
                    continue  

                with cols[i]:
                    st.markdown("<div class='book-card'>", unsafe_allow_html=True)

                    # cover
                    if buku.get("cover_url") and buku["cover_url"].strip():
                        try:
                            signed_cover = supabase.storage.from_("uploads").create_signed_url(
                                buku["cover_url"], 3600
                            )["signedURL"]
                            st.markdown(
                                f"<div class='cover-box'><img src='{signed_cover}'/></div>",
                                unsafe_allow_html=True
                            )
                        except:
                            pass

                    # judul & meta
                    st.markdown(
                        f"<div class='book-title'>{buku['judul']}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div class='book-meta'>✍️ {buku['penulis']} | 📅 {buku['tahun']} | 🏷️ {buku.get('genre','-')} | 📦 Stok: {buku.get('stok','-')}</div>",
                        unsafe_allow_html=True
                    )

                    # tombol baca
                    if buku.get("pdf_url") and buku["pdf_url"].strip():
                        try:
                            signed_pdf = supabase.storage.from_("uploads").create_signed_url(
                                buku["pdf_url"], 3600
                            )["signedURL"]
                            st.markdown(
                                f"<a class='read-btn' href='{signed_pdf}' target='_blank'>📕 Baca Buku</a>",
                                unsafe_allow_html=True
                            )
                        except:
                            pass

                    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# Halaman Peminjaman Saya
# =====================================================
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
                "Judul Buku": buku.get("judul", "(Tanpa Judul)"),
                "Penulis": buku.get("penulis", "-"),
                "Tahun": buku.get("tahun", "-"),
                "Genre": buku.get("genre", "-"),
                "Tanggal Pinjam": p["tanggal_pinjam"],
                "Tanggal Kembali": p.get("tanggal_kembali", "-"),
                "Status": p["status"],
                "Denda (Rp)": p.get("denda", 0)
            })

        df = pd.DataFrame(table_data)
        html_table = df.to_html(index=False, classes="styled-table")
        st.markdown(html_table, unsafe_allow_html=True)

# =====================================================
# Halaman Profil
# =====================================================
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")

    st.markdown(
        f"<p class='profil-text'>👤 Username: {user['username']}</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p class='profil-text'>🆔 ID User: {user['id_user']}</p>",
        unsafe_allow_html=True
    )

    if user.get("nama_lengkap"):
        st.markdown(
            f"<p class='profil-text'>📛 Nama Lengkap: {user['nama_lengkap']}</p>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("🔑 Ubah Password")
    st.markdown("<div class='input-animate'>", unsafe_allow_html=True)

    with st.form("ubah_password_form"):
        old_pw = st.text_input("Password Lama", type="password")
        new_pw = st.text_input("Password Baru", type="password")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password")
        submit_pw = st.form_submit_button("💾 Simpan Password")

    st.markdown("</div>", unsafe_allow_html=True)

    if submit_pw:
        if not old_pw or not new_pw or not confirm_pw:
            st.error("⚠️ Semua field wajib diisi!")
        elif new_pw != confirm_pw:
            st.error("❌ Konfirmasi password tidak cocok!")
        else:
            try:
                db_user = (
                    supabase.table("akun")
                    .select("password")
                    .eq("id_user", user["id_user"])
                    .single()
                    .execute()
                )
                if not db_user.data or db_user.data["password"] != old_pw:
                    st.error("❌ Password lama salah!")
                else:
                    supabase.table("akun").update({"password": new_pw}).eq(
                        "id_user", user["id_user"]
                    ).execute()
                    st.success("✅ Password berhasil diperbarui!")
            except Exception as e:
                st.error(f"❌ Gagal mengubah password: {e}")

    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# =====================================================
# Footer
# =====================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:brown;'>© 2025 Perpustakaan Digital Payakarta</center>",
    unsafe_allow_html=True
)
