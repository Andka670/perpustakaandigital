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
# CSS Style: (menambahkan awan animasi + pelangi)
# =====================================================
st.markdown(
    """
<style>
/* === Override Streamlit background containers sehingga efek terlihat === */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(to bottom, #f7fbff 0%, #fffaf0 55%); /* lembut, cream/sky */
    overflow-x: hidden;
    position: relative;
    min-height: 100vh;
}

/* ====== Awan animasi ====== */
/* container awan */
.cloud {
    position: absolute;
    top: 8%;
    left: -20%;
    width: 60vw;
    height: 18vh;
    background: linear-gradient(#ffffff, #f1f5f9);
    border-radius: 50%;
    filter: blur(6px);
    opacity: 0.9;
    transform: scale(1.1);
    animation: floatClouds 40s linear infinite;
    z-index: 0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
/* duplicating multiple clouds via pseudo elements */
.cloud:before,
.cloud:after {
    content: "";
    position: absolute;
    background: linear-gradient(#ffffff, #f1f5f9);
    width: 45%;
    height: 70%;
    top: -20%;
    left: 10%;
    border-radius: 50%;
    filter: blur(6px);
    opacity: 0.95;
}
.cloud:after {
    width: 55%;
    height: 55%;
    top: 0%;
    left: 40%;
}

/* additional cloud layers with different speed & position */
.cloud.layer2 {
    top: 20%;
    left: -40%;
    width: 40vw;
    height: 12vh;
    opacity: 0.85;
    animation: floatClouds 55s linear infinite;
}
.cloud.layer3 {
    top: 35%;
    left: -60%;
    width: 70vw;
    height: 20vh;
    opacity: 0.75;
    animation: floatClouds 70s linear infinite;
}

/* keyframe: move clouds horizontally */
@keyframes floatClouds {
    0% {
        transform: translateX(0) scale(1);
    }
    50% {
        transform: translateX(120vw) scale(1.02);
    }
    100% {
        transform: translateX(240vw) scale(1);
    }
}

/* ====== Rainbow (pelangi) ====== */
/* arc container */
.rainbow {
    position: fixed;
    left: 50%;
    bottom: -6vh;
    transform: translateX(-50%);
    width: 120vw;
    height: 40vh;
    pointer-events: none;
    z-index: 0;
    opacity: 0.15; /* lembut */
    mix-blend-mode: screen;
    animation: rainbowPulse 8s ease-in-out infinite;
}

/* create rainbow rings using radial-gradients layered */
.rainbow::before {
    content: "";
    position: absolute;
    left: 50%;
    top: 0;
    transform: translateX(-50%);
    width: 100%;
    height: 200%;
    border-radius: 50%;
    background:
        radial-gradient(closest-side, rgba(255,0,102,0.9) 0%, transparent 40%),
        radial-gradient(closest-side, rgba(255,94,0,0.9) 0%, transparent 44%),
        radial-gradient(closest-side, rgba(255,214,0,0.9) 0%, transparent 48%),
        radial-gradient(closest-side, rgba(0,180,81,0.9) 0%, transparent 52%),
        radial-gradient(closest-side, rgba(0,112,255,0.9) 0%, transparent 56%),
        radial-gradient(closest-side, rgba(124,0,255,0.9) 0%, transparent 60%);
    background-blend-mode: screen;
    opacity: 0.95;
    filter: blur(18px);
}

/* slight pulsing animation for rainbow */
@keyframes rainbowPulse {
    0% { transform: translateX(-50%) translateY(0) scale(1); opacity: 0.12; }
    50% { transform: translateX(-50%) translateY(-2%) scale(1.02); opacity: 0.18; }
    100% { transform: translateX(-50%) translateY(0) scale(1); opacity: 0.12; }
}

/* ====== Card / content styling (jaga agar teks cokelat terbaca) ====== */
.book-card {
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    height:100%;
    padding:12px;
    border-radius:14px;
    background: rgba(255, 250, 240, 0.95); /* cream semi-opaque supaya terlihat di atas awan/pelangi */
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
    animation:fadeIn 0.6s ease-in-out;
    z-index: 2;
}

.cover-box {
    width:100%;
    aspect-ratio:3/4;
    overflow:hidden;
    border-radius:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.12);
    margin-bottom:10px;
}
.cover-box img {
    width:100%;
    height:100%;
    object-fit:cover;
}

/* teks judul & meta berwarna cokelat */
.book-title {
    font-weight:bold;
    font-size:16px;
    margin:8px 0;
    flex-grow:1;
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
    overflow:hidden;
    text-overflow:ellipsis;
    min-height:50px;
    color: #5C3A21 !important; /* cokelat hangat */
}
.book-meta {
    font-size:13px;
    color: #5C3A21 !important; /* cokelat hangat */
    margin-bottom:10px;
}
.book-desc {
    font-size:13px;
    color: #5C3A21; /* cokelat */
    margin-bottom:8px;
}

/* tombol baca */
.read-btn {
    display:inline-block;
    width:100%;
    min-height:45px;
    padding:12px 0;
    background:linear-gradient(270deg, #6a3a00, #b88229);
    background-size:200% 200%;
    color:white !important;
    text-decoration:none;
    border-radius:12px;
    font-weight:bold;
    text-align:center;
    margin-top:auto;
    transition:all 0.4s ease-in-out;
    animation:gradientShift 6s ease infinite;
}
.read-btn:hover {
    transform:translateY(-3px);
    box-shadow:0 8px 18px rgba(0,0,0,0.12);
}
@keyframes gradientShift {
    0%{background-position:left;}
    50%{background-position:right;}
    100%{background-position:left;}
}

/* page title dan profile text */
.main-title { text-align:center; font-size:52px; font-weight:bold; color:#3d2b1f; }
.profil-text { color: #5C3A21 !important; font-weight:bold; font-size:18px; }

/* other utilities */
@keyframes fadeIn {
    from{opacity:0; transform:translateY(-8px);}
    to{opacity:1; transform:translateY(0);}
}

/* ensure UI elements appear above decorative layers */
[data-testid="stHeader"], .block-container, .stMarkdown, .stButton {
    position: relative;
    z-index: 3;
}
</style>
""",
    unsafe_allow_html=True,
)

