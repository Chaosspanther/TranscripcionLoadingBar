@echo off
echo ========================================
echo    CREANDO EJECUTABLE SIMPLE
echo ========================================
echo.

echo [1/3] Instalando dependencias minimas...
pip install pyinstaller

echo.
echo [2/3] Creando ejecutable con exclusiones...
pyinstaller --onefile --windowed --name="TranscriptorAudio" ^
    --exclude-module=torch ^
    --exclude-module=torchvision ^
    --exclude-module=torchaudio ^
    --exclude-module=tensorflow ^
    --exclude-module=keras ^
    --exclude-module=sklearn ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    --exclude-module=PIL ^
    --exclude-module=cv2 ^
    --exclude-module=opencv ^
    --exclude-module=jupyter ^
    --exclude-module=notebook ^
    --exclude-module=IPython ^
    --exclude-module=test ^
    --exclude-module=tests ^
    --exclude-module=testing ^
    transcriptor_audio.py

echo.
echo [3/3] Verificando resultado...
if exist "dist\TranscriptorAudio.exe" (
    echo ✓ Ejecutable creado exitosamente!
    echo Ubicacion: dist\TranscriptorAudio.exe
) else (
    echo ✗ Error al crear el ejecutable
)

echo.
pause
