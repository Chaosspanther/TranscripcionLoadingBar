@echo off
echo ========================================
echo    CREANDO EJECUTABLE TRANSCRIPTOR
echo    (Version Corregida - Sin Dependencias Problematicas)
echo ========================================
echo.

echo [1/4] Instalando dependencias basicas...
pip install SpeechRecognition pydub pyaudio pyinstaller

echo.
echo [2/4] Creando ejecutable con configuracion personalizada...
pyinstaller transcriptor_audio.spec

echo.
echo [3/4] Verificando archivos...
if exist "dist\TranscriptorAudio.exe" (
    echo ✓ Ejecutable creado exitosamente!
    echo.
    echo El archivo TranscriptorAudio.exe se encuentra en la carpeta "dist"
    echo.
    echo Caracteristicas incluidas:
    echo - Barra de progreso mejorada
    echo - Estimacion de tiempo restante
    echo - Interfaz grafica moderna
    echo - Informacion detallada por segmentos
    echo - Estadisticas finales completas
    echo.
    echo Para usar el programa:
    echo 1. Ve a la carpeta "dist"
    echo 2. Ejecuta "TranscriptorAudio.exe"
    echo 3. Selecciona tu archivo de audio
    echo 4. Elige donde guardar la transcripcion
    echo 5. ¡Disfruta de la nueva barra de progreso!
) else (
    echo ✗ Error al crear el ejecutable
    echo.
    echo Intentando metodo alternativo...
    echo.
    echo [2b/4] Creando ejecutable con exclusiones manuales...
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
        transcriptor_audio.py
    
    if exist "dist\TranscriptorAudio.exe" (
        echo ✓ Ejecutable creado con metodo alternativo!
    ) else (
        echo ✗ Error persistente al crear el ejecutable
    )
)

echo.
echo [4/4] Limpiando archivos temporales...
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo ========================================
echo    PROCESO COMPLETADO
echo ========================================
pause
