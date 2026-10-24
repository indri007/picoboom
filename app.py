"""
🎮 PICOBOOM PARTY — Game Pesta & Seru-seruan Keluarga di Streamlit
Terinspirasi dari game viral PicoBoom: Oper Bom, Tebak Imposter, Tantangan 5 Detik, dan Hukuman Gokil!
"""

import html
import random
import time
import streamlit as st

# -----------------------------------------------------------------------------
# Konfigurasi Halaman Streamlit
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PicoBoom Party! 💣",
    page_icon="💣",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Custom CSS: Tampilan Ceria, Modern, & Ramah HP (Mobile Friendly)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Fredoka:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Fredoka', 'Baloo 2', system-ui, sans-serif;
    }
    
    /* Header & Title */
    .pico-header {
        text-align: center;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFA900 100%);
        padding: 20px 15px;
        border-radius: 24px;
        color: white;
        box-shadow: 0 8px 24px rgba(255, 107, 107, 0.28);
        margin-bottom: 20px;
    }
    .pico-header h1 {
        color: white !important;
        font-size: 2.3rem !important;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.15);
    }
    .pico-header p {
        color: #FFF3E8;
        font-size: 1.1rem;
        margin: 6px 0 0 0;
        font-weight: 500;
    }

    /* Cards */
    .pico-card {
        background: #FFFFFF;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 6px 0 #EADCD0, 0 10px 25px rgba(0,0,0,0.04);
        border: 2px solid #F6EDE4;
        margin-bottom: 18px;
    }

    /* Big Bomb Display */
    .bomb-box {
        text-align: center;
        padding: 20px 15px;
        border-radius: 24px;
        background: radial-gradient(circle, #FFF5EB 30%, #FFE2D1 100%);
        border: 3px dashed #FF9E6C;
        margin: 15px 0;
    }
    .bomb-icon {
        font-size: 5rem;
        animation: pulse 1s infinite alternate ease-in-out;
        display: inline-block;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); }
        100% { transform: scale(1.15) rotate(5deg); }
    }

    /* Exploded Bomb */
    .boom-box {
        text-align: center;
        padding: 25px 15px;
        border-radius: 24px;
        background: linear-gradient(135deg, #FF416C, #FF4B2B);
        color: white;
        box-shadow: 0 10px 30px rgba(255, 65, 108, 0.4);
        margin: 15px 0;
        animation: shake 0.6s ease-in-out;
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-10px) rotate(-3deg); }
        40%, 80% { transform: translateX(10px) rotate(3deg); }
    }

    /* Prompt Box */
    .prompt-box {
        background: #F8F9FA;
        border-left: 6px solid #FF6B6B;
        padding: 16px 20px;
        border-radius: 16px;
        margin: 14px 0;
        font-size: 1.35rem;
        font-weight: 700;
        color: #2D3748;
        line-height: 1.35;
    }

    /* Secret Card (Imposter) */
    .secret-card {
        background: #2D3748;
        color: white;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(45, 55, 72, 0.3);
        margin: 16px 0;
    }

    /* Player Badge */
    .player-tag {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #F0F4F8;
        border: 2px solid #D9E2EC;
        padding: 8px 16px;
        border-radius: 999px;
        font-size: 1.1rem;
        font-weight: 700;
        color: #334E68;
        margin: 4px;
    }

    /* Streamlit Buttons Style */
    div.stButton > button:first-child {
        border-radius: 18px !important;
        font-weight: 800 !important;
        font-size: 1.25rem !important;
        padding: 12px 28px !important;
        border: none !important;
        box-shadow: 0 5px 0 rgba(0,0,0,0.12) !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button:first-child:active {
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 rgba(0,0,0,0.12) !important;
    }

    /* Custom Radio Tabs */
    .stRadio [role="radiogroup"] {
        gap: 8px;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Sound Synthesizer (Web Audio API)
# -----------------------------------------------------------------------------
def play_sound(sound_type: str):
    """Memutar efek suara instan di browser via Web Audio API tanpa file audio eksternal."""
    js_code = ""
    if sound_type == "tick":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(800, ctx.currentTime);
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.06);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.06);
            } catch(e) {}
        })();
        </script>
        """
    elif sound_type == "boom":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                // Sub-bass rumble
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(140, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(25, ctx.currentTime + 0.8);
                gain.gain.setValueAtTime(0.6, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.9);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.9);
                // Noise burst
                const bufferSize = ctx.sampleRate * 0.5;
                const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = Math.random() * 2 - 1;
                }
                const noise = ctx.createBufferSource();
                noise.buffer = buffer;
                const noiseGain = ctx.createGain();
                noiseGain.gain.setValueAtTime(0.5, ctx.currentTime);
                noiseGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
                noise.connect(noiseGain);
                noiseGain.connect(ctx.destination);
                noise.start();
            } catch(e) {}
        })();
        </script>
        """
    elif sound_type == "ding":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.value = freq;
                    const t = ctx.currentTime + i * 0.09;
                    gain.gain.setValueAtTime(0.25, t);
                    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(t);
                    osc.stop(t + 0.3);
                });
            } catch(e) {}
        })();
        </script>
        """
    elif sound_type == "alarm":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(950, ctx.currentTime);
                gain.gain.setValueAtTime(0.2, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.4);
            } catch(e) {}
        })();
        </script>
        """
    if js_code:
        st.components.v1.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# Database Pertanyaan & Konten Game (Bahasa Indonesia Seru & Kaya)
