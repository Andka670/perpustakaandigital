import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# =====================================================
# Page Config
# =====================================================
st.set_page_config(page_title="Perpustakaan Digital", page_icon="📚", layout="wide")

# =====================================================
# CSS Style
# =====================================================
st.markdown("""
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f0f0f0, #ffffff);
}

/* Title Animasi */
@keyframes titleFadeIn {
    0% {opacity:0; transform:translateY(-20px) scale(0.9);}
    50% {opacity:0.5; transform:translateY(0) scale(1.05);}
    100% {opacity:1; transform:translateY(0) scale(1);}
}
.main-title {
    text-align:center; color:brown; font-size:48px;
    font-weight:bold; animation:titleFadeIn 1.2s ease-in-out;
}

/* Subtitle */
h1, h2, h3, h4 {
    color: brown !important;
}

/* Input Animasi */
@keyframes inputFadeIn {
    0% {opacity:0; transform:translateY(10px) scale(0.95);}
    100% {opacity:1; transform:translateY(0) scale(1);}
}
.input-animate { animation:inputFadeIn 0.8s ease-in-out; }

/* Tombol */
div[data-testid="stButton"] > button {
    width:100%; min-height:50px; padding:15px 0;
    border-radius:20px; font-size:16px; font-weight:bold;
    background-color:brown; color:white; border:none;
    margin-right:5px; transition:all 0.3s ease;
}
div[data-testid="stButton"] > button:hover {
    background-color:#45a049; transform:scale(1.05);
}
div[data-testid="stButton"] > button:active {
    transform:scale(0.95);
}

/* Hilangkan sidebar bawaan */
section[data-testid="stSidebar"] {display:none !important;}

/* Card Buku */
.book-card {
    display:flex; flex-direction:column; justify-content:space-between;
    height:100%; padding:12px; border-radius:14px; background:brown;
    box-shadow:0 3px 8px rgba(0,0,0,0.1); animation:fadeIn 0.6s ease-in-out;
}
.cover-box {
    width:100%; aspect-ratio:3/4; overflow:hidden;
    border-radius:12px; box-shadow:0 2px 6px rgba(0,0,0,0.2);
    margin-bottom:10px;
}
.cover-box img {width:100%; height:100%; object-fit:cover;}
.book-title {
    font-weight:bold; font-size:16px; margin:8px 0; flex-grow:1;
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
    overflow:hidden; text-overflow:ellipsis; min-height:50px;
}
.book-meta {font-size:13px; color:black; margin-bottom:10px;}

/* Tombol Baca Buku */
.read-btn {
    display:inline-block; width:100%; min-height:45px; padding:12px 0;
    background:linear-gradient(270deg, #2575fc, #6a11cb);
    background-size:200% 200%; color:white !important; text-decoration:none;
    border-radius:12px; font-weight:bold; text-align:center;
    margin-top:auto; transition:all 0.4s ease-in-out;
    animation:gradientShift 4s ease infinite;
}
.read-btn:hover {
    background-position:right center; transform:scale(1.05) rotate(-1deg);
    box-shadow:0 6px 16px rgba(0,0,0,0.25);
}
.read-btn:active {transform:scale(0.95);}
@keyframes gradientShift {
    0%{background-position:left center;}
    50%{background-position:right center;}
    100%{background-position:left center;}
}

/* Selectbox */
div[data-baseweb="select"] {
    border-radius:12px; border:2px solid #6a11cb; background:white;
    transition:all 0.3s ease-in-out; animation:fadeIn 0.6s ease-in-out;
}
div[data-baseweb="select"]:hover {
    border-color:#2575fc; box-shadow:0 0 10px rgba(37,117,252,0.4);
    transform:scale(1.02);
}
@keyframes fadeIn {
    from{opacity:0; transform:translateY(-8px);}
    to{opacity:1; transform:translateY(0);}
}

/* Profil text */
.profil-text {
    color: brown !important;
    font-weight: bold;
    font-size: 18px;
}

/* Label input password */
div[data-baseweb="input"] input {
    color: brown !important;
}

/* Tabel custom */
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
    color: brown;
    padding: 8px;
    border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Cek Login
# =====================================================
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")

user = st.session_state["user"]

# =====================================================
# Title
# =====================================================
st.markdown("<div class='main-title'>Perpustakaan Digital</div><br>", unsafe_allow_html=True)

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
        rows = [buku_data[i:i+num_cols] for i in range(0, len(buku_data), num_cols)]
        for row in rows:
            cols = st.columns(num_cols, gap="medium")
            for i, buku in enumerate(row):
                with cols[i]:
                    st.markdown("<div class='book-card'>", unsafe_allow_html=True)

                    if buku.get("cover_url"):
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

                    st.markdown(f"<div class='book-title'>{buku['judul']}</div>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='book-meta'>✍️ {buku['penulis']} | 📅 {buku['tahun']} | 🏷️ {buku.get('genre','-')}</div>",
                        unsafe_allow_html=True
                    )

                    if buku.get("pdf_url"):
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
    st.markdown(f"<p class='profil-text'>👤 Username: {user['username']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='profil-text'>🆔 ID User: {user['id_user']}</p>", unsafe_allow_html=True)

    if user.get("nama_lengkap"):
        st.markdown(f"<p class='profil-text'>📛 Nama Lengkap: {user['nama_lengkap']}</p>", unsafe_allow_html=True)

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
                db_user = supabase.table("akun").select("password").eq("id_user", user["id_user"]).single().execute()
                if not db_user.data or db_user.data["password"] != old_pw:
                    st.error("❌ Password lama salah!")
                else:
                    supabase.table("akun").update({"password": new_pw}).eq("id_user", user["id_user"]).execute()
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
st.markdown("<center style='color:brown;'>© 2025 Perpustakaan Digital Payakarta</center>", unsafe_allow_html=True)
