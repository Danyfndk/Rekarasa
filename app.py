import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timezone, timedelta
from supabase import create_client, Client

# ==========================================
# 1. KONFIGURASI HALAMAN & RESPONSIVE CSS
# ==========================================
st.set_page_config(
    page_title="Rekarasa | Teman Tumbuhmu", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #F8FAFC; } 
    
    /* Hide Streamlit Branding for SaaS look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* -----------------------------------
       SaaS COLOR PALETTE & TYPOGRAPHY
       ----------------------------------- */
    .hero-title { color: #0F172A; font-weight: 800; font-size: 3.5rem; letter-spacing: -1.5px; margin-bottom: 0.2rem; line-height: 1.1;}
    .hero-subtitle { color: #64748B; line-height: 1.6; font-size: 1.15rem; max-width: 90%; font-weight: 400;}
    h2 { color: #0F172A; font-weight: 700 !important; font-size: 1.8rem; padding-bottom: 15px; margin-bottom: 25px; border-bottom: 2px solid #F1F5F9;}
    
    /* -----------------------------------
       MODERN CARDS & CONTAINERS
       ----------------------------------- */
    div[role="radiogroup"] { 
        background: #FFFFFF; 
        padding: 20px 25px; 
        border-radius: 16px; 
        border: 1px solid #E2E8F0; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease;
    }
    div[role="radiogroup"]:hover { border-color: #0D9488; box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.08); }
    .question-text { font-weight: 700; color: #1E293B; font-size: 1.05rem; margin-bottom: 12px; line-height: 1.5; }
    
    .alias-box { 
        background: #FFFFFF; 
        padding: 40px; 
        border-radius: 24px; 
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        text-align: center; 
        max-width: 550px; 
        margin: 8vh auto; 
    }
    
    /* Insight Boxes */
    .insight-box {
        background-color: #F0FDF4; border-left: 5px solid #0D9488; padding: 1.8rem;
        border-radius: 12px; margin-bottom: 1.5rem; color: #115E59; font-size: 1.05rem; line-height: 1.6;
    }
    .insight-box-warning {
        background-color: #FFFBEB; border-left: 5px solid #D97706; padding: 1.8rem;
        border-radius: 12px; margin-bottom: 1.5rem; color: #92400E; font-size: 1.05rem; line-height: 1.6;
    }

    /* -----------------------------------
       BUTTONS & METRICS
       ----------------------------------- */
    .stButton>button { 
        background-color: #0F172A; color: white; border-radius: 12px; 
        padding: 0.6rem 2rem; border: none; font-weight: 600; font-size: 1rem;
        transition: all 0.3s ease; width: auto;
    }
    .stButton>button:hover { background-color: #0D9488; color: white; transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.3); }
    
    [data-testid="stMetric"] {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 1.5rem !important;
        border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        border-top: 5px solid #0D9488;
    }
    [data-testid="stMetricValue"] > div { font-size: 1.6rem !important; font-weight: 800 !important; color: #0F172A !important; line-height: 1.2 !important; white-space: normal !important; word-wrap: break-word !important;}
    [data-testid="stMetricLabel"] > div { color: #64748B !important; font-size: 0.8rem !important; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 5px;}

    /* Utilities */
    .scroll-hint { text-align: center; color: #94A3B8; font-size: 0.85rem; font-weight: 700; margin-top: 20px; margin-bottom: 50px; text-transform: uppercase; letter-spacing: 1.5px; }
    .spacer-top { margin-top: 3rem; }

    /* -----------------------------------
       MOBILE RESPONSIVENESS (SMARTPHONES)
       ----------------------------------- */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2rem; }
        .hero-subtitle { font-size: 1rem; max-width: 100%; }
        h2 { font-size: 1.4rem; margin-bottom: 15px; }
        .alias-box { padding: 25px; margin: 5vh 15px; }
        
        .stButton>button { width: 100%; margin-top: 10px; }
        div[role="radiogroup"] { padding: 18px 20px; border-radius: 12px;}
        .question-text { font-size: 1rem; }
        
        .insight-box, .insight-box-warning { padding: 1.2rem; font-size: 0.95rem; }
        .spacer-top { margin-top: 1.5rem; }
        
        [data-testid="stMetric"] { padding: 1.2rem !important; margin-bottom: 10px; }
        [data-testid="stMetricValue"] > div { font-size: 1.4rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI DATABASE & WAKTU LOKAL (WIB)
# ==========================================
# Konfigurasi zona waktu patokan: UTC+7 (WIB)
WIB = timezone(timedelta(hours=7))

@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Gagal terhubung ke database. Pastikan pengaturan Secrets di Streamlit Cloud sudah benar.")
    st.stop()

def upsert_jurnal(nama_alias, tgl_input, **kwargs):
    tgl_str = str(tgl_input)
    response = supabase.table("rekarasa_jurnal").select("*").eq("nama_pengguna", nama_alias).eq("tanggal", tgl_str).execute()
    data_baru = {"nama_pengguna": nama_alias, "tanggal": tgl_str}
    if response.data:
        data_baru.update(response.data[0]) 
    data_baru.update(kwargs) 
    supabase.table("rekarasa_jurnal").upsert(data_baru).execute()

# ==========================================
# 3. SAAS LOGIN GATEWAY (DYNAMIC EMPATHY)
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)

if 'user_alias' not in st.session_state:
    st.session_state['user_alias'] = ""

col_empty1, col_login_box, col_empty2 = st.columns([1, 2, 1])
with col_login_box:
    if not st.session_state['user_alias']:
        # Ambil waktu WIB secara real-time
        waktu_sekarang = datetime.now(WIB)
        jam = waktu_sekarang.hour
        
        # Logika Dinamis Penyambut berdasarkan Psikologi Waktu
        if 4 <= jam < 12:
            sapaan = "Selamat Pagi."
            kutipan = '"Luka adalah tempat di mana cahaya mulai memasukimu."<br>— Jalaluddin Rumi'
            pengantar = "Mari mulai hari ini dengan pelan-pelan. Tidak perlu langsung utuh, satu langkah kecil saja sudah sangat berarti. Ketik namamu untuk masuk ke ruang amanmu."
            warna_kutipan = "#D97706" # Warm Morning Orange
        elif 12 <= jam < 18:
            sapaan = "Selamat Siang."
            kutipan = '"Di tengah musim dingin yang paling membeku, aku akhirnya menemukan bahwa di dalam diriku ada musim panas yang tak terkalahkan."<br>— Albert Camus'
            pengantar = "Apapun yang sedang riuh dan melelahkan di luar sana, ruang ini akan selalu tenang untukmu. Mari letakkan sejenak lelahmu di sini."
            warna_kutipan = "#0D9488" # Calm Teal
        else:
            sapaan = "Selamat Malam."
            kutipan = '"Terkadang, keberanian paling besar di penghujung hari adalah sekadar berbisik: aku akan mencobanya lagi besok."<br>— Mary Anne Radmacher'
            pengantar = "Bintang tak akan bisa bersinar tanpa kegelapan. Kamu sudah bertahan dengan sangat luar biasa hari ini. Masuklah, dan biarkan kepalamu beristirahat."
            warna_kutipan = "#4338CA" # Deep Indigo Night
        
        # Tampilan UI Dinamis
        html_gate = f"""
        <div class='alias-box'>
            <h3 style='color:#0F172A; font-weight:800; font-size:2rem; margin-bottom:5px;'>{sapaan}</h3>
            <p style='font-size:1.05rem; font-weight:600; color:{warna_kutipan}; font-style:italic; margin-bottom:20px; line-height:1.5;'>{kutipan}</p>
            <p style='color:#64748B; margin-bottom:25px; font-size:0.95rem; line-height:1.6;'>{pengantar}</p>
        </div>
        """
        st.markdown(html_gate, unsafe_allow_html=True)
        
        # Input Login
        input_nama = st.text_input("Alias", placeholder="Ketik nama alias rahasiamu di sini...", label_visibility="collapsed")
        if st.button("Masuk ke Ruangku"):
            if input_nama:
                st.session_state['user_alias'] = input_nama
                st.rerun()
            else:
                st.warning("Silakan isi namamu terlebih dahulu.")
        st.stop()

nama_pengguna = st.session_state['user_alias']

# --- TARIK DATA ---
@st.cache_data(ttl=2) 
def get_user_data(nama_alias):
    resp = supabase.table("rekarasa_jurnal").select("*").eq("nama_pengguna", nama_alias).execute()
    if resp.data:
        df = pd.DataFrame(resp.data)
        df['tanggal'] = pd.to_datetime(df['tanggal']).dt.date
        return df.sort_values('tanggal')
    return pd.DataFrame(columns=["nama_pengguna", "tanggal", "skor_who5", "fase_hidup", "skor_pertumbuhan", "catatan", "jurnal"])

df_jurnal = get_user_data(nama_pengguna)
hari_ini = datetime.now(WIB).date() # Dikunci ke tanggal WIB

fase_saat_ini = "Baru Mulai Melangkah"
if not df_jurnal.empty:
    data_hari_ini = df_jurnal[df_jurnal['tanggal'] == hari_ini]
    if not data_hari_ini.empty and pd.notna(data_hari_ini.iloc[0]['fase_hidup']):
        fase_saat_ini = data_hari_ini.iloc[0]['fase_hidup']
    else:
        riwayat_fase = df_jurnal.dropna(subset=['fase_hidup'])
        if not riwayat_fase.empty:
            fase_saat_ini = riwayat_fase.iloc[-1]['fase_hidup']

# ==========================================
# 4. DASHBOARD HEADER
# ==========================================
st.markdown("---")
col_title, col_metric = st.columns([2.5, 1.2])

with col_title:
    st.markdown(f'<div class="hero-title">Halo, {nama_pengguna}.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Berdasarkan model <b>Growing Around Grief</b>. Kita tidak mengecilkan duka, kita memperluas ruang hidup untuk menampungnya.</div>', unsafe_allow_html=True)

with col_metric:
    st.metric(label="Fase Hidupmu Saat Ini", value=fase_saat_ini)
    if st.button("Keluar (Ganti Akun)", key="logout_btn"):
        st.session_state['user_alias'] = ""
        st.rerun()

st.markdown("<br><hr><div class='spacer-top'></div>", unsafe_allow_html=True)


# ==========================================
# BLOK 1: ASESMEN (WHO-5 WELL-BEING INDEX)
# ==========================================
st.markdown("<h2>1. Cek Ruang Kapasitas (WHO-5 Index)</h2>", unsafe_allow_html=True)
st.write("Skrining singkat standar kesehatan mental global. Pilih yang paling sesuai dengan kondisimu **beberapa hari terakhir**.")

opsi_skala = ["Hampir nggak pernah", "Jarang", "Kadang-kadang", "Sering", "Hampir selalu"]

with st.form("asesmen_who5"):
    st.markdown("<div class='question-text'>1. Aku ngerasa ceria dan mood lagi lumayan bagus.</div>", unsafe_allow_html=True)
    q1 = st.radio("q1", opsi_skala, horizontal=False, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>2. Aku ngerasa lebih tenang dan rileks.</div>", unsafe_allow_html=True)
    q2 = st.radio("q2", opsi_skala, horizontal=False, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>3. Aku ngerasa aktif dan mau gerak.</div>", unsafe_allow_html=True)
    q3 = st.radio("q3", opsi_skala, horizontal=False, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>4. Pas bangun tidur, aku ngerasa seger (nggak ngerasa capek banget).</div>", unsafe_allow_html=True)
    q4 = st.radio("q4", opsi_skala, horizontal=False, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>5. Keseharianku kerasa ada aja hal yang menarik atau seru.</div>", unsafe_allow_html=True)
    q5 = st.radio("q5", opsi_skala, horizontal=False, label_visibility="collapsed", index=None)
    
    submit_asesmen = st.form_submit_button("Analisis Fase Hidupku")

if submit_asesmen:
    if all([q1, q2, q3, q4, q5]):
        skor_dict = {"Hampir nggak pernah": 1, "Jarang": 2, "Kadang-kadang": 3, "Sering": 4, "Hampir selalu": 5}
        skor_total = skor_dict[q1] + skor_dict[q2] + skor_dict[q3] + skor_dict[q4] + skor_dict[q5]
        
        if skor_total <= 8: fase_baru = "Fokus Bertahan Diri"
        elif skor_total <= 12: fase_baru = "Mulai Beradaptasi"
        elif skor_total <= 16: fase_baru = "Pertumbuhan Seimbang"
        elif skor_total <= 20: fase_baru = "Ekspansi Kehidupan"
        else: fase_baru = "Kapasitas Hidup Luas"
        
        upsert_jurnal(nama_pengguna, hari_ini, skor_who5=skor_total, fase_hidup=fase_baru)
        get_user_data.clear() 
        
        st.session_state['notif_who5'] = fase_baru
        st.rerun() 
    else:
        st.warning("Mohon lengkapi semua pertanyaan terlebih dahulu.")

if 'notif_who5' in st.session_state:
    st.success(f"Tersimpan di Cloud! Berdasarkan analisis, fase kamu sekarang ada di: **{st.session_state['notif_who5']}**.")
    del st.session_state['notif_who5']

# --- PEMBATAS VISUAL 1 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Cek jejak langkahmu di bawah ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 2: JEJAK LANGKAH (BEHAVIORAL ACTIVATION)
# ==========================================
st.markdown("<h2>2. Jejak Langkahmu</h2>", unsafe_allow_html=True)
st.write("Pantau seberapa jauh **Ruang Hidupmu** udah bertumbuh dari hari ke hari.")

col_input, col_graph = st.columns([1, 2], gap="large")
with col_input:
    tgl_input = st.date_input("Pilih Tanggal", hari_ini)
    skala_likert = st.radio("Seberapa luas ruang hidupmu hari ini?", ["😢 Terhimpit", "🙁 Terbatas", "😐 Menengah", "🙂 Meluas", "😄 Bertumbuh"], horizontal=True, index=None)
    
    catatan_singkat = st.pills("Aktivitas baru yang kamu lakuin?", [
        "Cuma Bertahan", "Rawat Diri", "Ngulik Hobi", "Ketemu Teman", "Fokus Kerja", "Mulai Berdamai"
    ], default="Cuma Bertahan")
    
    if st.button("Simpan Jejak Hari Ini"):
        if skala_likert:
            skor_final = {"😢 Terhimpit": 1, "🙁 Terbatas": 2, "😐 Menengah": 3, "🙂 Meluas": 4, "😄 Bertumbuh": 5}[skala_likert]
            upsert_jurnal(nama_pengguna, tgl_input, skor_pertumbuhan=skor_final, catatan=catatan_singkat)
            get_user_data.clear() 
            
            st.session_state['notif_jejak'] = True
            st.rerun()
        else:
            st.warning("Pilih skala pertumbuhannya dulu ya.")

    if 'notif_jejak' in st.session_state:
        st.success("Jejaknya udah kesimpan aman di Cloud!")
        del st.session_state['notif_jejak']

with col_graph:
    df_plot = df_jurnal.dropna(subset=['skor_pertumbuhan']).copy()
    if not df_plot.empty:
        fig = px.line(df_plot, x="tanggal", y="skor_pertumbuhan", custom_data=['catatan'], markers=True, height=300)
        
        if len(df_plot) == 1:
            s_date = df_plot['tanggal'].iloc[0]
            fig.update_xaxes(range=[s_date - pd.Timedelta(days=1), s_date + pd.Timedelta(days=1)])
            
        fig.update_traces(
            line_color="#0D9488", 
            line_width=4, 
            line_shape='spline', 
            marker=dict(size=12, color="#0F172A", symbol="circle", line=dict(width=2, color="#FFFFFF")),
            fill='tozeroy', 
            fillcolor="rgba(13, 148, 136, 0.1)",
            hovertemplate="<b>Skor:</b> %{y}/5<br><b>Aktivitas:</b> %{customdata[0]}<extra></extra>"
        )
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)", 
            hovermode="x unified",
            yaxis=dict(
                range=[0, 5.5], 
                tickvals=[1, 2, 3, 4, 5], 
                ticktext=["(1) Terhimpit", "(2) Terbatas", "(3) Menengah", "(4) Meluas", "(5) Bertumbuh"],
                title="", showgrid=True, gridcolor="#F1F5F9"
            ),
            xaxis=dict(
                title="", showgrid=False, tickformat="%d %b"
            ),
            margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Visualisasinya bakal muncul kalau kamu udah masukin data pertumbuhan.")

# --- PEMBATAS VISUAL 2 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Intip kesimpulan buat kamu hari ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 3: PANEL KESIMPULAN & SARAN
# ==========================================
st.markdown("<h2>3. Insight & Teman Melangkah</h2>", unsafe_allow_html=True)

if fase_saat_ini == "Baru Mulai Melangkah" or df_plot.empty:
    st.info("Isi dulu asesmen di Blok 1 dan simpan jejak di Blok 2 ya, biar sistem bisa buatin rangkuman dan langkah kecil yang pas buat kondisi kamu sekarang.")
else:
    col_summary_data, col_summary_insight = st.columns([1.2, 2.3], gap="large")
    
    with col_summary_data:
        st.markdown("<p style='font-size:12px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;'>📋 Rekap Perjalananmu</p>", unsafe_allow_html=True)
        total_hari = len(df_plot)
        avg_score = df_plot['skor_pertumbuhan'].mean()
        
        st.metric(label="Udah Bertahan Selama", value=f"{total_hari} Hari")
        st.write("")
        st.metric(label="Indeks Rata-rata Kapasitas", value=f"{avg_score:.1f} / 5.0")
        
    with col_summary_insight:
        st.markdown("<p style='font-size:12px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;'>💡 Catatan Buat Kamu</p>", unsafe_allow_html=True)
        
        if avg_score < 3.0:
            st.markdown(f"<div class='insight-box-warning'><b>Hasil Analisis:</b> Fase kamu secara rata-rata ada di <b>{fase_saat_ini}</b>. Wajar banget kalau lagi ngerasa mentok atau berat. Mengacu ke konsep <i>Self-Compassion</i> Dr. Kristin Neff, ini sama sekali bukan kegagalan. Tubuh dan pikiranmu cuma lagi ngasih alarm buat minta istirahat ekstra. Nggak perlu nyalahin diri sendiri, <i>take your time</i> aja.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='insight-box'><b>Hasil Analisis:</b> Keren banget, kapasitas hidupmu lagi lumayan stabil dan ada di <b>{fase_saat_ini}</b>. Mengacu ke teori Dr. Lois Tonkin, kamu udah ngebuktiin kalau kamu pelan-pelan bisa ngebangun sirkuit memori baru yang lebih luas dari rasa sedih itu. Lanjutin terus dengan ritme yang paling bikin kamu nyaman ya.</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:12px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-top:25px; margin-bottom:10px;'>🎯 Langkah Kecil Hari Ini</p>", unsafe_allow_html=True)
        
        if "Fokus" in fase_saat_ini: 
            st.checkbox("🌬️ Latihan **Box Breathing** yuk: Tarik napas 4s, tahan 4s, buang perlahan 4s. Lakuin 2 menit aja buat nenangin deg-degan.")
            st.checkbox("💧 Ambil segelas air putih sekarang dan minum pelan-pelan sampai habis.")
            st.checkbox("🛡️ Nggak apa-apa banget kalau hari ini ngerasa nggak produktif. Kasih izin buat dirimu istirahat.")
        elif "Adaptasi" in fase_saat_ini: 
            st.checkbox("☀️ Berdiri di teras atau dekat jendela pas pagi, kena sinar matahari 10 menit aja biar hormon bahagia naik.")
            st.checkbox("🎯 Beresin satu hal super gampang hari ini (misal: cuma ngerapiin meja kerja).")
            st.checkbox("✍️ Keluarin emosimu di 'Ruang Tumpah Rasa' di bawah.")
        elif "Seimbang" in fase_saat_ini: 
            st.checkbox("🧩 Pakai teknik **5-4-3-2-1**: Sebutkan 5 hal yang dilihat, 4 disentuh, 3 didengar, 2 dicium baunya, dan 1 hal baik tentangmu.")
            st.checkbox("🚫 Kurangin kepo atau *scroll* sosmed yang bisa mancing pikiran lama buat sisa hari ini.")
            st.checkbox("🏃 Jalan kaki santai 15 menit biar stres di otot berkurang.")
        else: 
            st.checkbox("🌱 Bikin satu kebiasaan pagi yang baru banget, yang sama sekali nggak ngingetin kamu sama masa lalu.")
            st.checkbox("🎨 Kasih waktu 30 menit buat ngulik hobi baru yang seru.")
            st.checkbox("🤝 Ngobrol ringan sama temen, bahas hal-hal *random*.")

# --- PEMBATAS VISUAL 3 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Tumpahin semuanya di bawah</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 4: RUANG TUMPAH RASA (EXPRESSIVE WRITING)
# ==========================================
st.markdown("<h2>4. Ruang Tumpah Rasa</h2>", unsafe_allow_html=True)
st.write("Nggak usah mikirin ejaan atau tanda baca. Tumpahin aja semua yang lagi menuhin kepala kamu di sini, tanpa perlu disensor.")

with st.form("ruang_tumpah_rasa_form", clear_on_submit=True):
    j_text = st.text_area("Tumpahkan di sini...", height=150, label_visibility="collapsed", placeholder="Ketik apa aja di sini, bebas...")
    submit_cerita = st.form_submit_button("Udah, Lumayan Lega")

if submit_cerita:
    if j_text: 
        upsert_jurnal(nama_pengguna, hari_ini, jurnal=j_text)
        get_user_data.clear() 
        
        st.session_state['notif_jurnal'] = True
        st.rerun()

if 'notif_jurnal' in st.session_state:
    st.success("Tumpahan rasamu udah diterima dan dikunci di Cloud. Secara ilmiah, mindahin uneg-uneg lewat tulisan bikin otak logis kamu kerja lebih enteng.")
    st.balloons()
    del st.session_state['notif_jurnal']

# ==========================================
# FOOTER & COMPLIANCE
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.markdown("---")
with st.expander("ℹ️ Tentang Rekarasa, Info Ilmiah & Bantuan Psikolog"):
    st.markdown("""
    **Tentang Rekarasa**
    Rekarasa adalah *tools* mandiri buat ngebantu kamu mantau proses perluasan kapasitas hidup. Penting diingat, aplikasi ini **bukan pengganti** sesi ngobrol langsung sama psikolog atau psikiater klinis ya.

    **🚨 Kapan Waktunya Cari Bantuan Profesional?**
    Sangat disarankan buat langsung janjian sama ahli kalau kamu ngerasa:
    * **Kegiatan Sehari-hari Terbengkalai:** Kesulitan banget buat tidur, makan, atau kerja secara normal selama lebih dari 2 minggu.
    * **Pikiran Berbahaya:** Mulai muncul keinginan buat nyakitin diri sendiri.
    * **Pelarian Ekstrem:** Mulai bergantung sama zat adiktif.
    
    *(Hubungi layanan kesehatan mental terdekat atau telepon ke **119 ekstensi 8** - Layanan Sejiwa Kemenkes RI).*

    ---
    **Literatur Riset & Teori Faktual:**
    * **WHO-5 Well-Being Index (1998):** Kuesioner global dari WHO untuk mengukur kesejahteraan subjektif.
    * **Model *Growing Around Grief* (Dr. Lois Tonkin, 1996):** Arsitektur utama aplikasi.
    * **Aktivasi Perilaku (Peter Lewinsohn, 1974):** Teori CBT yang mendasari dasbor Jejak Langkah.
    * **Konsep *Self-Compassion* (Dr. Kristin Neff):** Dasar analitik tidak menghakimi.
    * **Paradigma *Expressive Writing* (Dr. James W. Pennebaker, 1997):** Landasan 'Ruang Tumpah Rasa'.
    """)
    st.caption("© 2026 Rekarasa. Didesain dengan mengedepankan keamanan privasi, kepatuhan etika, dan integritas data ilmiah.")