# -----------------------------------------------------------------------------
BOMB_TOPICS = [
    # Hewan & Alam
    "Sebutkan hewan berkaki empat!",
    "Sebutkan hewan yang bisa terbang selain burung!",
    "Sebutkan hewan yang hidup di dalam air!",
    "Sebutkan hewan yang diawali huruf K!",
    "Sebutkan hewan yang diawali huruf B!",
    "Sebutkan hewan yang punya ekor panjang!",
    "Sebutkan hewan pemakan rumput / tumbuhan!",
    "Sebutkan buah yang banyak bijinya!",
    "Sebutkan buah yang rasanya asam / kecut!",
    "Sebutkan sayuran yang berwarna hijau!",
    "Sebutkan sesuatu yang bisa ditemukan di kebun binatang!",
    "Sebutkan sesuatu yang bisa ditemukan di pantai!",

    # Makanan & Minuman
    "Sebutkan makanan khas Indonesia!",
    "Sebutkan makanan berkuah panas!",
    "Sebutkan makanan yang rasanya manis!",
    "Sebutkan makanan yang digoreng!",
    "Sebutkan minuman yang paling enak diminum saat dingin!",
    "Sebutkan toping martabak manis!",
    "Sebutkan jajanan pasar favorit!",
    "Sebutkan makanan yang berwarna kuning!",
    "Sebutkan makanan yang pedas!",
    "Sebutkan makanan cepat saji (fast food)!",
    "Sebutkan jenis buah yang kulitnya berduri atau kasar!",
    "Sebutkan makanan yang sering ada di acara ulang tahun!",

    # Rumah & Kehidupan Sehari-hari
    "Sebutkan benda yang ada di dalam kamar mandi!",
    "Sebutkan benda elektronik di ruang keluarga!",
    "Sebutkan benda tajam di dapur!",
    "Sebutkan perlengkapan sekolah di tas!",
    "Sebutkan pakaian yang dipakai saat hujan atau dingin!",
    "Sebutkan hal yang dilakukan setelah bangun tidur!",
    "Sebutkan hal yang tidak boleh dilakukan di dalam kelas!",
    "Sebutkan alasan orang datang terlambat!",
    "Sebutkan benda yang gampang pecah!",
    "Sebutkan benda yang terbuat dari plastik!",
    "Sebutkan sesuatu yang berwarna biru di sekitarmu!",
    "Sebutkan sesuatu yang berbau harum!",

    # Profesi, Kota & Dunia
    "Sebutkan profesi yang memakai seragam!",
    "Sebutkan nama kota di pulau Jawa!",
    "Sebutkan nama negara di benua Asia!",
    "Sebutkan jenis kendaraan roda dua atau roda empat!",
    "Sebutkan karakter superhero terkenal!",
    "Sebutkan karakter kartun Disney / anime!",
    "Sebutkan olahraga yang memakai bola!",
    "Sebutkan penyanyi atau band Indonesia!",
    "Sebutkan judul film kartun / animasi!",
    "Sebutkan aplikasi yang paling sering kamu buka di HP!",
]

