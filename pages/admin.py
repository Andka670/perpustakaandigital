import streamlit as st
from supabase import create_client, Client

# ----------------------------
# Supabase Config
# ----------------------------
SUPABASE_URL = "https://bcalrkqeeoaalfpjrwvx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWxya3FlZW9hYWxmcGpyd3Z4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDc5NTUsImV4cCI6MjA3Mzc4Mzk1NX0.Pg0EUKGfDYk7-apJNjHoqVSub_atlE54ahVKuWtQc0o"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ----------------------------
# CSS Styling
# ----------------------------
st.markdown("""
    <style>
    /* Hilangkan sidebar */
    section[data-testid="stSidebar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}

    /* Perlebar container utama */
    .block-container {
        max-width: 85% !important;   /* Hampir full layar */
        padding-left: 3% !important;
        padding-right: 10% !important;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        padding-top: 90px;
        padding-bottom: 50px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* Tombol navigasi */
    div[data-testid="stButton"] > button {
        min-height: 50px;
        padding: 25px 80px;
        border-radius: 25px;
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

        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
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
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Mapping menu ke file path
# ----------------------------
menu_options = {
    "📚 Tambah/Ubah Buku": "pages/tambahbuku.py",
    "📋 Data Buku&User": "pages/daftarpeminjaman.py",
    "🖊️ Peminjaman Offline": "pages/peminjamanoffline.py",
    "🔄 Pengembalian": "pages/pengembalian.py",
    "⚙️ Settings": "pages/settings.py"
}

# ----------------------------
# Layout navigasi
# ----------------------------
left_col, right_col = st.columns([1, 6])

with left_col:
    if st.button("ℹ️ Info Akun", use_container_width=True):
        st.switch_page("pages/admin.py")  # pastikan file ini ada

with right_col:
    cols = st.columns(len(menu_options))
    for i, (name, page_path) in enumerate(menu_options.items()):
        with cols[i]:
            if st.button(name, use_container_width=True):
                st.switch_page(page_path)

# ----------------------------
# Judul dengan animasi
# ----------------------------
st.markdown("<h1 class='animated-title'>⚙️ Admin Panel</h1>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ----------------------------
# Ambil data akun dari Supabase
# ----------------------------
def get_akun():
    try:
        response = supabase.table("akun").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Gagal mengambil data akun: {e}")
        return []

akun_list = get_akun()

# ----------------------------
# Selectbox untuk pilih akun
# ----------------------------
if akun_list:
    akun_options = {str(a['id_user']): a for a in akun_list}
    selected_id = st.selectbox("👤 Pilih akun (berdasarkan ID User):", list(akun_options.keys()))
    selected_akun = akun_options[selected_id]

    st.write("### 📌 Keterangan Akun")
    st.markdown(f"""
    - **ID User:** {selected_akun.get('id_user', '')}  
    - **Username:** {selected_akun.get('username', '')}  
    - **Password:** {selected_akun.get('password', '')}  
    """)
else:
    st.warning("⚠️ Tidak ada akun ditemukan di database.")
