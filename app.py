import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timezone, timedelta
from supabase import create_client

# ==========================================
# 1. KONFIGURASI HALAMAN & RESPONSIVE CSS
# ==========================================
st.set_page_config(page_title="Rekarasa | Teman Tumbuhmu", page_icon="🌱", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Global Container */
    .stApp { background-color: #F8FAFC; } 
    
    /* Login Gate Layout */
    .saas-card { 
        background: rgba(255, 255, 255, 0.9); 
        padding: 40px; 
        border-radius: 32px; 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
    }
    
    /* Card Kuesioner */
    .survey-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .survey-card:hover { transform: translateY(-2px); border-color: #0D9488; }
    
    /* Typography */
    .headline { font-size: 2.5rem; font-weight: 800; color: #0F172A; margin-bottom: 10px; }
    
    /* Mobile Override */
    @media (max-width: 768px) {
        .headline { font-size: 1.8rem; }
        .saas-card { padding: 25px; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIKA WAKTU & DATABASE (JANGKAR WIB)
# ==========================================
WIB = timezone(timedelta(hours=7))

@st.cache_resource
def init_connection():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = init_connection()

# ==========================================
# 3. SAAS LOGIN GATEWAY (DYNAMC GRADIENT)
# ==========================================
if 'user_alias' not in st.session_state: st.session_state['user_alias'] = ""

if not st.session_state['user_alias']:
    jam = datetime.now(WIB).hour
    # Gradasi CSS Dinamis sesuai waktu
    if 4 <= jam < 12: bg_gradient = "linear-gradient(135deg, #FFF7ED, #FEF3C7)"
    elif 12 <= jam < 18: bg_gradient = "linear-gradient(135deg, #F0FDFA, #CCFBF1)"
    else: bg_gradient = "linear-gradient(135deg, #EEF2FF, #E0E7FF)"
    
    st.markdown(f"<div style='background: {bg_gradient}; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px;'>", unsafe_allow_html=True)
    
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("<h1>Rekarasa 🌱</h1>", unsafe_allow_html=True)
        # Logika kutipan...
        alias = st.text_input("Namamu:", placeholder="Alias unikmu...")
        if st.button("Mulai Perjalanan"):
            if alias:
                st.session_state['user_alias'] = alias
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 4. DASHBOARD UTAMA (LAYOUT GRID)
# ==========================================
nama_pengguna = st.session_state['user_alias']
st.markdown(f"## Halo, {nama_pengguna}. 👋")

# Implementasi Kuesioner dengan Layout Grid agar tidak berantakan di HP
st.markdown("### 1. Cek Ruang Kapasitas")
cols = st.columns(2) # Grid 2 kolom otomatis menjadi 1 di HP
with cols[0]:
    st.markdown("<div class='survey-card'>", unsafe_allow_html=True)
    st.radio("1. Aku ngerasa ceria...", ["Hampir nggak pernah", "Jarang", "Kadang", "Sering", "Hampir selalu"], horizontal=False)
    st.markdown("</div>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("<div class='survey-card'>", unsafe_allow_html=True)
    st.radio("2. Aku ngerasa tenang...", ["Hampir nggak pernah", "Jarang", "Kadang", "Sering", "Hampir selalu"], horizontal=False)
    st.markdown("</div>", unsafe_allow_html=True)

# Lanjutkan logika upsert dan grafik seperti versi sebelumnya...
