@echo off
cd /d "%~dp0"

echo.
echo ============================================
echo   Avvio del server musicale...
echo   Il browser si aprira automaticamente.
echo   Per fermare il server: chiudi questa finestra
echo ============================================
echo.

REM Aspetta 1 secondo, poi apre il browser (senza bloccare lo script)
start "" /b cmd /c "timeout /t 1 /nobreak >nul && start http://localhost:8000"

REM Avvia il server Python (questa riga resta in attesa)
python server.py

REM Se il server si chiude, tiene la finestra aperta per leggere eventuali errori
echo.
echo Server fermato.
pause