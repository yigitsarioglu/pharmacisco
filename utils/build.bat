@echo off

echo Pharmacisco EXE Derleniyor... Lutfen bekleyin.

REM Pyinstaller ile derleme
call venv\Scripts\pyinstaller --noconfirm --onedir --windowed --name Pharmacisco --icon icons\pharmacisco.ico main.py

echo.
echo Ayar ve gorsel dosyalari kopyalaniyor...

copy config.json dist\Pharmacisco\ > nul
copy .env dist\Pharmacisco\ > nul
xcopy icons dist\Pharmacisco\icons\ /E /H /C /I /Y > nul

echo.
echo Islem tamamlandi! dist\Pharmacisco klasoru hazir.

pause
