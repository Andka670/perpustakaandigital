import streamlit as st
from supabase import create_client

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

/* Peringatan Denda */
.denda-warning {
    color: red;
    font-weight: bold;
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
# Menu Navigasi Horizontal
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
        if st.button(name, use_container_width=True):
            st.switch_page(page_path)

# ----------------------------
# Judul
# ----------------------------
st.markdown("<h1 class='animated-title'>🔄 Pengembalian Buku</h1>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ----------------------------
# Data Peminjaman (status = dipinjam)
# ----------------------------
peminjaman_data = supabase.table("peminjaman").select(
    "id_peminjaman, id_user, id_buku, status, denda, akun(username), buku(judul)"
).eq("status", "dipinjam").execute().data

if peminjaman_data:
    # Buat daftar user
    user_options = {p['id_user']: p['akun']['username'] for p in peminjaman_data}
    selected_user = st.selectbox(
        "Pilih User",
        options=list(user_options.keys()),
        format_func=lambda x: f"{user_options[x]} (ID: {x})"
    )

    # Filter buku yang dipinjam user terpilih
    buku_user = [p for p in peminjaman_data if p['id_user'] == selected_user]

    # Mapping dropdown berdasarkan id_peminjaman
    buku_options = {
        p['id_peminjaman']: f"{p['buku']['judul']} (Peminjaman ID: {p['id_peminjaman']})"
        for p in buku_user
    }

    selected_peminjaman_id = st.selectbox(
        "Pilih Buku",
        options=list(buku_options.keys()),
        format_func=lambda x: buku_options[x]
    )

    # Cek denda jika ada
    peminjaman_selected = next((p for p in buku_user if p['id_peminjaman'] == selected_peminjaman_id), None)
    if peminjaman_selected and peminjaman_selected.get("denda", 0) > 0:
        st.markdown(
            f"<p class='denda-warning'>⚠️ Buku ini memiliki denda sebesar Rp {peminjaman_selected['denda']:,}!</p>",
            unsafe_allow_html=True
        )

    if st.button("Kembalikan Buku"):
        try:
            if peminjaman_selected:
                selected_buku = peminjaman_selected['id_buku']

                # Update status hanya untuk id_peminjaman ini
                supabase.table("peminjaman").update(
                    {"status": "sudah dikembalikan"}
                ).eq("id_peminjaman", selected_peminjaman_id).execute()

                # Tambah stok buku
                buku_data = supabase.table("buku").select("stok").eq("id_buku", selected_buku).execute().data
                if buku_data:
                    new_stok = buku_data[0]["stok"] + 1
                    supabase.table("buku").update({"stok": new_stok}).eq("id_buku", selected_buku).execute()

                st.success(
                    f"✅ Buku **{peminjaman_selected['buku']['judul']}** dikembalikan oleh "
                    f"User **{user_options[selected_user]}**!\n📚 Stok buku bertambah menjadi {new_stok}"
                )
        except Exception as e:
            st.error(f"❌ Gagal mengembalikan buku: {e}")
else:
    st.info("ℹ️ Tidak ada buku yang sedang dipinjam.")
# =====================================================
# Footer
# =====================================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:green;'>© 2025 Perpustakaan Digital Payakarta</center>",
    unsafe_allow_html=True
)
