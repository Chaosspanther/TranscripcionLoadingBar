@echo off
echo ========================================
echo    CREANDO EJECUTABLE TRANSCRIPTOR
echo ========================================
echo.

echo [1/4] Instalando dependencias...
pip install SpeechRecognition pydub pyaudio pyinstaller

echo.
echo [2/4] Creando ejecutable...
pyinstaller --onefile --windowed --name="TranscriptorAudio" transcriptor_audio.py

echo.
echo [3/4] Verificando archivos...
if exist "dist\TranscriptorAudio.exe" (
    echo ✓ Ejecutable creado exitosamente!
    echo.
    echo El archivo TranscriptorAudio.exe se encuentra en la carpeta "dist"
    echo.
    echo Para usar el programa:
    echo 1. Ve a la carpeta "dist"
    echo 2. Ejecuta "TranscriptorAudio.exe"
    echo 3. Selecciona tu archivo de audio
    echo 4. Elige donde guardar la transcripción
    echo 5. ¡Listo!
) else (
    echo ✗ Error al crear el ejecutable
)

echo.
echo [4/4] Limpiando archivos temporales...
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.spec" del "*.spec"

echo.
echo ========================================
echo    PROCESO COMPLETADO
echo ========================================
pause
