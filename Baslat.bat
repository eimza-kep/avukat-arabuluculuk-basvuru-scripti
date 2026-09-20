@echo off
chcp 65001 >nul
echo =================================================================
echo        HUKUKİ ARABULUCULUK ÖN BAŞVURU SİSTEMİ BAŞLATICI
echo =================================================================
echo.
echo Sunucu hazırlanıyor ve başlatılıyor...
echo Port: 8086
echo.
start "" http://localhost:8086
python server.py
pause
