#!/usr/bin/env bash
echo "================================================================="
echo "       HUKUKİ ARABULUCULUK ÖN BAŞVURU SİSTEMİ BAŞLATICI"
echo "================================================================="
echo ""
echo "Sunucu başlatılıyor: http://localhost:8086"
echo "Dosya Yönetim Paneli: http://localhost:8086/admin"
echo ""

if command -v python3 &>/dev/null; then
    python3 server.py
elif command -v python &>/dev/null; then
    python server.py
else
    echo "Hata: Python bulunamadı!"
    exit 1
fi
