import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN & ADVANCED CSS
# ==========================================
st.set_page_config(
    page_title="Rekarasa | Teman Tumbuhmu", 
    page_icon="🌱", 
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F8FAFC; } 

    /* Metric Card Customization */
    [data-testid="stMetricValue"] > div {
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.2 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.5px;
    }
    [data-testid="stMetricLabel"] > div { 
        color: #64748B !important; 
        font-size: 0.8rem !important; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 1.2rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #10B981;
    }

    /* On-Screen Report Box Styles */
    .insight-box {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: #166534;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .insight-box-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: #92400E;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Tipografi Utama */
    .hero-title { color: #0F172A; font-weight: 800; font-size: 3rem; letter-spacing: -1.5px; margin-bottom: 0.5rem; }
    .hero-subtitle { color: #64748B; line-height: 1.6; font-size: 1.1rem; max-width: 90%; }
    h2 { color: #0F172A; font-weight: 700 !important; font-size: 1.6rem; border-bottom: 1.5px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 25px;}
    
    /* Buttons Customization */
    .stButton>button { 
        background-color: #0F172A; 
        color: white; 
        border-radius: 10px; 
        padding: 0.6rem 2rem; 
        border: none; 
        font-weight: 600; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #10B981; color: white; }
    
    /* Input & Forms */
    div[role="radiogroup"] { background: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;}
    .question-text { font-weight: 600; color: #0F172A; font-size: 1rem; margin-bottom: 5px; }
    
    .scroll-hint { text-align: center; color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-top: 15px; margin-bottom: 60px; text-transform: uppercase; letter-spacing: 1px; }
    .spacer-top { margin-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE MANAGEMENT 
# ==========================================
if 'status_pertumbuhan' not in st.session_state:
    st.session_state.status_pertumbuhan = "Baru Mulai Melangkah"
if 'database_pertumbuhan' not in st.session_state:
    st.session_state.database_pertumbuhan = pd.DataFrame(columns=["Tanggal", "Skor Pertumbuhan", "Catatan"])

# ==========================================
# 3. HEADER PLATFORM
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
col_title, col_metric = st.columns([2.5, 1.2])

with col_title:
    st.markdown('<div class="hero-title">Rekarasa <span style="color:#10B981">🌱</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Berdasarkan model <b>Growing Around Grief</b>. Nggak usah maksain rasa sedihnya cepet hilang. Kita cuma perlu pelan-pelan ngeluasin ruang hidupmu buat nampung itu semua.</div>', unsafe_allow_html=True)

with col_metric:
    metrik_status = st.empty()
    metrik_status.metric(label="Fase Hidupmu Saat Ini", value=st.session_state.status_pertumbuhan)

st.markdown("<br><hr><div class='spacer-top'></div>", unsafe_allow_html=True)


# ==========================================
# BLOK 1: ASESMEN (WHO-5 WELL-BEING INDEX)
# ==========================================
st.markdown("<h2>1. Cek Ruang Kapasitas (WHO-5 Index)</h2>", unsafe_allow_html=True)
st.write("Biar sistem bisa ngasih saran yang paling akurat, kita pakai standar kuesioner kesehatan mental global. Nggak ada jawaban yang salah kok, pilih aja yang paling kerasa sama kamu **beberapa hari terakhir ini** ya.")

opsi_skala = ["(1) Hampir nggak pernah", "(2) Jarang", "(3) Kadang-kadang", "(4) Sering", "(5) Hampir selalu"]

with st.form("asesmen_who5"):
    st.markdown("<div class='question-text'>1. Aku ngerasa ceria dan mood lagi lumayan bagus.</div>", unsafe_allow_html=True)
    q1 = st.radio("q1", opsi_skala, horizontal=True, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>2. Aku ngerasa lebih tenang dan rileks.</div>", unsafe_allow_html=True)
    q2 = st.radio("q2", opsi_skala, horizontal=True, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>3. Aku ngerasa aktif dan mau gerak.</div>", unsafe_allow_html=True)
    q3 = st.radio("q3", opsi_skala, horizontal=True, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>4. Pas bangun tidur, aku ngerasa seger (nggak ngerasa capek banget).</div>", unsafe_allow_html=True)
    q4 = st.radio("q4", opsi_skala, horizontal=True, label_visibility="collapsed", index=None)
    
    st.markdown("<div class='question-text'>5. Keseharianku kerasa ada aja hal yang menarik atau seru.</div>", unsafe_allow_html=True)
    q5 = st.radio("q5", opsi_skala, horizontal=True, label_visibility="collapsed", index=None)
    
    submit_asesmen = st.form_submit_button("Analisis Fase Hidupku")

if submit_asesmen:
    if all([q1, q2, q3, q4, q5]):
        # Ekstrak angka dengan aman menggunakan split
        def ambil_skor(teks):
            return int(teks.split(')')[0].replace('(', ''))
            
        skor_total = ambil_skor(q1) + ambil_skor(q2) + ambil_skor(q3) + ambil_skor(q4) + ambil_skor(q5)
        
        # Mapping Skor WHO-5 (Min 5, Max 25) ke 5 Fase Rekarasa
        if skor_total <= 8: fase_baru = "Fokus Bertahan Diri"
        elif skor_total <= 12: fase_baru = "Mulai Beradaptasi"
        elif skor_total <= 16: fase_baru = "Pertumbuhan Seimbang"
        elif skor_total <= 20: fase_baru = "Ekspansi Kehidupan"
        else: fase_baru = "Kapasitas Hidup Luas"
        
        st.session_state.status_pertumbuhan = fase_baru
        metrik_status.metric(label="Fase Hidupmu Saat Ini", value=st.session_state.status_pertumbuhan)
        st.success(f"Dicatat ya! Berdasarkan analisis, fase kamu sekarang ada di: **{st.session_state.status_pertumbuhan}**.")
    else:
        st.warning("Eits, sepertinya ada pertanyaan yang belum keisi. Dilengkapin dulu yuk!")

# --- PEMBATAS VISUAL 1 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Cek seberapa jauh kamu udah jalan di bawah ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 2: JEJAK LANGKAH 
# ==========================================
st.markdown("<h2>2. Jejak Langkahmu</h2>", unsafe_allow_html=True)
st.write("Grafik ini bukan buat ngukur kesedihan, tapi ngeliat seberapa jauh **Ruang Hidupmu** udah bertumbuh dari hari ke hari.")

col_input, col_graph = st.columns([1, 2], gap="large")
with col_input:
    tgl = st.date_input("Pilih Tanggal (Bisa ubah tanggal buat cek mundur)", datetime.date.today())
    skala_likert = st.radio("Seberapa luas ruang hidupmu hari ini?", ["😢 Terhimpit", "🙁 Terbatas", "😐 Menengah", "🙂 Meluas", "😄 Bertumbuh"], horizontal=True, index=None)
    catatan_singkat = st.selectbox("Ada aktivitas baru yang kamu lakuin?", ["Nggak ngapa-ngapain, cuma bertahan", "Rawat Diri (Skincare/Mandi air hangat)", "Mulai ngulik hobi", "Nongkrong/Ketemu Teman", "Fokus Kerja", "Mulai pelan-pelan berdamai"])
    
    if st.button("Simpan Jejak Hari Ini"):
        if skala_likert:
            skor_final = {"😢 Terhimpit": 1, "🙁 Terbatas": 2, "😐 Menengah": 3, "🙂 Meluas": 4, "😄 Bertumbuh": 5}[skala_likert]
            new_data = pd.DataFrame({"Tanggal": [pd.to_datetime(tgl)], "Skor Pertumbuhan": [skor_final], "Catatan": [catatan_singkat]})
            
            # BUG FIX: Menggunakan keep='last' agar jika user salah input di hari yang sama, data bisa ditimpa.
            st.session_state.database_pertumbuhan = pd.concat([st.session_state.database_pertumbuhan, new_data]).drop_duplicates(subset=['Tanggal'], keep='last').sort_values('Tanggal')
            
            st.success("Jejaknya udah kesimpan aman!")
        else:
            st.warning("Pilih skala pertumbuhannya dulu ya.")

with col_graph:
    if not st.session_state.database_pertumbuhan.empty:
        df_plot = st.session_state.database_pertumbuhan.copy()
        fig = px.line(df_plot, x="Tanggal", y="Skor Pertumbuhan", text="Catatan", markers=True, height=340)
        
        # BUG FIX: Mencegah grafik error/zooming aneh kalau data baru 1 hari
        if len(df_plot) == 1:
            s_date = df_plot['Tanggal'].iloc[0]
            fig.update_xaxes(range=[s_date - pd.Timedelta(days=1), s_date + pd.Timedelta(days=1)])
            
        fig.update_traces(line_color="#E2E8F0", line_width=3, line_shape='spline', marker=dict(size=14, color="#10B981"), textposition="top center", textfont=dict(color="#475569", size=11, family='Inter'))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", yaxis=dict(range=[0.5, 5.5], tickvals=[1, 2, 3, 4, 5], ticktext=["Terhimpit", "Terbatas", "Menengah", "Meluas", "Bertumbuh"]), margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Visualisasinya bakal muncul kalau kamu udah masukin data hari ini.")

# --- PEMBATAS VISUAL 2 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Tarik napas sebentar, yuk intip kesimpulan buat kamu hari ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 3: PANEL KESIMPULAN & SARAN
# ==========================================
st.markdown("<h2>3. Insight & Teman Melangkah</h2>", unsafe_allow_html=True)
stat_p = st.session_state.status_pertumbuhan

if stat_p == "Baru Mulai Melangkah" or st.session_state.database_pertumbuhan.empty:
    st.info("Isi dulu asesmen di Blok 1 dan simpan jejak di Blok 2 ya, biar sistem bisa buatin rangkuman dan langkah kecil yang pas buat kondisi kamu sekarang.")
else:
    col_summary_data, col_summary_insight = st.columns([1.2, 2.3], gap="large")
    
    with col_summary_data:
        st.markdown("<p style='font-size:13px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>📋 Rekap Perjalananmu</p>", unsafe_allow_html=True)
        total_hari = len(st.session_state.database_pertumbuhan)
        avg_score = st.session_state.database_pertumbuhan['Skor Pertumbuhan'].mean()
        
        st.metric(label="Udah Bertahan Selama", value=f"{total_hari} Hari")
        st.write("")
        st.metric(label="Indeks Rata-rata Kapasitas", value=f"{avg_score:.1f} / 5.0")
        
    with col_summary_insight:
        st.markdown("<p style='font-size:13px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>💡 Catatan Buat Kamu</p>", unsafe_allow_html=True)
        
        if avg_score < 3.0:
            st.markdown(f"<div class='insight-box-warning'><b>Hasil Analisis:</b> Fase kamu secara rata-rata ada di <b>{stat_p}</b>. Wajar banget kalau lagi ngerasa mentok atau berat. Mengacu ke konsep <i>Self-Compassion</i> Dr. Kristin Neff, ini sama sekali bukan kegagalan. Tubuh dan pikiranmu cuma lagi ngasih alarm buat minta istirahat ekstra. Nggak perlu nyalahin diri sendiri, <i>take your time</i> aja.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='insight-box'><b>Hasil Analisis:</b> Keren banget, kapasitas hidupmu lagi lumayan stabil dan ada di <b>{stat_p}</b>. Mengacu ke teori Dr. Lois Tonkin, kamu udah ngebuktiin kalau kamu pelan-pelan bisa ngebangun sirkuit memori baru yang lebih luas dari rasa sedih itu. Lanjutin terus dengan ritme yang paling bikin kamu nyaman ya.</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:13px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-top:20px; margin-bottom:10px;'>🎯 Langkah Kecil yang Bisa Dicoba Hari Ini</p>", unsafe_allow_html=True)
        
        if "Fokus" in stat_p: 
            st.checkbox("🌬️ Latihan **Box Breathing** yuk: Tarik napas 4 detik, tahan 4 detik, buang perlahan 4 detik. Lakuin 2 menit aja buat nenangin deg-degan.")
            st.checkbox("💧 Ambil segelas air putih sekarang dan minum pelan-pelan sampai habis. Bantu tubuhmu tetep seger.")
            st.checkbox("🛡️ Nggak apa-apa banget kalau hari ini ngerasa nggak produktif. Kasih izin buat dirimu istirahat, kamu udah berusaha keras kok.")
        elif "Adaptasi" in stat_p: 
            st.checkbox("☀️ Coba berdiri di teras atau dekat jendela pas pagi, kena sinar matahari 10 menit aja biar hormon bahagia (*serotonin*) naik.")
            st.checkbox("🎯 Beresin satu hal super gampang hari ini (misal: cuma ngerapiin meja kerja atau bersihin layar tablet).")
            st.checkbox("✍️ Kalau masih ada yang ganjel, keluarin aja semuanya di 'Ruang Tumpah Rasa' di bawah.")
        elif "Seimbang" in stat_p: 
            st.checkbox("🧩 Pakai teknik **5-4-3-2-1** kalau tiba-tiba kepikiran masa lalu: Cari 5 benda di sekitar yang bisa dilihat, 4 yang bisa disentuh.")
            st.checkbox("🚫 Kurangin kepo atau *scroll* sosmed yang bisa mancing pikiran lama buat sisa hari ini.")
            st.checkbox("🏃 Jalan kaki santai 15 menit, entah di komplek atau keliling kantor, biar stres di otot berkurang.")
        else: 
            st.checkbox("🌱 Bikin satu kebiasaan pagi yang baru banget, yang sama sekali nggak ngingetin kamu sama masa lalu.")
            st.checkbox("🎨 Kasih waktu 30 menit buat ngulik hobi, *coding* Python, atau hal seru yang udah lama pengen kamu coba.")
            st.checkbox("🤝 Coba ngobrol ringan sama temen kantor, bahas hal-hal *random* yang nggak ngebahas masalah personal.")

# --- PEMBATAS VISUAL 3 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Tumpahin semuanya di bawah, biar kepalamu lebih enteng</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 4: RUANG TUMPAH RASA
# ==========================================
st.markdown("<h2>4. Ruang Tumpah Rasa</h2>", unsafe_allow_html=True)
st.write("Nggak usah mikirin ejaan atau tanda baca. Tumpahin aja semua yang lagi menuhin kepala kamu di sini, tanpa perlu disensor.")
j_text = st.text_area("Tumpahkan di sini...", height=150, label_visibility="collapsed", placeholder="Ketik apa aja di sini, bebas...")

if st.button("Udah, Lumayan Lega"):
    if j_text: 
        st.success("Tumpahan rasamu udah diterima dengan aman. Secara ilmiah, mindahin uneg-uneg lewat tulisan bikin otak logis kamu kerja lebih enteng.")
        st.balloons()

# ==========================================
# FOOTER & COMPLIANCE (INFO ILMIAH)
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.markdown("---")
with st.expander("ℹ️ Tentang Rekarasa, Info Ilmiah & Bantuan Psikolog"):
    st.markdown("""
    **Tentang Rekarasa**
    Rekarasa adalah *tools* mandiri buat ngebantu kamu mantau proses perluasan kapasitas hidup. Penting diingat, aplikasi ini **bukan pengganti** sesi ngobrol langsung sama psikolog atau psikiater klinis ya.

    **🚨 Kapan Waktunya Cari Bantuan Profesional?**
    Pemulihan mandiri itu ada batasannya. Sangat disarankan buat langsung janjian sama ahli kalau kamu ngerasa:
    * **Kegiatan Sehari-hari Terbengkalai:** Kesulitan banget buat tidur, makan, atau kerja secara normal selama lebih dari 2 minggu berturut-turut.
    * **Pikiran Berbahaya:** Mulai muncul keinginan atau ngerencanain hal buat nyakitin diri sendiri.
    * **Pelarian Ekstrem:** Mulai bergantung banget sama alkohol, obat-obatan tanpa resep, atau zat adiktif lainnya.
    
    *(Kalau kamu ngerasa udah di titik yang bener-bener krisis, tolong jangan ragu buat hubungi layanan kesehatan mental terdekat atau telepon ke **119 ekstensi 8** - Layanan Sejiwa Kemenkes RI).*

    ---

    **Berdasarkan Literatur Riset & Teori Faktual:**
    * **WHO-5 Well-Being Index (1998):** Instrumen validasi global dari Organisasi Kesehatan Dunia yang dirancang khusus untuk mengukur kesejahteraan subjektif dan kualitas hidup secara positif.
    * **Model *Growing Around Grief* (Dr. Lois Tonkin, 1996):** Teori inti yang memvalidasi bahwa pemulihan sejati terjadi dengan memperluas dimensi hidup mengelilingi duka, bukan memaksanya hilang.
    * **Konsep *Self-Compassion* (Dr. Kristin Neff):** Dasar penyusunan laporan analitik yang tidak menghakimi (*non-judgmental*), terbukti secara klinis memotong rantai kritik diri (*self-criticism*).
    * **Paradigma *Expressive Writing* (Dr. James W. Pennebaker, 1997):** Landasan neuropsikologis 'Ruang Tumpah Rasa' yang terbukti mampu memindahkan muatan stres dari amigdala menuju korteks prefrontal.
    * **Regulasi Sistem Saraf (*Box Breathing*):** Latihan pernapasan taktis untuk menurunkan lonjakan kortisol (Riset Dr. Richard Brown & Dr. Patricia Gerbarg).
    * **Protokol *Sensory Grounding* 5-4-3-2-1:** Teknik kesadaran indrawi dari Cognitive Behavioral Therapy (CBT) untuk mengembalikan kendali logika saat kepanikan menyerang.
    """)
    st.caption("© 2026 Rekarasa. Didesain dengan mengedepankan keamanan privasi, kepatuhan etika, dan integritas data ilmiah.")