FIVE_SEC_CHALLENGES = [
    "Sebutkan 3 rasa es krim!",
    "Sebutkan 3 jenis burung!",
    "Sebutkan 3 merek mobil!",
    "Sebutkan 3 jenis sayuran!",
    "Sebutkan 3 nama hewan laut!",
    "Sebutkan 3 karakter superhero Marvel atau DC!",
    "Sebutkan 3 hal berwarna merah di rumahmu!",
    "Sebutkan 3 negara di Asia Tenggara!",
    "Sebutkan 3 nama kota berawalan huruf S!",
    "Sebutkan 3 nama buah yang diawali huruf M!",
    "Sebutkan 3 hal yang dibawa saat liburan!",
    "Sebutkan 3 alasan orang berbohong!",
    "Sebutkan 3 jenis minuman bersoda atau kemasan!",
    "Sebutkan 3 benda di dalam lemari es!",
    "Sebutkan 3 nama bunga yang harum!",
    "Sebutkan 3 makanan pedas!",
    "Sebutkan 3 mata pelajaran sekolah favorit!",
    "Sebutkan 3 hal yang bikin orang tertawa!",
    "Sebutkan 3 aplikasi belanja online!",
    "Sebutkan 3 karakter kartun kartun Spongebob!",
]

IMPOSTER_WORDS = {
    "Makanan & Jajanan": [
        "Bakso", "Sate Ayam", "Nasi Goreng", "Rendang", "Pizza", "Burger", 
        "Martabak", "Siomay", "Cireng", "Soto Ayam", "Es Krim", "Donat"
    ],
    "Hewan": [
        "Kucing Anggora", "Gajah", "Harimau", "Lumba-lumba", "Penguin", 
        "Jerapah", "Kelinci", "Elang", "Kuda Nil", "Kangguru", "Monyet"
    ],
    "Tempat Wisata & Umum": [
        "Pantai Kuta", "Kebun Binatang", "Bioskop", "Bandara", "Pasar Malam", 
        "Museum", "Gunung Bromo", "Candi Borobudur", "Taman Hiburan", "Stasiun Kereta"
    ],
    "Profesi & Tokoh": [
        "Astronot", "Dokter Bedah", "Pilot Pesawat", "Koki Restoran", "Detektif", 
        "Polisi Lalu Lintas", "Pemadam Kebakaran", "Penyanyi Rock", "Guru Sekolah"
    ],
    "Benda Rumah & Elektronik": [
        "Kipas Angin", "Kulkas", "Mesin Cuci", "Smart TV", "Blender", 
        "Setrika", "Kasur Empuk", "Sapu Lantai", "Lampu Tidur", "Jam Dinding"
    ],
}

FORFEITS = [
    "🎭 Tirukan suara hewan (kambing, ayam, atau monyet) sekencang mungkin!",
    "💃 Joget TikTok lucu tanpa ekspresi muka (poker face) selama 15 detik!",
    "🎤 Nyanyikan reff lagu 'Balonku' tapi semua vokal huruf diganti jadi 'O'!",
    "🤖 Bicara seperti robot kaku sampai ronde berikutnya dimulai!",
    "❤️ Gombalin salah satu benda mati di depanmu (misal: botol minum / bantal)!",
    "🙈 Tahan ketawa selama 30 detik saat semua pemain lain mencoba membuatmu tertawa!",
    "📸 Pasang muka terjelek kamu dan biarkan pemain lain memotretnya!",
    "💪 Lakukan 5 kali jumping jacks sambil teriak 'Aku Juara PicoBoom!'",
    "🤫 Jangan boleh bicara sepatah kata pun selama 1 ronde penuh (hanya boleh pakai bahasa isyarat)!",
    "🌟 Sebutkan 3 pujian tulus untuk pemain yang ada di sebelah kirimu!",
    "🦆 Jalan jongkok keliling meja atau ruangan sebanyak 1 putaran!",
]

DEFAULT_AVATARS = ["🦁", "🐼", "🦊", "🐰", "🐸", "🐻", "🦄", "🐶", "🐯", "🐱"]

