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

    /* Mencegah metrik terpotong (Metric Truncation Fix) */
    [data-testid="stMetricValue"] > div {
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.2 !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
    }
    [data-testid="stMetricLabel"] > div { color: #64748B !important; font-size: 0.85rem !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;}
    
    /* SaaS Card Dashboard Style */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 1.2rem !important;
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #10B981;
    }

    /* Tipografi & Layout Vertical Block */
    h1 { color: #0F172A; font-weight: 700 !important; letter-spacing: -1.2px; margin-bottom: 0rem; }
    h2 { color: #0F172A; font-weight: 700 !important; font-size: 1.6rem; border-bottom: 1.5px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 25px;}
    p { color: #475569; line-height: 1.7; font-size: 1.05rem; }
    
    /* Tombol Interaktif Premium */
    .stButton>button { 
        background-color: #0F172A; 
        color: white; 
        border-radius: 10px; 
        padding: 0.6rem 2rem; 
        border: none; 
        font-weight: 600; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #10B981; 
        color: white; 
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    /* Container untuk Blok Input */
    div[role="radiogroup"] { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    
    /* Indikator Navigasi Bawah */
    .scroll-hint {
        text-align: center;
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 60px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .spacer-top { margin-top: 3.5rem; }
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
header_col1, header_col2 = st.columns([2.2, 1.3])
with header_col1:
    st.title("Rekarasa 🌱")
    st.write("Sesuai teori **Growing Around Grief**, kita tidak perlu memaksa rasa duka mengecil. Kita hanya perlu membantu hidupmu tumbuh lebih besar mengitari rasa duka itu.")
with header_col2:
    # Menggunakan placeholder empty agar pembaruan status berjalan instan tanpa klik dua kali
    metrik_status = st.empty()
    metrik_status.metric(label="Kapasitas Hidup Saat Ini", value=st.session_state.status_pertumbuhan)

st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)


# ==========================================
# BLOK 1: APA RASAMU HARI INI? (Asesmen Tonkin)
# ==========================================
st.markdown("<h2>1. Apa Rasa Berukir Hari Ini?</h2>", unsafe_allow_html=True)
st.write("Mari petakan seberapa besar ruang duka memengaruhi hidupmu hari ini. Ingat, rasa duka yang besar tidak berarti kamu gagal.")

pilihan_kondisi = st.radio("Seberapa besar hidupmu mengitari duka hari ini?", [
    "Duka terasa mengambil seluruh ruang hidup saya. Sulit untuk memikirkan hal lain.",
    "Hidup saya masih didominasi duka, tapi saya mulai bisa melakukan beberapa tugas kecil.",
    "Ada keseimbangan. Saya merasa sedih, tapi saya juga mulai bisa merancang rencana masa depan.",
    "Saya sudah mulai aktif melakukan hal-hal baru, meski sesekali rasa duka tetap muncul menyapa.",
    "Hidup saya sudah tumbuh jauh lebih besar. Rasa duka itu tetap ada, tapi ia hanya menjadi bagian kecil dari hidup saya."
], index=None, label_visibility="collapsed")

if st.button("Catat Kapasitas Hidupku"):
    if pilihan_kondisi:
        if "seluruh ruang" in pilihan_kondisi: st.session_state.status_pertumbuhan = "Fokus Bertahan Diri"
        elif "tugas kecil" in pilihan_kondisi: st.session_state.status_pertumbuhan = "Mulai Beradaptasi"
        elif "keseimbangan" in pilihan_kondisi: st.session_state.status_pertumbuhan = "Pertumbuhan Seimbang"
        elif "aktif" in pilihan_kondisi: st.session_state.status_pertumbuhan = "Ekspansi Kehidupan"
        else: st.session_state.status_pertumbuhan = "Kapasitas Hidup Luas"
        
        # Mengubah tampilan bingkai metrik secara langsung ketika tombol ditekan
        metrik_status.metric(label="Kapasitas Hidup Saat Ini", value=st.session_state.status_pertumbuhan)
        st.success(f"Status tercatat: **{st.session_state.status_pertumbuhan}**. Kamu sedang belajar memperluas ruang hidupmu.")
    else:
        st.warning("Silakan pilih kondisi yang paling mewakilimu.")

# --- PEMBATAS VISUAL 1 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Lihat jejak pertumbuhanmu di bawah ini</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 2: JEJAK LANGKAH (Progress Dashboard)
# ==========================================
st.markdown("<h2>2. Jejak Langkahmu</h2>", unsafe_allow_html=True)
st.write("Grafik ini tidak melacak seberapa sedih dirimu, melainkan seberapa besar **Kapasitas Hidup** yang berhasil kamu bangun setiap harinya.")

col_input, col_graph = st.columns([1, 2], gap="large")

with col_input:
    tgl = st.date_input("Tanggal", datetime.date.today())
    
    st.markdown("<p style='font-size:14px; font-weight:600; margin-bottom:5px;'>Seberapa luas ruang hidupmu hari ini?</p>", unsafe_allow_html=True)
    skala_likert = st.radio(
        "Skala Pertumbuhan",
        options=["😢 Terhimpit", "🙁 Terbatas", "😐 Menengah", "🙂 Meluas", "😄 Bertumbuh"],
        horizontal=True, 
        label_visibility="collapsed",
        index=None
    )
    
    catatan_singkat = st.selectbox("Hal baru apa yang kamu lakukan?", ["Rawat Diri", "Mulai Hobi", "Bertemu Teman", "Kerja Fokus", "Hanya Bertahan", "Mulai Berdamai"])
    
    st.write("")
    if st.button("Simpan Jejak Pertumbuhan", use_container_width=True):
        if skala_likert:
            konv_skor = {"😢 Terhimpit": 1, "🙁 Terbatas": 2, "😐 Menengah": 3, "🙂 Meluas": 4, "😄 Bertumbuh": 5}
            skor_final = konv_skor[skala_likert]
            
            new_data = pd.DataFrame({"Tanggal": [pd.to_datetime(tgl)], "Skor Pertumbuhan": [skor_final], "Catatan": [catatan_singkat]})
            st.session_state.database_pertumbuhan = pd.concat([st.session_state.database_pertumbuhan, new_data]).drop_duplicates('Tanggal').sort_values('Tanggal')
            st.success("Jejak pertumbuhan berhasil disimpan!")
        else:
            st.warning("Pilih skala pertumbuhan terlebih dahulu.")

with col_graph:
    if not st.session_state.database_pertumbuhan.empty:
        df_p = st.session_state.database_pertumbuhan.copy()
        fig = px.line(df_p, x="Tanggal", y="Skor Pertumbuhan", text="Catatan", markers=True, height=340)
        
        if len(df_p) == 1:
            s_date = df_p['Tanggal'].iloc[0]
            fig.update_xaxes(range=[s_date - pd.Timedelta(days=1), s_date + pd.Timedelta(days=1)])
            
        fig.update_traces(
            line_color="#E2E8F0", line_width=3, line_shape='spline',
            marker=dict(size=14, color="#10B981", line=dict(width=3, color="white")), 
            textposition="top center", 
            textfont=dict(color="#475569", size=11, family='Inter')
        )
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=20, b=0),
            yaxis=dict(range=[0.5, 5.5], gridcolor="#F1F5F9", tickvals=[1, 2, 3, 4, 5], ticktext=["Terhimpit", "Terbatas", "Menengah", "Meluas", "Bertumbuh"], title=""),
            xaxis=dict(showgrid=False, tickformat="%d %b %Y", title="")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dasbor pertumbuhan akan muncul setelah Anda mencatat data hari ini.")

# --- PEMBATAS VISUAL 2 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Lanjut ke langkah pemulihanmu</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 3: LANGKAH KECIL (Intervensi Lois Tonkin)
# ==========================================
st.markdown("<h2>3. Langkah Kecil Hari Ini</h2>", unsafe_allow_html=True)
stat_p = st.session_state.status_pertumbuhan

if stat_p == "Memulai Perjalanan":
    st.warning("Silakan isi bagian 'Apa Rasa Berukir Hari Ini' agar kami bisa memberikan saran perluasan hidup yang tepat.")
else:
    st.write(f"Kapasitas hidupmu saat ini: **{stat_p}**. Mari coba langkah kecil ini untuk memperluas ruang hidupmu:")
    
    c1, c2 = st.columns(2)
    
    if stat_p == "Fokus Bertahan Diri":
        with c1:
            st.error("🌬️ **Regulasi Sistem Saraf**\nTarik napas 4 detik, tahan 4 detik, buang 4 detik. Fokuslah pada tubuh fisikmu dulu.")
        with c2:
            st.error("💧 **Kebutuhan Dasar**\nCukup minumlah segelas air putih dan basuh wajahmu. Hari ini, bertahan hidup adalah kemenangan besar.")
            
    elif stat_p == "Mulai Beradaptasi":
        with c1:
            st.warning("☀️ **Sapa Dunia Luar**\nBerdirilah di bawah sinar matahari pagi selama 10 menit. Biarkan hormon serotonin membantumu merasa sedikit lebih tenang.")
        with c2:
            st.warning("🎯 **Tugas Mikro**\nSelesaikan satu hal kecil hari ini, misalnya hanya merapikan satu sudut meja kerja Anda.")
            
    elif stat_p == "Pertumbuhan Seimbang":
        with c1:
            st.info("🧩 **Grounding 5-4-3-2-1**\nSebutkan 5 benda yang kamu lihat dan 4 yang kamu sentuh. Bawa dirimu kembali ke masa kini.")
        with c2:
            st.info("🚫 **Batasi Masa Lalu**\nJangan mengecek media sosialnya hari ini. Berikan ruang bagi otakmu untuk bernapas tanpa pemicu lama.")
            
    else: # Ekspansi & Kapasitas Luas
        with c1:
            st.success("🌱 **Rutinitas Baru**\nMulailah membangun kebiasaan pagi yang sama sekali baru dan tidak melibatkan memori masa lalu.")
        with c2:
            st.success("🎨 **Eksplorasi Hobi**\nPelajari satu hal yang selama ini tertunda. Sirkuit saraf yang baru akan membuat hidupmu tumbuh jauh lebih luas.")

# --- PEMBATAS VISUAL 3 ---
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&h=250&q=80", use_container_width=True)
st.markdown("<div class='scroll-hint'>↓ Buang beban pikiranmu di bawah</div>", unsafe_allow_html=True)


# ==========================================
# BLOK 4: RUANG CERITA
# ==========================================
st.markdown("<h2>4. Ruang Cerita</h2>", unsafe_allow_html=True)
st.write("Duka tidak harus hilang untuk kita bisa bercerita. Tuliskan apa pun yang memenuhi pikiranmu saat ini.")

j_text = st.text_area("Tumpahkan di sini...", height=150, label_visibility="collapsed", placeholder="Ketik apa pun yang kamu rasakan tanpa perlu memikirkan struktur kalimat...")

if st.button("Sudah, Terasa Lebih Lega"):
    if j_text:
        j_low = j_text.lower()
        if any(k in j_low for k in ['marah', 'benci', 'kesal', 'bodoh', 'jahat']):
            st.success("Pelepasan emosi yang hebat. Menuliskan kemarahan adalah bentuk perlindungan diri agar stres tidak menetap di tubuhmu.")
        elif any(k in j_low for k in ['kangen', 'rindu', 'sepi', 'sendiri']):
            st.success("Wajar untuk merindu. Izinkan rasa itu ada di sudut kecil hidupmu, sementara bagian hidupmu yang lain terus tumbuh.")
        else:
            st.success("Luar biasa. Menulis terbukti mengalihkan beban kerja otak dari pusat panik ke otak logis. Kamu baru saja memperluas ruang hidupmu.")
        st.balloons()

# ==========================================
# FOOTER: TENTANG, LANDASAN KLINIS & BANTUAN PROFESIONAL
# ==========================================
st.markdown("<div class='spacer-top'></div>", unsafe_allow_html=True)
st.markdown("---") # Garis pembatas footer

with st.expander("ℹ️ Tentang Rekarasa, Landasan Ilmiah & Bantuan Profesional"):
    st.markdown("""
    **Tentang Rekarasa**
    Rekarasa adalah platform pemulihan psikologis mandiri (*self-help*) yang dirancang untuk membantu memetakan, melacak, dan mengelola fluktuasi emosi. Platform ini **bukan pengganti** evaluasi, diagnosis, atau penanganan dari psikolog maupun psikiater profesional.

    **🚨 Kapan Harus Mencari Bantuan Profesional?**
    Pemulihan mandiri memiliki batasan. Anda sangat disarankan untuk segera menjangkau bantuan profesional (psikolog/psikiater) jika Anda mengalami kondisi berikut:
    * **Gangguan Fungsi Harian:** Kesulitan melakukan aktivitas dasar (makan, tidur, menjaga kebersihan diri, atau bekerja) selama lebih dari dua minggu berturut-turut.
    * **Ideasi Berbahaya:** Munculnya pikiran untuk menyakiti diri sendiri atau mengakhiri hidup.
    * **Pelarian Ekstrem:** Mengandalkan alkohol, obat-obatan, atau zat adiktif lainnya sebagai mekanisme koping.
    * **Gejala Fisik Berat:** Mengalami serangan panik persisten (dada sesak, napas pendek), insomnia parah, atau perubahan berat badan yang drastis tanpa sebab medis.
    * **Isolasi Total:** Menarik diri sepenuhnya dari lingkungan sosial terdekat dan kehilangan harapan secara total.
    
    *(Jika Anda berada dalam kondisi krisis darurat, jangan ragu untuk menghubungi layanan darurat kesehatan mental terdekat atau hubungi **119 ekstensi 8** untuk Layanan Sejiwa Kemenkes RI).*

    ---

    **Sumber Riset & Teori Psikologi**
    Seluruh arsitektur logika, metrik, dan intervensi di dalam platform ini dibangun berdasarkan riset dan teori klinis yang dapat dipertanggungjawabkan:

    * **Model *Growing Around Grief* (Lois Tonkin, 1996):** Teori yang memvalidasi bahwa rasa sakit tidak harus mengecil atau dilupakan seiring waktu, melainkan kapasitas hidup manusia lah yang secara perlahan tumbuh membesar mengelilingi memori duka tersebut. Ini merupakan fondasi algoritma Dasbor Rekarasa.
    * **Paradigma *Expressive Writing* (Dr. James W. Pennebaker, 1997):** Riset empiris dari Universitas Texas yang membuktikan bahwa menuliskan emosi terdalam tanpa filter dapat menggeser beban kerja otak dari pusat panik (amigdala) menuju otak logis (korteks prefrontal), serta menurunkan tingkat stres sistemik.
    * **Regulasi Sistem Saraf Parasimpatik (*Box Breathing*):** Teknik pernapasan taktis yang secara luas dipopulerkan oleh mantan Navy SEAL Mark Divine, dan didukung oleh riset klinis mengenai stimulasi saraf vagus (seperti studi oleh psikiater Dr. Richard Brown dan Dr. Patricia Gerbarg). Secara biologis memotong lonjakan hormon kortisol dan adrenalin secara instan.
    * **Teknik Berpijak 5-4-3-2-1 (*Sensory Grounding*):** Praktik yang berakar dari *Mindfulness-Based Cognitive Therapy* (MBCT) dan diadaptasi dari protokol penanganan kecemasan klinis (berkembang dari teknik relaksasi indrawi oleh terapis Betty Erickson). Berfungsi secara neurologis untuk menarik kesadaran kembali ke realitas fisik saat korteks prefrontal dibajak oleh kepanikan.
    """)
    
    st.caption("© 2026 Rekarasa. Dibangun dengan memprioritaskan privasi data dan integritas sains.")