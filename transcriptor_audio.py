import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
import time
from datetime import datetime, timedelta

try:
    import speech_recognition as sr
    import pydub
    from pydub import AudioSegment
except ImportError:
    print("Instalando dependencias...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "SpeechRecognition", "pydub", "pyaudio"])
    import speech_recognition as sr
    import pydub
    from pydub import AudioSegment

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

class TranscriptorAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcriptor de Audio")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        self.archivo_seleccionado = tk.StringVar()
        self.archivo_salida = tk.StringVar()
        self.progreso = tk.DoubleVar()
        self.estado = tk.StringVar(value="Listo para transcribir")
        self.progreso_detallado = tk.StringVar(value="0%")
        self.tiempo_restante = tk.StringVar(value="")
        self.segmento_actual = tk.StringVar(value="")
        self.total_segmentos = tk.StringVar(value="")
        
        # Variables para el cálculo de tiempo
        self.tiempo_inicio = None
        self.segmentos_completados = 0
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        titulo = tk.Label(
            self.root, 
            text="🎵 Transcriptor de Audio a Texto", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo.pack(pady=20)
        
        frame_archivo = tk.Frame(self.root, bg="#f0f0f0")
        frame_archivo.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            frame_archivo, 
            text="Seleccionar archivo de audio:", 
            font=("Arial", 10, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        btn_seleccionar = tk.Button(
            frame_archivo,
            text="📁 Examinar archivos",
            command=self.seleccionar_archivo,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        )
        btn_seleccionar.pack(pady=5)
        
        self.label_archivo = tk.Label(
            frame_archivo,
            textvariable=self.archivo_seleccionado,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Arial", 9),
            wraplength=500,
            justify="left"
        )
        self.label_archivo.pack(pady=5, fill="x")
        
        frame_salida = tk.Frame(self.root, bg="#f0f0f0")
        frame_salida.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            frame_salida, 
            text="Archivo de salida:", 
            font=("Arial", 10, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        btn_salida = tk.Button(
            frame_salida,
            text="💾 Seleccionar ubicación de guardado",
            command=self.seleccionar_salida,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        )
        btn_salida.pack(pady=5)
        
        self.label_salida = tk.Label(
            frame_salida,
            textvariable=self.archivo_salida,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Arial", 9),
            wraplength=500,
            justify="left"
        )
        self.label_salida.pack(pady=5, fill="x")
        
        frame_controles = tk.Frame(self.root, bg="#f0f0f0")
        frame_controles.pack(pady=20, padx=20, fill="x")
        
        self.btn_transcribir = tk.Button(
            frame_controles,
            text="🎤 Iniciar Transcripción",
            command=self.iniciar_transcripcion,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.btn_transcribir.pack(side="left", padx=10)
        
        # Frame para la barra de progreso mejorada
        frame_progreso = tk.Frame(frame_controles, bg="#f0f0f0")
        frame_progreso.pack(side="left", padx=10, fill="x", expand=True)
        
        # Barra de progreso principal
        self.progress_bar = ttk.Progressbar(
            frame_progreso,
            variable=self.progreso,
            maximum=100,
            length=200,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x", pady=2)
        
        # Información detallada del progreso
        frame_info_progreso = tk.Frame(frame_progreso, bg="#f0f0f0")
        frame_info_progreso.pack(fill="x", pady=2)
        
        # Porcentaje y tiempo restante
        tk.Label(
            frame_info_progreso,
            textvariable=self.progreso_detallado,
            font=("Arial", 9, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(side="left")
        
        tk.Label(
            frame_info_progreso,
            textvariable=self.tiempo_restante,
            font=("Arial", 8),
            bg="#f0f0f0",
            fg="#7f8c8d"
        ).pack(side="right")
        
        # Información de segmentos
        frame_segmentos = tk.Frame(frame_progreso, bg="#f0f0f0")
        frame_segmentos.pack(fill="x", pady=1)
        
        tk.Label(
            frame_segmentos,
            textvariable=self.segmento_actual,
            font=("Arial", 8),
            bg="#f0f0f0",
            fg="#34495e"
        ).pack(side="left")
        
        tk.Label(
            frame_segmentos,
            textvariable=self.total_segmentos,
            font=("Arial", 8),
            bg="#f0f0f0",
            fg="#34495e"
        ).pack(side="right")
        
        frame_estado = tk.Frame(self.root, bg="#f0f0f0")
        frame_estado.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            frame_estado,
            text="Estado:",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        self.label_estado = tk.Label(
            frame_estado,
            textvariable=self.estado,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Arial", 9),
            wraplength=500,
            justify="left"
        )
        self.label_estado.pack(pady=5, fill="x")
        
    def seleccionar_archivo(self):
        tipos_archivo = [
            ("Archivos de audio", "*.wav *.mp3 *.m4a *.flac *.aac *.ogg *.wma"),
            ("Archivos WAV", "*.wav"),
            ("Archivos MP3", "*.mp3"),
            ("Todos los archivos", "*.*")
        ]
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=tipos_archivo
        )
        
        if archivo:
            self.archivo_seleccionado.set(f"📄 {os.path.basename(archivo)}")
            self.archivo_path = archivo
            self.verificar_botones()
            
    def seleccionar_salida(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar transcripción como",
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.archivo_salida.set(f"💾 {os.path.basename(archivo)}")
            self.salida_path = archivo
            self.verificar_botones()
            
    def verificar_botones(self):
        if hasattr(self, "archivo_path") and hasattr(self, "salida_path"):
            self.btn_transcribir.config(state="normal")
    
    def calcular_tiempo_restante(self, progreso_actual, tiempo_transcurrido):
        """Calcula el tiempo restante estimado basado en el progreso actual"""
        if progreso_actual <= 0:
            return ""
        
        tiempo_total_estimado = tiempo_transcurrido / (progreso_actual / 100)
        tiempo_restante = tiempo_total_estimado - tiempo_transcurrido
        
        if tiempo_restante <= 0:
            return "Finalizando..."
        
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        
        if minutos > 0:
            return f"⏱️ {minutos}m {segundos}s restantes"
        else:
            return f"⏱️ {segundos}s restantes"
    
    def actualizar_progreso(self, valor, estado_texto, segmento_actual=None, total_segmentos=None):
        """Actualiza la barra de progreso con información detallada"""
        self.progreso.set(valor)
        self.progreso_detallado.set(f"{valor:.1f}%")
        self.estado.set(estado_texto)
        
        if segmento_actual is not None and total_segmentos is not None:
            self.segmento_actual.set(f"Segmento: {segmento_actual}")
            self.total_segmentos.set(f"de {total_segmentos}")
        
        # Calcular tiempo restante si tenemos tiempo de inicio
        if self.tiempo_inicio and valor > 0:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            tiempo_rest = self.calcular_tiempo_restante(valor, tiempo_transcurrido)
            self.tiempo_restante.set(tiempo_rest)
        
        # Actualizar la interfaz
        self.root.update_idletasks()
            
    def iniciar_transcripcion(self):
        self.btn_transcribir.config(state="disabled")
        self.tiempo_inicio = time.time()
        self.segmentos_completados = 0
        
        # Limpiar variables de progreso
        self.progreso.set(0)
        self.progreso_detallado.set("0%")
        self.tiempo_restante.set("")
        self.segmento_actual.set("")
        self.total_segmentos.set("")
        self.estado.set("Iniciando transcripción...")
        
        hilo = threading.Thread(target=self.transcribir_audio)
        hilo.daemon = True
        hilo.start()
        
    def transcribir_audio(self):
        try:
            # Verificar que ffmpeg esté disponible
            ffmpeg_path = os.environ.get('FFMPEG_BINARY')
            if not ffmpeg_path:
                self.actualizar_progreso(0, "Error: FFmpeg no está configurado")
                messagebox.showerror("Error", "FFmpeg no está disponible. Por favor, instala ffmpeg y vuelve a intentar.")
                return
            
            self.actualizar_progreso(5, "🔍 Verificando archivo...")
            
            # Verificar que el archivo existe
            if not os.path.exists(self.archivo_path):
                self.actualizar_progreso(0, "Error: Archivo no encontrado")
                messagebox.showerror("Error", f"El archivo no existe: {self.archivo_path}")
                return
            
            self.actualizar_progreso(10, "📁 Cargando archivo de audio...")
            audio = AudioSegment.from_file(self.archivo_path)
            
            self.actualizar_progreso(15, "🔄 Preparando audio para transcripción...")
            audio = audio.set_frame_rate(16000).set_channels(1)
            
            # Dividir en segmentos para mejor progreso
            segment_duration_ms = 30000  # 30 segundos por segmento
            total_duration = len(audio)
            segments = [audio[i:i + segment_duration_ms] for i in range(0, total_duration, segment_duration_ms)]
            
            self.actualizar_progreso(20, f"✂️ Dividiendo audio en {len(segments)} segmentos...", 0, len(segments))
            
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            
            full_text = ""
            temp_files = []
            
            # Procesar cada segmento
            for idx, segment in enumerate(segments):
                segment_path = f"temp_segment_{idx}.wav"
                segment.export(segment_path, format="wav")
                temp_files.append(segment_path)
                
                self.actualizar_progreso(
                    25 + (idx * 65 / len(segments)), 
                    f"🎤 Transcribiendo segmento {idx + 1}...", 
                    idx + 1, 
                    len(segments)
                )
                
                with sr.AudioFile(segment_path) as source:
                    try:
                        audio_data = recognizer.record(source)
                        texto_segmento = recognizer.recognize_google(audio_data, language="es-ES", show_all=False)
                        full_text += texto_segmento + "\n"
                        
                        self.segmentos_completados += 1
                        
                    except sr.UnknownValueError:
                        self.actualizar_progreso(
                            25 + (idx * 65 / len(segments)), 
                            f"⚠️ Segmento {idx + 1} no reconocido, continuando...", 
                            idx + 1, 
                            len(segments)
                        )
                    except sr.RequestError as e:
                        self.actualizar_progreso(
                            25 + (idx * 65 / len(segments)), 
                            f"❌ Error en segmento {idx + 1}: {str(e)}", 
                            idx + 1, 
                            len(segments)
                        )
                    except Exception as e:
                        self.actualizar_progreso(
                            25 + (idx * 65 / len(segments)), 
                            f"❌ Error inesperado en segmento {idx + 1}: {str(e)}", 
                            idx + 1, 
                            len(segments)
                        )
            
            self.actualizar_progreso(90, "💾 Guardando transcripción...")
            
            # Guardar la transcripción
            with open(self.salida_path, "w", encoding="utf-8") as f:
                f.write(f"Transcripción del archivo: {os.path.basename(self.archivo_path)}\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Segmentos procesados: {self.segmentos_completados}/{len(segments)}\n")
                f.write("=" * 60 + "\n\n")
                f.write(full_text)
            
            # Limpiar archivos temporales
            self.actualizar_progreso(95, "🧹 Limpiando archivos temporales...")
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            self.actualizar_progreso(100, "✅ ¡Transcripción completada!")
            
            # Mostrar estadísticas finales
            tiempo_total = time.time() - self.tiempo_inicio
            minutos = int(tiempo_total // 60)
            segundos = int(tiempo_total % 60)
            
            mensaje = f"✅ Transcripción completada exitosamente!\n\n"
            mensaje += f"📊 Estadísticas:\n"
            mensaje += f"• Segmentos procesados: {self.segmentos_completados}/{len(segments)}\n"
            mensaje += f"• Tiempo total: {minutos}m {segundos}s\n"
            mensaje += f"• Archivo guardado en: {self.salida_path}"
            
            messagebox.showinfo("Transcripción Completada", mensaje)
            
        except FileNotFoundError as e:
            self.actualizar_progreso(0, "❌ Error: Archivo no encontrado")
            messagebox.showerror("Error", f"Error: No se puede encontrar el archivo especificado.\n{str(e)}")
        except Exception as e:
            self.actualizar_progreso(0, f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error durante la transcripción:\n{str(e)}")
            
        finally:
            self.btn_transcribir.config(state="normal")
            # Resetear variables para próxima transcripción
            self.tiempo_inicio = None
            self.segmentos_completados = 0

def main():
    root = tk.Tk()
    
    # Configurar estilo personalizado para la barra de progreso
    style = ttk.Style()
    style.theme_use('clam')
    
    # Crear estilo personalizado para la barra de progreso
    style.configure("Custom.Horizontal.TProgressbar",
                   background='#3498db',
                   troughcolor='#ecf0f1',
                   borderwidth=0,
                   lightcolor='#3498db',
                   darkcolor='#3498db')
    
    app = TranscriptorAudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
   