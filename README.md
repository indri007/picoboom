# 💣 PICOBOOM PARTY! 🎉

Game pesta, arisan, kumpul keluarga, dan seru-seruan bareng teman yang terinspirasi dari game viral **PicoBoom**. Dibuat menggunakan Python & **Streamlit** sehingga mudah dimainkan di HP maupun laptop, serta siap di-deploy langsung ke **Streamlit Community Cloud** (gratis!).

---

## ✨ Mode Permainan

### 1. 💣 Oper Bom Waktu (Pass the Bomb)
- Waktu bom berdetak secara rahasia (**15–35 detik**).
- Topik acak muncul di layar (Hewan, Makanan, Hal Sehari-hari, dll).
- Pemain harus menjawab cepat lalu tekan **👉 SUDAH JAWAB! OPER BOM** ke teman berikutnya.
- Suara bom berdetak makin cepat via Web Audio API.
- Pemain yang memegang bom saat meledak (**💥 BOOM!**) mendapatkan hukuman gokil!

### 2. 🕵️ Imposter (Siapa Penyusup?)
- 3–10 pemain.
- Semua pemain (Warga) melihat **kata rahasia** yang sama (contoh: *Bakso*).
- 1 pemain dipilih acak sebagai **Imposter** dan hanya melihat pesan *KAMU IMPOSTER!* serta nama kategori.
- Fitur **Intip Privat**: HP dioper bergiliran untuk melihat peran masing-masing secara rahasia.
- Fase Petunjuk: Tiap pemain bergiliran menyebutkan **1 kata petunjuk**.
- Fase Voting: Selidiki dan tangkap siapa penyusupnya!

### 3. ⚡ Tantangan 5 Detik (5-Second Rule)
- Tantangan cepat: *"Sebutkan 3 rasa es krim!"*, *"Sebutkan 3 merek mobil!"*, dll.
- Visual bar & suara hitung mundur **5 detik**.
- Berhasil atau gagal langsung menambah poin di papan skor.

### 4. 🎡 Roda Hukuman Gokil
- Puluhan tantangan & hukuman lucu, aman, dan ramah anak/keluarga (joget ekspresi datar, suara hewan, gombalin benda mati, dll).

### 5. 👥 Pengaturan Pemain
- Dukungan **2 hingga 10 pemain**.
- Nama bisa disesuaikan.
- Avatar hewan lucu (🦁, 🐼, 🦊, 🐰, 🐸, dll).
- Papan skor terintegrasi.

---

## 🚀 Cara Menjalankan Secara Lokal

1. Pastikan Python sudah terpasang di komputer Anda.
2. Masuk ke folder proyek dan pasang dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Buka tautan lokal yang muncul (biasanya `http://localhost:8501`).

---

## 🌐 Cara Upload & Deploy ke Streamlit Community Cloud (Gratis)

### Langkah 1: Buat Repositori di GitHub
1. Buka [GitHub.com](https://github.com) dan buat repositori baru bernama `picoboom`.
2. Di terminal komputer Anda, jalankan:
   ```bash
   cd /Users/jevin/game/picoboom
   git init
   git branch -M main
   git add .
   git commit -m "Initial commit: PicoBoom Party Streamlit Game"
   git remote add origin https://github.com/<username-github-anda>/picoboom.git
   git push -u origin main
   ```

### Langkah 2: Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io) dan login menggunakan akun GitHub Anda.
2. Klik tombol **New app**.
3. Isi kolom:
   - **Repository:** `<username-github-anda>/picoboom`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Klik **Deploy!**
5. Dalam ~1 menit, game PicoBoom Anda sudah online dan punya tautan web yang bisa langsung dibuka bersama di HP! 📲

---

## 📄 Lisensi
MIT License