# Inject actual cloud and rainbow DOM nodes so pseudo/CSS can animate them
st.markdown(
    """
<div class="cloud"></div>
<div class="cloud layer2"></div>
<div class="cloud layer3"></div>
<div class="rainbow"></div>
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
                        st.markdown("<div class='book-card'>", unsafe_allow_html=True)

                        # cover
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
                            f"<div class='book-title'>{buku.get('judul','-')}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div class='book-meta'>✍️ {buku.get('penulis','-')} | 📅 {buku.get('tahun','-')} | 🏷️ {buku.get('genre','-')} | 📦 Stok: {buku.get('stok','-')}</div>",
                            unsafe_allow_html=True
                        )

                        # deskripsi
                        if buku.get("deskripsi"):
                            deskripsi_pendek = buku["deskripsi"][:150] + ("..." if len(buku["deskripsi"]) > 150 else "")
                            st.markdown(f"<div class='book-desc'>{deskripsi_pendek}</div>", unsafe_allow_html=True)
                            with st.expander("📖 Selengkapnya"):
                                st.write(buku["deskripsi"])

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
                "Tanggal Pinjam": p.get("tanggal_pinjam", "-"),
                "Tanggal Kembali": p.get("tanggal_kembali", "-"),
                "Status": p.get("status", "-"),
                "Denda (Rp)": p.get("denda", 0)
            })

        df = pd.DataFrame(table_data)

        # Styling warna denda
        def color_denda(row):
            if row["Denda (Rp)"] > 0:
                if row["Status"].lower() == "dipinjam":
                    return ["color: red" if col == "Denda (Rp)" else "" for col in df.columns]
                elif row["Status"].lower() == "sudah dikembalikan":
                    return ["color: green" if col == "Denda (Rp)" else "" for col in df.columns]
            return [""] * len(df.columns)

        styled_df = df.style.apply(color_denda, axis=1)
        st.dataframe(styled_df, use_container_width=True)

# =====================================================
# Halaman Profil
# =====================================================
elif st.session_state.page == "profil":
    st.title("⚙️ Profil")

    st.markdown(
        f"<p class='profil-text'>👤 Username: {user.get('username','-')}</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p class='profil-text'>🆔 ID User: {user.get('id_user','-')}</p>",
        unsafe_allow_html=True
    )

    if user.get("nama_lengkap"):
        st.markdown(
            f"<p class='profil-text'>📛 Nama Lengkap: {user.get('nama_lengkap')}</p>",
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
    "<center style='color:#5C3A21;'>© 2025 Perpustakaan Digital Payakarta</center>",
    unsafe_allow_html=True
)
