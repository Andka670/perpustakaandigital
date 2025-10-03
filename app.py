import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# =====================================================
# Supabase Config
# =====================================================
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o")
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
/* Background langit */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(to bottom, #87ceeb, #ffffff);
    height: 100%;
    margin: 0;
    overflow: hidden;
}

/* Matahari */
.sun {
    position: absolute;
    top: 50px;
    left: 70%;
    width: 120px;
    height: 120px;
    background: radial-gradient(circle, #FFD700 60%, #FFA500 100%);
    border-radius: 50%;
    box-shadow: 0 0 80px 20px rgba(255, 223, 0, 0.7);
    animation: shine 6s ease-in-out infinite alternate;
}
@keyframes shine {
    0% { transform: scale(1); opacity: 0.9; }
    100% { transform: scale(1.1); opacity: 1; }
}

/* Pelangi */
.rainbow {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 600px;
    height: 300px;
    margin-left: -300px;
    border-radius: 300px 300px 0 0;
    background: conic-gradient(red, orange, yellow, green, blue, indigo, violet, red);
    opacity: 0.6;
    animation: fadeIn 10s ease-in-out infinite alternate;
}
@keyframes fadeIn {
    0% { opacity: 0; transform: scale(0.9); }
    100% { opacity: 0.6; transform: scale(1); }
}

/* Awan */
.cloud {
    position: absolute;
    background: radial-gradient(circle at 30% 30%, #fff 70%, #f0f0f0 100%);
    border-radius: 50%;
    opacity: 0.9;
    animation: moveClouds 60s linear infinite;
}
.cloud::before, .cloud::after {
    content: "";
    position: absolute;
    background: inherit;
    border-radius: 50%;
}
.cloud::before { width: 80px; height: 80px; top: -20px; left: -40px; }
.cloud::after  { width: 60px; height: 60px; top: -10px; right: -30px; }
.cloud.large  { width: 200px; height: 100px; }
.cloud.medium { width: 150px; height: 75px; }
.cloud.small  { width: 100px; height: 50px; }

@keyframes moveClouds {
    0% { left: -300px; }
    100% { left: 110%; }
}

/* Burung */
.bird {
    position: absolute;
    width: 40px;
    height: 40px;
    background: transparent;
    animation: fly 25s linear infinite;
}
.bird::before, .bird::after {
    content: "";
    position: absolute;
    width: 30px;
    height: 10px;
    border-top: 3px solid black;
    border-radius: 50%;
    top: 15px;
}
.bird::before { left: -25px; transform: rotate(-20deg); }
.bird::after  { right: -25px; transform: rotate(20deg); }

@keyframes fly {
    0% { left: -100px; }
    50% { left: 50%; }
    100% { left: 110%; }
}

/* Efek hujan */
.rain {
    position: absolute;
    width: 100%;
    height: 100%;
    pointer-events: none;
}
.raindrop {
    position: absolute;
    width: 2px;
    height: 15px;
    background: rgba(0,0,255,0.4);
    bottom: 100%;
    animation: fall linear infinite;
}
@keyframes fall {
    0%   { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(110vh); opacity: 0; }
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
h1, h2, h3, h4 {
    color: brown !important;
}
</style>
<div class="sun"></div>
<div class="rainbow"></div>
<div class="cloud large" style="top:80px; animation-delay:0s;"></div>
<div class="cloud medium" style="top:150px; animation-delay:20s;"></div>
<div class="cloud small" style="top:250px; animation-delay:40s;"></div>
<div class="bird" style="top:100px; animation-delay:0s;"></div>
<div class="bird" style="top:200px; animation-delay:5s;"></div>
<div class="bird" style="top:300px; animation-delay:10s;"></div>
<div class="rain">
  <div class="raindrop" style="left:10%; animation-duration:1s; animation-delay:0s;"></div>
  <div class="raindrop" style="left:30%; animation-duration:1.2s; animation-delay:0.2s;"></div>
  <div class="raindrop" style="left:50%; animation-duration:0.9s; animation-delay:0.4s;"></div>
  <div class="raindrop" style="left:70%; animation-duration:1.3s; animation-delay:0.1s;"></div>
  <div class="raindrop" style="left:90%; animation-duration:1s; animation-delay:0.3s;"></div>
</div>
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
        buku_data = (
            supabase.table("buku")
            .select("id_buku, judul, penulis, tahun, genre, stok, cover_url, pdf_url, deskripsi")
            .execute()
            .data
        )
    except Exception as e:
        buku_data = []
        st.error(f"❌ Gagal mengambil data buku: {e}")

    if buku_data:
        buku_data = [b for b in buku_data if b.get("cover_url") and b["cover_url"].strip()]

        if not buku_data:
            st.info("ℹ️ Tidak ada buku dengan cover yang tersedia.")
        else:
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
                    with cols[i]:
                        st.image(
                            supabase.storage.from_("uploads").create_signed_url(buku["cover_url"], 3600)["signedURL"],
                            use_container_width=True
                        )
                        st.markdown(f"**{buku['judul']}**")
                        st.caption(f"✍️ {buku['penulis']} | 📅 {buku['tahun']} | 🏷️ {buku['genre']} | 📦 Stok: {buku['stok']}")
                        if buku.get("pdf_url"):
                            signed_pdf = supabase.storage.from_("uploads").create_signed_url(buku["pdf_url"], 3600)["signedURL"]
                            st.markdown(f"[📕 Baca Buku]({signed_pdf})")

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
        st.dataframe(df, use_container_width=True)

# =====================================================
# Halaman Profil
# =====================================================
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")
    st.write(f"👤 Username: {user['username']}")
    st.write(f"🆔 ID User: {user['id_user']}")
    if user.get("nama_lengkap"):
        st.write(f"📛 Nama Lengkap: {user['nama_lengkap']}")

    st.subheader("🔑 Ubah Password")
    with st.form("ubah_password_form"):
        old_pw = st.text_input("Password Lama", type="password")
        new_pw = st.text_input("Password Baru", type="password")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password")
        submit_pw = st.form_submit_button("💾 Simpan Password")

    if submit_pw:
        if not old_pw or not new_pw or not confirm_pw:
            st.error("⚠️ Semua field wajib diisi!")
        elif new_pw != confirm_pw:
            st.error("❌ Konfirmasi password tidak cocok!")
        else:
            db_user = supabase.table("akun").select("password").eq("id_user", user["id_user"]).single().execute()
            if not db_user.data or db_user.data["password"] != old_pw:
                st.error("❌ Password lama salah!")
            else:
                supabase.table("akun").update({"password": new_pw}).eq("id_user", user["id_user"]).execute()
                st.success("✅ Password berhasil diperbarui!")

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
