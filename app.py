import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN & ADVANCED CSS (SaaS Polish)
# ==========================================
st.set_page_config(
    page_title="Rekarasa | Growing Around Grief", 
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

    /* On-Screen Report Box Styles (Tidak Menghakimi) */
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
    
    div[role="radiogroup"] { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .scroll-hint { text-align: center; color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-top: 15px; margin-bottom: 60px; text-transform: uppercase; letter-spacing: 1px; }
    .spacer-top { margin-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE MANAGEMENT (LOGIKA LOIS TONKIN)
# ==========================================
if 'status_pertumbuhan' not in st.session_state:
    st.session_state.status_pertumbuhan = "Memulai Perjalanan"
if 'database_pertumbuhan' not in st.session_state:
    st.session_state.database_pertumbuhan = pd.DataFrame(columns=["Tanggal", "Skor Pertumbuhan", "Catatan"])

# ==========================================
# 3. HEADER PLATFORM
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
col_title, col_metric = st.columns([2.5, 1.2])

with col_title:
    st.markdown('<div class="hero-title">Rekarasa <span style="color:#10B981">🌱</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Berdasarkan model <b>Growing Around Grief</b>. Kita tidak fokus mengecilkan duka, namun memperluas kapasitas hidup untuk menampungnya.</div>', unsafe_allow_html=True)

with col_metric:
    metrik_status = st.empty()
    metrik_status.metric(label="Kapasitas Hidup Saat Ini", value=st.session_state.status_pertumbuhan)

st.markdown("<br><hr><div class='spacer-top'></div>", unsafe_allow_html=True)


# ==========================================
# BLOK 1: APA RASA BERUKIR HARI INI? (Asesmen)
# ==========================================
st.markdown("<h2>1. Apa Rasa Berukir Hari Ini?</h2>", unsafe_allow_html=True)
pilihan_kondisi = st.radio("Seberapa besar hidupmu mengitari duka hari ini?", [
    "Duka terasa mengambil seluruh ruang hidup saya. Sulit untuk memikirkan hal lain.",
    "Hidup saya masih didominasi duka, tapi saya mulai bisa melakukan beberapa tugas kecil.",
    "Ada keseimbangan. Saya merasa sedih, tapi saya juga mulai bisa merancang rencana masa depan.",
    "Saya sudah mulai aktif melakukan hal-hal baru, meski sesekali rasa duka tetap muncul menyapa.",
    "Hidup saya sudah tumbuh jauh lebih besar. Rasa duka itu tetap ada, tapi ia hanya menjadi bagian kecil dari hidup saya."
], index=None, label_visibility="collapsed")

if st.button("Catat Kapasitas Hidupku"):
    if pilihan_kondisi:
        mapping = {
            "Duka terasa mengambil seluruh ruang hidup saya. Sulit untuk memikirkan hal lain.": "Fokus Bertahan Diri",
            "Hidup saya masih didominasi duka, tapi saya mulai bisa melakukan beberapa tugas kecil.": "Mulai Beradaptasi",
            "Ada keseimbangan. Saya merasa sedih, tapi saya juga mulai bisa merancang rencana masa depan.": "Pertumbuhan Seimbang",
            "Saya sudah mulai aktif melakukan hal-hal baru, meski sesekali rasa duka tetap muncul menyapa.": "Ekspansi Kehidupan",
            "Hidup saya sudah tumbuh jauh lebih besar. Rasa duka itu tetap ada, tapi ia hanya menjadi bagian kecil dari hidup saya.": "Kapasitas Hidup Luas"
        }
        st.session_state.status_pertumbuhan = mapping[pilihan_kondisi]
        metrik_status.metric(label="Kapasitas Hidup Saat Ini", value=st.session_state.status_pertumbuhan)
        st.success(f"Status tercatat: **{st.session_state.status_pertumbuhan}**.")

# --- PEMBATAS VISUAL 1 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Periksa visualisasi jejak langkahmu di bawah ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 2: JEJAK LANGKAH (Progress Dashboard)
# ==========================================
st.markdown("<h2>2. Jejak Langkahmu</h2>", unsafe_allow_html=True)
st.write("Grafik ini melacak seberapa besar **Kapasitas Hidup** yang berhasil kamu bangun setiap harinya.")

col_input, col_graph = st.columns([1, 2], gap="large")
with col_input:
    tgl = st.date_input("Tanggal", datetime.date.today())
    skala_likert = st.radio("Skala Pertumbuhan", ["😢 Terhimpit", "🙁 Terbatas", "😐 Menengah", "🙂 Meluas", "😄 Bertumbuh"], horizontal=True, index=None)
    catatan_singkat = st.selectbox("Aktivitas baru:", ["Rawat Diri", "Mulai Hobi", "Bertemu Teman", "Kerja Fokus", "Hanya Bertahan", "Mulai Berdamai"])
    if st.button("Simpan Jejak"):
        if skala_likert:
            skor_final = {"😢 Terhimpit": 1, "🙁 Terbatas": 2, "😐 Menengah": 3, "🙂 Meluas": 4, "😄 Bertumbuh": 5}[skala_likert]
            new_data = pd.DataFrame({"Tanggal": [pd.to_datetime(tgl)], "Skor Pertumbuhan": [skor_final], "Catatan": [catatan_singkat]})
            st.session_state.database_pertumbuhan = pd.concat([st.session_state.database_pertumbuhan, new_data]).drop_duplicates('Tanggal').sort_values('Tanggal')
            st.success("Jejak pertumbuhan berhasil disimpan!")

with col_graph:
    if not st.session_state.database_pertumbuhan.empty:
        fig = px.line(st.session_state.database_pertumbuhan, x="Tanggal", y="Skor Pertumbuhan", text="Catatan", markers=True, height=340)
        fig.update_traces(line_color="#E2E8F0", line_width=3, line_shape='spline', marker=dict(size=14, color="#10B981"), textposition="top center", textfont=dict(color="#475569", size=11, family='Inter'))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", yaxis=dict(range=[0.5, 5.5], tickvals=[1, 2, 3, 4, 5], ticktext=["Terhimpit", "Terbatas", "Menengah", "Meluas", "Bertumbuh"]), margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dasbor pertumbuhan akan muncul setelah Anda mencatat data hari ini.")

# --- PEMBATAS VISUAL 2 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Lihat kesimpulan panel laporan on-screen di bawah ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 3: PANEL KESIMPULAN, HASIL & SARAN (ON-SCREEN REPORT)
# ==========================================
st.markdown("<h2>3. Panel Kesimpulan, Hasil & Saran</h2>", unsafe_allow_html=True)
stat_p = st.session_state.status_pertumbuhan

if stat_p == "Memulai Perjalanan" or st.session_state.database_pertumbuhan.empty:
    st.info("Silakan isi bagian Asesmen (Blok 1) dan simpan minimal satu Jejak Langkah (Blok 2) untuk merumuskan panel kesimpulan secara otomatis di sini.")
else:
    # Memisahkan layout menjadi komparasi data eksekutif & refleksi sains
    col_summary_data, col_summary_insight = st.columns([1.2, 2.3], gap="large")
    
    with col_summary_data:
        st.markdown("<p style='font-size:13px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>📋 Kesimpulan Metrik Data</p>", unsafe_allow_html=True)
        total_hari = len(st.session_state.database_pertumbuhan)
        avg_score = st.session_state.database_pertumbuhan['Skor Pertumbuhan'].mean()
        
        st.metric(label="Total Hari yang Berhasil Dilalui", value=f"{total_hari} Hari")
        st.write("")
        st.metric(label="Indeks Rata-rata Kapasitas", value=f"{avg_score:.1f} / 5.0")
        
    with col_summary_insight:
        st.markdown("<p style='font-size:13px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>💡 Hasil Analisis Welas Asih</p>", unsafe_allow_html=True)
        
        # HASIL: Sintesis otomatis berbasis rata-rata metrik (Teori Kristin Neff)
        if avg_score < 3:
            st.markdown(f"<div class='insight-box-warning'><b>Hasil Refleksi:</b> Saat ini kapasitas ruang hidupmu berada di fase <b>{stat_p}</b>. Berdasarkan prinsip <i>Self-Compassion</i> Dr. Kristin Neff, merasa terhimpit atau stagnan bukanlah bentuk kegagalan. Ini adalah indikator biologis yang valid bahwa tubuhmu sedang memerlukan proteksi, penerimaan utuh, dan istirahat kognitif yang mendalam tanpa penghakiman.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='insight-box'><b>Hasil Refleksi:</b> Analisis data mendeteksi kestabilan yang baik di fase <b>{stat_p}</b>. Mengacu pada paradigma Dr. Lois Tonkin, kamu telah berhasil mengukir sirkuit memori baru untuk memperluas ruang hidupmu mengitari memori duka tersebut. Teruskan dengan ritme yang paling nyaman bagi jiwamu.</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:13px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-top:20px; margin-bottom:10px;'>🎯 Saran Rekomendasi Tindakan</p>", unsafe_allow_html=True)
        
        # SARAN: Checklist aksi berbasis sains taktis
        if "Fokus" in stat_p: 
            st.checkbox("🌬️ Lakukan **Box Breathing** (Tarik napas 4 detik, tahan 4 detik, buang 4 detik) selama 2 menit guna meredam over-aktivasi amigdala.")
            st.checkbox("💧 Penuhi kebutuhan hidrasi dengan meminum satu gelas air putih penuh secara sadar (*mindful drinking*).")
            st.checkbox("🛡️ Berikan afirmasi tertulis pada diri sendiri bahwa Anda diizinkan untuk tidak produktif hari ini.")
        elif "Adaptasi" in stat_p: 
            st.checkbox("☀️ Berdiri di ruang terbuka/bawah sinar matahari pagi selama 10 menit untuk menstimulasi produksi hormon serotonin.")
            st.checkbox("🎯 Selesaikan satu (1) tugas fisik mikro yang sangat mudah (misal: merapikan posisi bantal tidur).")
            st.checkbox("✍️ Tuangkan satu kata atau emosi yang paling membebanimu saat ini ke dalam Ruang Cerita di bawah.")
        elif "Seimbang" in stat_p: 
            st.checkbox("🧩 Gunakan teknik **Sensory Grounding 5-4-3-2-1** apabila memori masa lalu secara mendadak membajak kesadaranmu.")
            st.checkbox("🚫 Lakukan detoks informasi digital (hindari media sosial atau pemicu lama) selama sisa hari ini.")
            st.checkbox("🏃 Berjalan santai di sekitar area tinggal selama 15 menit untuk mengurai akumulasi hormon stres kortisol.")
        else: 
            st.checkbox("🌱 Bangun satu rutinitas pagi baru berskala kecil yang terbebas dari asosiasi atau memori masa lalu.")
            st.checkbox("🎨 Luangkan waktu 30 menit terisolasi untuk mengeksplorasi minat, hobi, atau karya baru yang tertunda.")
            st.checkbox("🤝 Jangkau satu kerabat dekat untuk berkomunikasi mengenai topik eksternal yang netral.")

# --- PEMBATAS VISUAL 3 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Gunakan ruang katarsis di bawah untuk melepaskan beban kognitif</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 4: RUANG CERITA
# ==========================================
st.markdown("<h2>4. Ruang Cerita (Katarsis)</h2>", unsafe_allow_html=True)
st.write("Duka tidak menuntut struktur kalimat. Tuliskan apa pun yang memenuhi pikiranmu saat ini tanpa sensor.")
j_text = st.text_area("Tumpahkan di sini...", height=150, label_visibility="collapsed", placeholder="Ketik secara bebas...")

if st.button("Selesai Menulis"):
    if j_text: 
        st.success("Tulisan Anda berhasil diproses secara mandiri. Beban memori kerja pada sistem saraf Anda kini telah dialihkan menuju wilayah otak logis.")
        st.balloons()

# ==========================================
# FOOTER & COMPLIANCE (INTEGRITAS SAINS)
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.markdown("---")
with st.expander("ℹ️ Tentang Rekarasa, Landasan Ilmiah & Bantuan Profesional"):
    st.markdown("""
    **Tentang Rekarasa**
    Rekarasa adalah platform analitik mandiri (*self-help*) yang dirancang khusus untuk memetakan pertumbuhan kapasitas hidup individu secara terukur. Platform ini **bukan pengganti** dari penanganan medis, konseling klinis, evaluasi psikiatris, maupun psikoterapi profesional.

    **🚨 Kapan Harus Menjangkau Bantuan Ahli Profesional?**
    Protokol pemulihan mandiri memiliki batasan klinis yang ketat. Anda sangat diimbau untuk segera menjangkau psikolog klinis atau psikiater apabila mendeteksi tanda-tanda krisis berikut:
    * **Disfungsi Aktivitas Harian:** Mengalami kelumpuhan fungsi sosial, penurunan nafsu makan drastis, insomnia parah, atau absen bekerja selama lebih dari 14 hari berturut-turut.
    * **Ideasi Destruktif:** Timbulnya dorongan, rencana, atau pikiran aktif untuk menyakiti diri sendiri maupun mengakhiri kehidupan.
    * **Koping Maladaptif:** Menggunakan zat adiktif, obat-obatan penenang tanpa resep, atau alkohol sebagai benteng pelarian emosi.
    
    *(Jika Anda berada dalam situasi krisis emosional akut, silakan hubungi pusat layanan darurat medis nasional atau Layanan Kesehatan Jiwa Kemenkes RI melalui saluran **119 ekstensi 8**).*

    ---

    **Sumber Literatur Riset & Teori Faktual:**
    * **Model *Growing Around Grief* (Dr. Lois Tonkin, 1996):** Teori inti yang mendasari algoritma visualisasi platform, memvalidasi fakta bahwa pemulihan sejati terjadi dengan memperluas dimensi kapasitas hidup, bukan mengecilkan esensi duka.
    * **Konsep *Self-Compassion* (Dr. Kristin Neff):** Dasar penyusunan teks analitik tidak menghakimi (*non-judgmental monitoring*) untuk memotong rantai kritik diri radikal (*self-criticism*) saat grafik metrik sedang menurun.
    * **Paradigma *Expressive Writing* (Dr. James W. Pennebaker, 1997):** Landasan neuropsikologis Blok Ruang Cerita yang terbukti memindahkan muatan emosi negatif dari amigdala menuju korteks prefrontal.
    * **Regulasi Sistem Saraf Parasimpatik (*Box Breathing*):** Latihan pernapasan taktis untuk stimulasi saraf vagus yang divalidasi klinis oleh Dr. Richard Brown dan Dr. Patricia Gerbarg.
    * **Protokol *Sensory Grounding* 5-4-3-2-1:** Teknik intervensi kecemasan berbasis kesadaran indrawi yang diadaptasi dari metode relaksasi klinis Betty Erickson untuk menangani pembajakan fungsi logis otak akibat kepanikan mendadak.
    """)
    st.caption("© 2026 Rekarasa. Beroperasi penuh dengan standar privasi lokal, kepatuhan sistem, dan integritas data ilmiah.")
