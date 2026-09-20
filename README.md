# Hukuki Arabuluculuk Ön Başvuru ve Dosya Takip Portalı

[![CI Test Suite](https://github.com/eimza-kep/avukat-arabuluculuk-basvuru-scripti/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/avukat-arabuluculuk-basvuru-scripti/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://python.org)
[![PHP: 7.4+](https://img.shields.io/badge/PHP-7.4%2B-purple.svg)](https://php.net)

Hukuk büroları, avukatlar ve uzman arabulucular için; 6325 sayılı Hukuk Uyuşmazlıklarında Arabuluculuk Kanunu (HUAK), 7036 sayılı İş Mahkemeleri Kanunu ve 6102 sayılı TTK m. 5/A hükümleri doğrultusunda **dava şartı (zorunlu)** ve **ihtiyari arabuluculuk** başvurularını toplayan, **resmi başvuru formunu yazdıran** ve dosya süreçlerini yöneten açık kaynaklı kurumsal portal.

---

## 🎯 Temel Yetenekler

- **Çoklu Uyuşmazlık Alanı Desteği:**
  - **İş Hukuku:** Kıdem tazminatı, ihbar, fazla çalışma, yıllık izin, UBGT, işe iade talepleri.
  - **Ticari Uyuşmazlıklar (TTK 5/A):** Fatura alacakları, cari hesap bakiyesi, sözleşmeden doğan cezai şartlar.
  - **Kira ve Kat Mülkiyeti (7445 Sayılı Yargı Paketi):** Taşınmazın tahliyesi, kira bedeli tespiti, aidat uyuşmazlıkları.
  - **Tüketici Uyuşmazlıkları** ve genel hukuki ihtilaflar.
- **Resmi Başvuru ve Talep Tutanağı Çıktısı:** Adalet Bakanlığı Arabuluculuk Daire Başkanlığı yönergeleriyle uyumlu, PDF veya yazıcı çıktısı alınabilir resmi başvuru evrakı üretir.
- **Arabulucu & Dosya Yönetim Paneli (`/admin`):**
  - Dosya Takip Numarası (`ARB-2026-XXXX`) ile arama ve filtreleme.
  - Dosya süreç takibi: "Başvuru Alındı", "İlk Toplantı Belirlendi", "Müzakereler Devam Ediyor", "Anlaşma Sağlandı", "Anlaşamama Tutanağı Tanzim Edildi".
  - Uyuşmazlık türlerine göre toplam talep tutarları ve analitik istatistikler.
  - UTF-8 BOM destekli Excel uyumlu **CSV Dışa Aktarımı**.
- **Sıfır Bağımlılık (Zero-Dependency):**
  - **Python Motoru:** Dahili SQLite veritabanı ile tek tıkla lokalde veya sunucuda çalışır (`server.py`).
  - **PHP Motoru:** Paylaşımlı hosting ve cPanel için hazır JSON REST backend (`api.php`).
  - **Offline Mod:** İnternetsiz veya offline kullanım için `localStorage` desteği.

---

## 🚀 Hızlı Başlangıç

### Windows (Tek Tıkla Çalıştır)
1. Repoyu klonlayın veya zip olarak indirin.
2. `Baslat.bat` dosyasına çift tıklayın.
3. Otomatik olarak açılır:
   - Başvuru Formu: `http://localhost:8086`
   - Dosya Yönetim Paneli: `http://localhost:8086/admin`

### Linux & macOS
```bash
git clone https://github.com/eimza-kep/avukat-arabuluculuk-basvuru-scripti.git
cd avukat-arabuluculuk-basvuru-scripti
chmod +x baslat.sh
./baslat.sh
```

### PHP / Paylaşımlı Hosting
Dosyaları sunucunuzdaki `/arabuluculuk/` dizinine yükleyin. `api.php` otomatik olarak JSON veritabanını yapılandıracaktır.

---

## 📊 Mimari ve Dosya Yapısı

```
avukat-arabuluculuk-basvuru-scripti/
├── index.html              # Arabuluculuk başvuru formu ve resmi tutanak çıktısı
├── admin.html              # Arabulucu dosya ve oturum takip paneli
├── server.py               # Standalone Python SQLite HTTP sunucusu (Port 8086)
├── api.php                 # PHP tabanlı REST backend
├── Baslat.bat              # Windows tek tıkla başlatıcı
├── baslat.sh               # Linux / macOS başlatıcı
├── scripts/
│   └── test_arabuluculuk.py # Otomatik test paketi
├── .github/
│   └── workflows/ci.yml    # GitHub Actions CI testi
└── README.md               # Dokümantasyon
```

---

## 🧪 Testleri Çalıştırma

```bash
python scripts/test_arabuluculuk.py
```

---

## ⚖️ Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında açık kaynak olarak sunulmuştur.
