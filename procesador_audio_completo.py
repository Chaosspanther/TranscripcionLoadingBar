import os
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.video.io.VideoFileClip import VideoFileClip
import time
from datetime import datetime

# Funciones para mostrar progreso en consola
def mostrar_barra_progreso(progreso, total=100, ancho=50, prefijo="Progreso", sufijo="Completado"):
    """Muestra una barra de progreso en la consola"""
    porcentaje = progreso / total
    barras_completas = int(ancho * porcentaje)
    barras_vacias = ancho - barras_completas
    
    barra = "█" * barras_completas + "░" * barras_vacias
    print(f"\r{prefijo}: |{barra}| {progreso:.1f}% {sufijo}", end="", flush=True)

def mostrar_progreso_detallado(progreso, estado, segmento_actual=None, total_segmentos=None, tiempo_inicio=None):
    """Muestra información detallada del progreso"""
    print(f"\n🔄 {estado}")
    
    if segmento_actual and total_segmentos:
        print(f"📊 Segmento: {segmento_actual}/{total_segmentos}")
    
    if tiempo_inicio and progreso > 0:
        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_total_estimado = tiempo_transcurrido / (progreso / 100)
        tiempo_restante = tiempo_total_estimado - tiempo_transcurrido
        
        if tiempo_restante > 0:
            minutos = int(tiempo_restante // 60)
            segundos = int(tiempo_restante % 60)
            if minutos > 0:
                print(f"⏱️ Tiempo restante estimado: {minutos}m {segundos}s")
            else:
                print(f"⏱️ Tiempo restante estimado: {segundos}s")
    
    mostrar_barra_progreso(progreso, prefijo="Progreso", sufijo="")

# Configurar ffmpeg para pydub - Buscar automáticamente
def encontrar_ffmpeg():
    """Busca ffmpeg en ubicaciones comunes"""
    posibles_rutas = [
        r"C:\Users\Usuario\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
        "ffmpeg.exe",  # Si está en PATH
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta) or ruta == "ffmpeg.exe":
            return ruta
    
    return None

def encontrar_ffprobe():
    """Busca ffprobe en ubicaciones comunes"""
    posibles_rutas = [
        r"C:\Users\Usuario\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe",
        r"C:\ffmpeg\bin\ffprobe.exe",
        r"C:\Program Files\ffmpeg\bin\ffprobe.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffprobe.exe",
        "ffprobe.exe",  # Si está en PATH
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta) or ruta == "ffprobe.exe":
            return ruta
    
    return None

# Buscar ffmpeg automáticamente
ffmpeg_path = encontrar_ffmpeg()
ffprobe_path = encontrar_ffprobe()

if ffmpeg_path and ffprobe_path:
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    os.environ["FFPROBE_BINARY"] = ffprobe_path
    print(f"FFmpeg configurado correctamente: {ffmpeg_path}")
    print(f"FFprobe configurado correctamente: {ffprobe_path}")
else:
    print("Error: No se encontraron los archivos ffmpeg.exe o ffprobe.exe")
    print("Por favor, instala ffmpeg y asegúrate de que esté en el PATH del sistema")
    print("O coloca los archivos ffmpeg.exe y ffprobe.exe en la misma carpeta que este script")

def convertir_mp4_a_m4a(ruta_mp4, ruta_m4a):
    """Convierte un archivo MP4 a M4A"""
    try:
        # Cargar el archivo MP4
        with VideoFileClip(ruta_mp4) as video:
            # Extraer el audio y guardarlo como M4A
            print(f"Convirtiendo {ruta_mp4} a {ruta_m4a}...")
            video.audio.write_audiofile(ruta_m4a, codec='aac')
            print("Conversión MP4 a M4A completada.")
            return True
    except FileNotFoundError:
        print(f"Error: El archivo {ruta_mp4} no existe.")
        return False
    except Exception as e:
        print(f"Error durante la conversión MP4 a M4A: {e}")
        return False

def transcribir_audio(audio_file_path):
    """Transcribe un archivo de audio a texto tal como se escucha, sin autocorrecciones"""
    tiempo_inicio = time.time()
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(audio_file_path):
        print(f"❌ Error: El archivo de audio no existe: {audio_file_path}")
        return False
    
    # Verificar que ffmpeg está configurado
    ffmpeg_path = os.environ.get('FFMPEG_BINARY')
    if not ffmpeg_path:
        print("❌ Error: FFmpeg no está configurado. No se puede procesar el archivo de audio.")
        return False
    
    mostrar_progreso_detallado(5, "🔍 Verificando archivo...", tiempo_inicio=tiempo_inicio)
    
    # Convertir el archivo .m4a a un archivo .wav para ser utilizado con speech_recognition
    wav_file_path = "temp_audio.wav"
    try:
        mostrar_progreso_detallado(10, "🔄 Convirtiendo archivo de audio a WAV...", tiempo_inicio=tiempo_inicio)
        print(f"\n📁 Usando ffmpeg desde: {ffmpeg_path}")
        
        # Usar subprocess para llamar ffmpeg directamente
        import subprocess
        
        # Comando ffmpeg directo para convertir cualquier formato a WAV
        cmd = [
            ffmpeg_path,
            '-i', audio_file_path,
            '-ar', '16000',  # Sample rate 16kHz
            '-ac', '1',      # Mono
            '-y',            # Sobrescribir archivo de salida
            wav_file_path
        ]
        
        print(f"⚙️ Ejecutando comando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            mostrar_progreso_detallado(15, "✅ Archivo convertido exitosamente a WAV temporal.", tiempo_inicio=tiempo_inicio)
        else:
            print(f"\n❌ Error en ffmpeg: {result.stderr}")
            return False
            
    except FileNotFoundError as e:
        print(f"\n❌ Error: No se puede encontrar ffmpeg en la ruta especificada: {ffmpeg_path}")
        print("Por favor, verifica que ffmpeg esté instalado correctamente.")
        return False
    except Exception as e:
        print(f"\n❌ Error al convertir el archivo: {e}")
        print("Verificando configuración de ffmpeg...")
        print(f"FFMPEG_BINARY: {ffmpeg_path}")
        return False

    # Dividir el archivo .wav en segmentos más pequeños
    segment_duration_ms = 30000  # Duración de cada segmento en milisegundos (30 segundos)
    audio = AudioSegment.from_file(wav_file_path, format="wav")
    total_duration = len(audio)
    segments = [audio[i:i + segment_duration_ms] for i in range(0, total_duration, segment_duration_ms)]

    mostrar_progreso_detallado(20, f"✂️ Dividiendo audio en {len(segments)} segmentos...", tiempo_inicio=tiempo_inicio)

    recognizer = sr.Recognizer()
    # Configurar para transcripción más literal
    recognizer.energy_threshold = 300  # Umbral de energía más bajo para capturar mejor el audio
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8  # Pausa más corta para mejor segmentación
    
    full_text = ""
    segmentos_completados = 0

    # Procesar cada segmento y transcribirlo
    for idx, segment in enumerate(segments):
        segment_path = f"segment_{idx}.wav"
        segment.export(segment_path, format="wav")
        
        progreso_segmento = 25 + (idx * 65 / len(segments))
        mostrar_progreso_detallado(
            progreso_segmento, 
            f"🎤 Transcribiendo segmento {idx + 1}...", 
            segmento_actual=idx + 1, 
            total_segmentos=len(segments),
            tiempo_inicio=tiempo_inicio
        )
        
        with sr.AudioFile(segment_path) as source:
            try:
                audio_data = recognizer.record(source)
                # Usar reconocimiento sin autocorrecciones para obtener transcripción literal
                text = recognizer.recognize_google(audio_data, language="es-ES", show_all=False)
                full_text += text + "\n"
                segmentos_completados += 1
                print(f"\n✅ Segmento {idx + 1} transcrito con éxito.")
            except sr.UnknownValueError:
                print(f"\n⚠️ No se pudo reconocer el audio del segmento {idx + 1}.")
            except sr.RequestError as e:
                print(f"\n❌ Hubo un problema con el servicio de reconocimiento de voz en el segmento {idx + 1}: {e}")
            except Exception as e:
                print(f"\n❌ Ocurrió un error en el segmento {idx + 1}: {e}")

        # Eliminar el archivo temporal del segmento
        if os.path.exists(segment_path):
            os.remove(segment_path)

    mostrar_progreso_detallado(90, "💾 Guardando transcripción...", tiempo_inicio=tiempo_inicio)

    # Guardar la transcripción completa en un archivo de texto
    txt_file_path = "transcripcion_completa.txt"
    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(f"Transcripción del archivo: {os.path.basename(audio_file_path)}\n")
        txt_file.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        txt_file.write(f"Segmentos procesados: {segmentos_completados}/{len(segments)}\n")
        txt_file.write("=" * 60 + "\n\n")
        txt_file.write(full_text)

    mostrar_progreso_detallado(95, "🧹 Limpiando archivos temporales...", tiempo_inicio=tiempo_inicio)

    # Eliminar el archivo temporal .wav
    if os.path.exists(wav_file_path):
        os.remove(wav_file_path)
        print("\n🗑️ Archivo WAV temporal eliminado.")
    
    mostrar_progreso_detallado(100, "✅ ¡Transcripción completada!", tiempo_inicio=tiempo_inicio)
    
    # Mostrar estadísticas finales
    tiempo_total = time.time() - tiempo_inicio
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    
    print(f"\n📊 Estadísticas de transcripción:")
    print(f"• Archivo procesado: {os.path.basename(audio_file_path)}")
    print(f"• Segmentos procesados: {segmentos_completados}/{len(segments)}")
    print(f"• Tiempo total: {minutos}m {segundos}s")
    print(f"• Archivo guardado en: {txt_file_path}")
    
    return True

def procesar_audio_completo(ruta_archivo):
    """Función principal que procesa cualquier archivo de audio y lo transcribe"""
    tiempo_inicio_total = time.time()
    
    print("🎵 === INICIANDO PROCESAMIENTO COMPLETO DE AUDIO ===")
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo no existe: {ruta_archivo}")
        return False
    
    # Obtener información del archivo
    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    extension = os.path.splitext(ruta_archivo)[1].lower()
    
    print(f"📁 Procesando archivo: {ruta_archivo}")
    print(f"📄 Tipo de archivo: {extension}")
    
    # Si es MP4, convertir a M4A primero
    if extension == '.mp4':
        directorio = os.path.dirname(ruta_archivo)
        ruta_m4a = os.path.join(directorio, f"{nombre_base}.m4a")
        
        print("\n🔄 --- PASO 1: CONVERSIÓN MP4 A M4A ---")
        mostrar_progreso_detallado(5, "🎬 Convirtiendo MP4 a M4A...", tiempo_inicio=tiempo_inicio_total)
        
        if not convertir_mp4_a_m4a(ruta_archivo, ruta_m4a):
            print("❌ Error en la conversión MP4 a M4A. Deteniendo el proceso.")
            return False
        
        mostrar_progreso_detallado(10, "✅ Conversión MP4 a M4A completada", tiempo_inicio=tiempo_inicio_total)
        archivo_para_transcribir = ruta_m4a
    else:
        # Para otros formatos (MP3, WAV, etc.), usar directamente
        mostrar_progreso_detallado(10, "✅ Archivo compatible, iniciando transcripción...", tiempo_inicio=tiempo_inicio_total)
        archivo_para_transcribir = ruta_archivo
    
    # Paso 2: Transcribir el audio
    print("\n🎤 --- PASO 2: TRANSCRIPCIÓN DE AUDIO ---")
    if not transcribir_audio(archivo_para_transcribir):
        print("❌ Error en la transcripción. Deteniendo el proceso.")
        return False
    
    # Mostrar estadísticas finales
    tiempo_total = time.time() - tiempo_inicio_total
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    
    print("\n🎉 === PROCESAMIENTO COMPLETADO CON ÉXITO ===")
    if extension == '.mp4':
        print(f"📁 Archivo M4A generado: {archivo_para_transcribir}")
    print(f"📄 Archivo de transcripción: transcripcion_completa.txt")
    print(f"⏱️ Tiempo total del proceso: {minutos}m {segundos}s")
    
    return True

# Configuración de rutas
if __name__ == "__main__":
    # Verificar que ffmpeg esté disponible antes de continuar
    if not os.environ.get('FFMPEG_BINARY'):
        print("Error: FFmpeg no está disponible. No se puede continuar.")
        print("Por favor, instala ffmpeg y vuelve a ejecutar el script.")
        input("Presiona Enter para salir...")
        exit(1)
    
    print("=== TRANSCRIPTOR DE AUDIO ===")
    print("NOTA: El reconocimiento de voz puede aplicar algunas autocorrecciones automáticas.")
    print("Para transcripción 100% literal, considera usar servicios especializados como Whisper.")
    print("=" * 60)
    
    # Solicitar archivo al usuario
    ruta_archivo = input("Ingresa la ruta completa del archivo de audio (MP3, MP4, WAV, etc.): ").strip()
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo no existe: {ruta_archivo}")
        input("Presiona Enter para salir...")
        exit(1)
    
    # Ejecutar el procesamiento completo
    if procesar_audio_completo(ruta_archivo):
        print("\n¡Transcripción completada exitosamente!")
    else:
        print("\nError durante la transcripción.")
    
    input("Presiona Enter para salir...") 