# -----------------------------------------------------------------------------
# Inisialisasi Session State
# -----------------------------------------------------------------------------
def init_session_state():
    defaults = {
        # Pemain
        "player_count": 4,
        "players": [
            {"name": "Pemain 1", "avatar": "🦁", "score": 0},
            {"name": "Pemain 2", "avatar": "🐼", "score": 0},
            {"name": "Pemain 3", "avatar": "🦊", "score": 0},
            {"name": "Pemain 4", "avatar": "🐰", "score": 0},
        ],
        # Mode Oper Bom
        "bomb_active": False,
        "bomb_exploded": False,
        "bomb_topic": "",
        "bomb_holder_idx": 0,
        "bomb_duration": 25,
        "bomb_start_time": 0.0,
        "bomb_loser": None,
        "bomb_history": [],
        # Mode Imposter
        "imp_category": "Makanan & Jajanan",
        "imp_word": "",
        "imp_imposter_idx": -1,
        "imp_step": "setup",  # setup -> passing -> discussion -> voting -> reveal
        "imp_pass_idx": 0,
        "imp_card_peeked": False,
        "imp_votes": {},
        # Mode 5 Detik
        "five_sec_prompt": "",
        "five_sec_running": False,
        "five_sec_player_idx": 0,
        # Hukuman
        "current_forfeit": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# -----------------------------------------------------------------------------
# Header Utama
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="pico-header">
        <h1>💣 PICOBOOM PARTY! 🎉</h1>
        <p>Game Seru & Heboh untuk Teman, Sahabat, dan Keluarga</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Navigasi Mode Permainan (Tabs Modern)
# -----------------------------------------------------------------------------
tab_bom, tab_imposter, tab_fivesec, tab_forfeit, tab_players = st.tabs(
    [
        "💣 Oper Bom",
        "🕵️ Imposter",
        "⚡ Tantangan 5 Detik",
        "🎡 Roda Hukuman",
        "👥 Pemain",
    ]
)

# =============================================================================
# TAB 1: 💣 OPER BOM (PASS THE BOMB)
# =============================================================================
with tab_bom:
    st.markdown("### 💣 Oper Bom Waktu (Pass the Bomb)")
    st.caption("Jawab topik yang diminta, lalu cepat-cepat oper ke pemain berikutnya sebelum bom meledak! 💥")

    players = st.session_state.players
    num_players = len(players)

    if not st.session_state.bomb_active and not st.session_state.bomb_exploded:
        st.markdown(
            """
            <div class="pico-card">
                <h4>🎯 Cara Main:</h4>
                <ol>
                    <li>Tekan tombol <b>Mulai Bom!</b> di bawah.</li>
                    <li>Satu topik seru akan muncul di layar.</li>
                    <li>Pemain yang memegang giliran harus <b>menyebutkan 1 jawaban</b> sesuai topik.</li>
                    <li>Setelah menjawab, tekan <b>👉 SUDAH JAWAB! OPER BOM</b> ke teman berikutnya.</li>
                    <li>Waktu meledak <b>dirahasiakan</b> (15-35 detik). Pemain yang memegang bom saat meledak dapat hukuman gokil! 💥</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Pilihan Durasi Bom
        col1, col2 = st.columns([1, 1])
        with col1:
            durasi_mode = st.selectbox(
                "⏱️ Tipe Durasi Bom:",
                ["Acak Tegang (15 - 35 Detik)", "Kilat Cepat (12 - 20 Detik)", "Santai (25 - 45 Detik)"],
            )

        if st.button("🚀 MULAI BOM WAKTU! 💣", type="primary", use_container_width=True):
            if "Kilat" in durasi_mode:
                duration = random.randint(12, 20)
            elif "Santai" in durasi_mode:
                duration = random.randint(25, 45)
            else:
                duration = random.randint(15, 35)

            st.session_state.bomb_active = True
            st.session_state.bomb_exploded = False
            st.session_state.bomb_duration = duration
            st.session_state.bomb_start_time = time.time()
            st.session_state.bomb_topic = random.choice(BOMB_TOPICS)
            st.session_state.bomb_holder_idx = random.randint(0, num_players - 1)
            play_sound("tick")
            st.rerun()

    elif st.session_state.bomb_active:
        # Cek apakah waktu sudah habis
        elapsed = time.time() - st.session_state.bomb_start_time
        remaining = st.session_state.bomb_duration - elapsed

        current_holder = players[st.session_state.bomb_holder_idx]

        if remaining <= 0:
            # BOM MELEDAK!
            st.session_state.bomb_active = False
            st.session_state.bomb_exploded = True
            st.session_state.bomb_loser = current_holder
            st.session_state.current_forfeit = random.choice(FORFEITS)
            play_sound("boom")
            st.rerun()
        else:
            # Bom masih aktif
            play_sound("tick")
            st.markdown(
                f"""
                <div class="bomb-box">
                    <div class="bomb-icon">💣🔥</div>
                    <div style="font-size: 1.2rem; color: #D9381E; font-weight: 800; margin-top: 8px;">
                        TIK-TOK-TIK-TOK... BOM BERDETAK!
                    </div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #1E293B; margin-top: 6px;">
                        Giliran: {current_holder['avatar']} {current_holder['name']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="prompt-box">
                    📋 <b>Topik Tantangan:</b><br>
                    {st.session_state.bomb_topic}
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns([2, 1])
            with c1:
                if st.button("👉 SUDAH JAWAB! OPER BOM KE TEMAN", type="primary", use_container_width=True):
                    # Oper ke pemain berikutnya
                    st.session_state.bomb_holder_idx = (st.session_state.bomb_holder_idx + 1) % num_players
                    play_sound("tick")
                    st.rerun()
            with c2:
                if st.button("🏳️ Menyerah", use_container_width=True):
                    st.session_state.bomb_active = False
                    st.session_state.bomb_exploded = True
                    st.session_state.bomb_loser = current_holder
                    st.session_state.current_forfeit = random.choice(FORFEITS)
                    play_sound("boom")
                    st.rerun()

            # Tombol darurat refresh / update detak
            time.sleep(0.5)
            st.rerun()

    elif st.session_state.bomb_exploded:
        loser = st.session_state.bomb_loser
        st.markdown(
            f"""
            <div class="boom-box">
                <div style="font-size: 4rem;">💥 BOOOOOOM! 💥</div>
                <h2 style="color: white; margin: 10px 0;">BOM MELEDAK DI TANGAN:</h2>
                <h1 style="color: #FFE600; font-size: 2.8rem; margin: 0;">{loser['avatar']} {loser['name']}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="pico-card" style="border: 2px solid #FF6B6B; background: #FFFBF9;">
                <h4 style="color: #D9381E; margin-top: 0;">🎲 Hukuman Gokil untuk {loser['name']}:</h4>
                <div style="font-size: 1.3rem; font-weight: 700; color: #2D3748; line-height: 1.4;">
                    {st.session_state.current_forfeit}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎲 Ganti Hukuman Lain", use_container_width=True):
                st.session_state.current_forfeit = random.choice(FORFEITS)
                st.rerun()
        with col_b:
            if st.button("🔁 Main Ronde Baru! 💣", type="primary", use_container_width=True):
                st.session_state.bomb_active = False
                st.session_state.bomb_exploded = False
                st.rerun()

# =============================================================================
# TAB 2: 🕵️ IMPOSTER (TEBAK PENYUSUP / WORD SPY)
# =============================================================================
with tab_imposter:
    st.markdown("### 🕵️ Siapa Imposter? (Find the Faker)")
    st.caption("Semua pemain menerima KATA RAHASIA yang sama, KECUALI satu orang Imposter! Temukan siapa yang pura-pura tahu!")

    step = st.session_state.imp_step
    players = st.session_state.players
    num_players = len(players)

    if step == "setup":
        st.markdown(
            """
            <div class="pico-card">
                <h4>📜 Aturan Main Imposter:</h4>
                <ol>
                    <li>Pilih kategori kata rahasia.</li>
                    <li>Satu per satu pemain memegang HP untuk <b>mengintip kata rahasia</b> secara privat.</li>
                    <li>Warga akan melihat kata aslinya (contoh: <b>"Bakso"</b>).</li>
                    <li><b>Imposter</b> hanya melihat pesan <i>"KAMU IMPOSTER! Kategori: Makanan"</i>.</li>
                    <li>Setiap pemain bergiliran menyebutkan <b>1 kata petunjuk</b>.</li>
                    <li>Lalu semua pemain berdiskusi & voting siapa penyamarnya!</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if num_players < 3:
            st.warning("⚠️ Game Imposter membutuhkan minimal 3 pemain! Silakan tambah pemain di tab '👥 Pemain'.")
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_cat = st.selectbox("📂 Pilih Kategori:", list(IMPOSTER_WORDS.keys()) + ["🎲 Acak Semua Kategori"])
            with col2:
                st.write("")
                st.write("")
                start_imp = st.button("🎬 Mulai Game Imposter!", type="primary", use_container_width=True)

            if start_imp:
                if selected_cat == "🎲 Acak Semua Kategori":
                    actual_cat = random.choice(list(IMPOSTER_WORDS.keys()))
                else:
                    actual_cat = selected_cat

                word = random.choice(IMPOSTER_WORDS[actual_cat])
                imposter_idx = random.randint(0, num_players - 1)

                st.session_state.imp_category = actual_cat
                st.session_state.imp_word = word
                st.session_state.imp_imposter_idx = imposter_idx
                st.session_state.imp_step = "passing"
                st.session_state.imp_pass_idx = 0
                st.session_state.imp_card_peeked = False
                st.session_state.imp_votes = {}
                play_sound("ding")
                st.rerun()

    elif step == "passing":
        idx = st.session_state.imp_pass_idx
        current_p = players[idx]
        is_imposter = (idx == st.session_state.imp_imposter_idx)

        st.markdown(
            f"""
            <div class="pico-card" style="text-align: center;">
                <div style="font-size: 1.2rem; color: #64748B; font-weight: 700;">GILIRAN INTIP KATA ({idx + 1} dari {num_players})</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #1E293B; margin: 10px 0;">
                    {current_p['avatar']} {current_p['name']}
                </div>
                <p style="color: #64748B; margin-bottom: 20px;">
                    Berikan HP ini ke <b>{current_p['name']}</b>. Pastikan pemain lain tidak melihat layar!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Fitur buka / tutup kartu rahasia
        if not st.session_state.imp_card_peeked:
            if st.button("👁️ KLIK UNTUK MELIHAT PERAN & KATAMU", type="primary", use_container_width=True):
                st.session_state.imp_card_peeked = True
                play_sound("ding")
                st.rerun()
        else:
            if is_imposter:
                st.markdown(
                    f"""
                    <div class="secret-card" style="background: linear-gradient(135deg, #FF416C, #FF4B2B);">
                        <div style="font-size: 3.5rem;">😈</div>
                        <h2 style="color: #FFE600; margin: 5px 0;">KAMU ADALAH IMPOSTER!</h2>
                        <p style="font-size: 1.15rem; color: #FFE4E6; margin-bottom: 12px;">
                            Kamu tidak tahu kata aslinya. Pasang telinga baik-baik, dengarkan petunjuk temanmu, dan berpura-puralah tahu!
                        </p>
                        <div style="background: rgba(0,0,0,0.25); padding: 8px 16px; border-radius: 12px; display: inline-block;">
                            Kategori Petunjuk: <b>{st.session_state.imp_category}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="secret-card" style="background: linear-gradient(135deg, #11998E, #38EF7D);">
                        <div style="font-size: 3.5rem;">😇</div>
                        <h3 style="color: #F0FFF4; margin: 5px 0;">Kamu adalah WARGA!</h3>
                        <div style="font-size: 0.95rem; color: #E6FFFA;">Kata rahasia bersama adalah:</div>
                        <div style="font-size: 2.8rem; font-weight: 800; color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); margin: 8px 0;">
                            {st.session_state.imp_word}
                        </div>
                        <div style="background: rgba(0,0,0,0.15); padding: 6px 14px; border-radius: 12px; display: inline-block;">
                            Kategori: <b>{st.session_state.imp_category}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("🔒 Selesai & Oper HP ke Pemain Berikutnya", use_container_width=True):
                st.session_state.imp_card_peeked = False
                if idx + 1 < num_players:
                    st.session_state.imp_pass_idx += 1
                else:
                    st.session_state.imp_step = "discussion"
                st.rerun()

    elif step == "discussion":
        st.markdown(
            f"""
            <div class="pico-card">
                <h3 style="text-align: center; color: #1E293B;">🗣️ Fase Diskusi & Petunjuk!</h3>
                <p style="text-align: center; color: #64748B;">
                    Semua pemain sudah melihat perannya masing-masing. Kategori kata: <b>{st.session_state.imp_category}</b>
                </p>
                <div style="background: #FFF8E7; border-left: 5px solid #FFA900; padding: 14px; border-radius: 12px; margin: 15px 0;">
                    <b>Aturan Giliran:</b>
                    <ul>
                        <li>Setiap pemain bergiliran menyebutkan <b>1 kata saja</b> yang berhubungan dengan kata rahasia.</li>
                        <li>Jangan terlalu gamblang agar Imposter tidak langsung menebak!</li>
                        <li>Imposter harus pintar-pintar menyamar agar tidak dicurigai.</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 🎯 Urutan Berbicara:")
        shuffled_indices = list(range(num_players))
        cols = st.columns(min(num_players, 4))
        for i, p_idx in enumerate(shuffled_indices):
            col_target = cols[i % len(cols)]
            with col_target:
                st.markdown(
                    f"""
                    <div style="background: #F1F5F9; padding: 10px; border-radius: 14px; text-align: center; margin-bottom: 8px;">
                        <span style="font-weight: 800; color: #2563EB;">#{i + 1}</span><br>
                        <span style="font-size: 1.5rem;">{players[p_idx]['avatar']}</span><br>
                        <b>{players[p_idx]['name']}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if st.button("🗳️ Masuk ke Fase Voting! (Siapa yang Dicurigai?)", type="primary", use_container_width=True):
            st.session_state.imp_step = "voting"
            play_sound("alarm")
            st.rerun()

    elif step == "voting":
        st.markdown(
            """
            <div class="pico-card" style="text-align: center;">
                <h3 style="margin: 0; color: #1E293B;">🗳️ Siapa Penyusupnya?</h3>
                <p style="color: #64748B;">Diskusikan bersama dan pilih siapa pemain yang menurut kalian adalah Imposter!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        suspect = st.selectbox(
            "Tersangka Pilihan Mayoritas Warga:",
            options=range(num_players),
            format_func=lambda i: f"{players[i]['avatar']} {players[i]['name']}",
        )

        if st.button("🔍 BUKA IDENTITAS IMPOSTER! 💥", type="primary", use_container_width=True):
            st.session_state.imp_voted_idx = suspect
            st.session_state.imp_step = "reveal"
            play_sound("boom")
            st.rerun()

    elif step == "reveal":
        real_imposter = players[st.session_state.imp_imposter_idx]
        voted_player = players[st.session_state.imp_voted_idx]
        warga_menang = (st.session_state.imp_voted_idx == st.session_state.imp_imposter_idx)

        if warga_menang:
            st.balloons()
            play_sound("ding")
            st.markdown(
                f"""
                <div class="boom-box" style="background: linear-gradient(135deg, #11998E, #38EF7D);">
                    <div style="font-size: 4rem;">🎉🥳</div>
                    <h2 style="color: white; margin: 5px 0;">WARGA MENANG!</h2>
                    <h3 style="color: #FFFFFF; font-weight: 500;">
                        Tebakan tepat! Imposter aslinya memang <b>{real_imposter['avatar']} {real_imposter['name']}</b>!
                    </h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="boom-box" style="background: linear-gradient(135deg, #FF416C, #FF4B2B);">
                    <div style="font-size: 4rem;">😈🎭</div>
                    <h2 style="color: #FFE600; margin: 5px 0;">IMPOSTER MENANG!</h2>
                    <h3 style="color: white; font-weight: 500;">
                        Kalian salah menuduh <b>{voted_player['avatar']} {voted_player['name']}</b>!<br>
                        Imposter aslinya adalah: <b>{real_imposter['avatar']} {real_imposter['name']}</b>!
                    </h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="pico-card" style="text-align: center;">
                <div style="font-size: 1rem; color: #64748B;">Kata rahasia yang asli:</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #2563EB; margin: 4px 0 10px 0;">
                    {st.session_state.imp_word}
                </div>
                <div style="font-size: 0.95rem; color: #64748B;">Kategori: {st.session_state.imp_category}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🔁 Main Lagi Ronde Imposter Baru", type="primary", use_container_width=True):
            st.session_state.imp_step = "setup"
            st.rerun()

# =============================================================================
# TAB 3: ⚡ TANTANGAN 5 DETIK (5-SECOND RULE)
# =============================================================================
with tab_fivesec:
    st.markdown("### ⚡ Tantangan 5 Detik (5-Second Rule)")
    st.caption("Sebutkan 3 hal yang diminta dalam waktu 5 detik sebelum bel berbunyi!")

    players = st.session_state.players
    num_players = len(players)

    # Pilih Pemain yang dapat giliran
    col_p, col_btn = st.columns([2, 1])
    with col_p:
        turn_p_idx = st.selectbox(
            "👤 Giliran Pemain:",
            options=range(num_players),
            index=st.session_state.five_sec_player_idx,
            format_func=lambda i: f"{players[i]['avatar']} {players[i]['name']} (Skor: {players[i]['score']})",
        )
        st.session_state.five_sec_player_idx = turn_p_idx
    with col_btn:
        st.write("")
        st.write("")
        if st.button("🎲 Ganti Soal", use_container_width=True):
            st.session_state.five_sec_prompt = random.choice(FIVE_SEC_CHALLENGES)
            st.rerun()

    if not st.session_state.five_sec_prompt:
        st.session_state.five_sec_prompt = random.choice(FIVE_SEC_CHALLENGES)

    active_p = players[st.session_state.five_sec_player_idx]

    st.markdown(
        f"""
        <div class="pico-card" style="text-align: center; border: 3px solid #FFA900;">
            <div style="font-size: 1.1rem; color: #EA580C; font-weight: 700;">TANTANGAN UNTUK {active_p['avatar']} {active_p['name']}</div>
            <div style="font-size: 2rem; font-weight: 800; color: #1E293B; margin: 12px 0;">
                {st.session_state.five_sec_prompt}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("⏱️ MULAI HITUNG MUNDUR 5 DETIK! 🔥", type="primary", use_container_width=True):
        play_sound("tick")
        progress_bar = st.progress(1.0)
        status_text = st.empty()

        for sec in range(5, 0, -1):
            status_text.markdown(f"<h1 style='text-align: center; color: #EA580C; font-size: 4rem;'>{sec}</h1>", unsafe_allow_html=True)
            progress_bar.progress(sec / 5.0)
            play_sound("tick")
            time.sleep(1.0)

        progress_bar.progress(0.0)
        status_text.markdown("<h1 style='text-align: center; color: #DC2626; font-size: 3.5rem;'>🚨 WAKTU HABIS! 🚨</h1>", unsafe_allow_html=True)
        play_sound("alarm")

    st.markdown("#### 🎯 Hasil Tantangan:")
    c_yes, c_no = st.columns(2)
    with c_yes:
        if st.button("✅ Berhasil Sebut 3 Hal! (+1 ⭐)", use_container_width=True):
            active_p['score'] += 1
            st.session_state.five_sec_player_idx = (st.session_state.five_sec_player_idx + 1) % num_players
            st.session_state.five_sec_prompt = random.choice(FIVE_SEC_CHALLENGES)
            play_sound("ding")
            st.toast(f"Hore! {active_p['name']} berhasil dapat 1 poin!")
            st.rerun()
    with c_no:
        if st.button("❌ Gagal / Terlambat! 😅", use_container_width=True):
            st.session_state.five_sec_player_idx = (st.session_state.five_sec_player_idx + 1) % num_players
            st.session_state.five_sec_prompt = random.choice(FIVE_SEC_CHALLENGES)
            play_sound("boom")
            st.toast(f"Sayang sekali! Giliran berpindah.")
            st.rerun()

# =============================================================================
# TAB 4: 🎡 RODA HUKUMAN GOKIL (FORFEITS)
# =============================================================================
with tab_forfeit:
    st.markdown("### 🎡 Roda Hukuman & Tantangan Lucu")
    st.caption("Kalah di permainan? Putar roda hukuman gokil yang ramah keluarga & bikin ngakak bareng!")

    if not st.session_state.current_forfeit:
        st.session_state.current_forfeit = random.choice(FORFEITS)

    st.markdown(
        f"""
        <div class="pico-card" style="text-align: center; border: 3px solid #8B5CF6; background: #FAF5FF;">
            <div style="font-size: 3.5rem;">🎭</div>
            <div style="font-size: 1.1rem; color: #7C3AED; font-weight: 700;">HUKUMAN SAAT INI:</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #2E1065; margin: 15px 0; line-height: 1.4;">
                {st.session_state.current_forfeit}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🎲 ACAK HUKUMAN BARU! 🔄", type="primary", use_container_width=True):
        st.session_state.current_forfeit = random.choice(FORFEITS)
        play_sound("ding")
        st.rerun()

# =============================================================================
# TAB 5: 👥 DAFTAR PEMAIN
# =============================================================================
with tab_players:
    st.markdown("### 👥 Pengaturan Pemain")
    st.caption("Atur jumlah pemain (2 hingga 10 pemain) dan sesuaikan nama serta avatar hewan lucunya!")

    current_count = len(st.session_state.players)
    new_count = st.slider("Berapa jumlah pemain?", min_value=2, max_value=10, value=current_count)

    # Sinkronisasi jumlah pemain
    if new_count != current_count:
        if new_count > current_count:
            for i in range(current_count, new_count):
                avatar = DEFAULT_AVATARS[i % len(DEFAULT_AVATARS)]
                st.session_state.players.append({"name": f"Pemain {i + 1}", "avatar": avatar, "score": 0})
        else:
            st.session_state.players = st.session_state.players[:new_count]
        st.rerun()

    st.markdown("#### ✏️ Ubah Nama Pemain:")
    cols = st.columns(2)
    for i, p in enumerate(st.session_state.players):
        col_target = cols[i % 2]
        with col_target:
            val = st.text_input(f"Pemain {i + 1} ({p['avatar']}):", value=p["name"], key=f"pname_{i}")
            p["name"] = val

    st.markdown("---")
    st.markdown("#### 🏆 Papan Skor Poin:")
    for p in st.session_state.players:
        st.markdown(
            f"""
            <span class="player-tag">
                {p['avatar']} {p['name']}: <b>{p['score']} ⭐</b>
            </span>
            """,
            unsafe_allow_html=True,
        )

    if st.button("🔄 Reset Semua Skor Jadi 0", use_container_width=True):
        for p in st.session_state.players:
            p["score"] = 0
        st.success("Skor berhasil direset!")
        st.rerun()
