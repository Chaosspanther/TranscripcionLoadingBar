import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
import time
from datetime import datetime, timedelta
import math

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

class RoundedButton(tk.Canvas):
    """Botón redondeado estilo CSS"""
    def __init__(self, parent, text, command=None, bg="#2196F3", fg="white", 
                 font=("Segoe UI", 10), width=120, height=35, radius=15):
        super().__init__(parent, width=width, height=height, highlightthickness=0, 
                        bg=parent.cget("bg") if hasattr(parent, 'cget') else "#f0f0f0")
        
        self.command = command
        self.bg = bg
        self.fg = fg
        self.font = font
        self.radius = radius
        self.width = width
        self.height = height
        
        # Crear el botón redondeado
        self.create_rounded_rect()
        self.create_text()
        
        # Bind eventos
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def create_rounded_rect(self):
        """Crea un rectángulo redondeado"""
        self.delete("all")
        
        # Colores
        fill_color = self.bg
        
        # Crear rectángulo redondeado
        self.create_rounded_rectangle(
            2, 2, self.width-2, self.height-2,
            radius=self.radius, fill=fill_color, outline=""
        )
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=15, **kwargs):
        """Función para crear rectángulo redondeado"""
        points = []
        
        # Esquinas redondeadas
        for x, y in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]:
            if x == x1 and y == y1:  # Esquina superior izquierda
                for i in range(90, 180, 5):
                    angle = math.radians(i)
                    px = x1 + radius + radius * math.cos(angle)
                    py = y1 + radius + radius * math.sin(angle)
                    points.extend([px, py])
            elif x == x2 and y == y1:  # Esquina superior derecha
                for i in range(0, 90, 5):
                    angle = math.radians(i)
                    px = x2 - radius + radius * math.cos(angle)
                    py = y1 + radius + radius * math.sin(angle)
                    points.extend([px, py])
            elif x == x2 and y == y2:  # Esquina inferior derecha
                for i in range(270, 360, 5):
                    angle = math.radians(i)
                    px = x2 - radius + radius * math.cos(angle)
                    py = y2 - radius + radius * math.sin(angle)
                    points.extend([px, py])
            elif x == x1 and y == y2:  # Esquina inferior izquierda
                for i in range(180, 270, 5):
                    angle = math.radians(i)
                    px = x1 + radius + radius * math.cos(angle)
                    py = y2 - radius + radius * math.sin(angle)
                    points.extend([px, py])
        
        return self.create_polygon(points, **kwargs)
    
    def create_text(self):
        """Crea el texto del botón"""
        self.create_text(
            self.width//2, self.height//2,
            text=self.text, fill=self.fg, font=self.font
        )
    
    def on_click(self, event):
        """Maneja el clic del botón"""
        if self.command:
            self.command()
    
    def on_enter(self, event):
        """Efecto hover"""
        # Cambiar color al pasar el mouse
        hover_color = self.lighten_color(self.bg, 0.1)
        self.create_rounded_rect()
        self.create_text()
    
    def on_leave(self, event):
        """Efecto al salir del mouse"""
        self.create_rounded_rect()
        self.create_text()
    
    def lighten_color(self, color, factor):
        """Aclara un color"""
        # Convertir hex a RGB
        hex_color = color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Aclarar
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"

class ModernCard(tk.Frame):
    """Tarjeta moderna con sombra"""
    def __init__(self, parent, bg="#ffffff", **kwargs):
        super().__init__(parent, bg=bg, relief="flat", bd=0, **kwargs)
        
        # Crear efecto de sombra
        self.shadow = tk.Frame(parent, bg="#000000", height=2)
        self.shadow.place(in_=self, x=2, y=2, relwidth=1, relheight=1)

class TranscriptorAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Transcriptor de Audio Profesional")
        self.root.geometry("800x800")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(True, True)
        
        # Variables
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
        
        self.crear_interfaz_moderna()
    
    def crear_interfaz_moderna(self):
        """Crea una interfaz moderna y profesional"""
        
        # Header con gradiente
        header = tk.Frame(self.root, bg="#667eea", height=120)
        header.pack(fill="x", pady=0)
        header.pack_propagate(False)
        
        # Título principal
        titulo = tk.Label(
            header,
            text="🎵 Transcriptor de Audio",
            font=("Segoe UI", 24, "bold"),
            bg="#667eea",
            fg="white"
        )
        titulo.pack(pady=20)
        
        subtitulo = tk.Label(
            header,
            text="Convierte audio a texto con precisión profesional JASON",
            font=("Segoe UI", 11),
            bg="#667eea",
            fg="#e8f0fe"
        )
        subtitulo.pack()
        
        # Contenido principal
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Card 1: Selección de archivo
        card1 = tk.Frame(main_frame, bg="white", relief="flat", bd=1)
        card1.pack(fill="x", pady=(0, 15))
        
        # Título de la card
        tk.Label(
            card1,
            text="📁 Seleccionar Archivo de Audio",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(15, 8), padx=20, anchor="w")
        
        # Botón de selección
        btn_frame1 = tk.Frame(card1, bg="white")
        btn_frame1.pack(fill="x", padx=20, pady=(0, 15))
        
        btn_seleccionar = tk.Button(
            btn_frame1,
            text="📂 Examinar Archivos",
            command=self.seleccionar_archivo,
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=30,
            pady=12,
            cursor="hand2",
            relief="flat",
            bd=0,
            activebackground="#2980b9",
            activeforeground="white"
        )
        btn_seleccionar.pack(side="left")
        
        # Label del archivo seleccionado
        self.label_archivo = tk.Label(
            card1,
            textvariable=self.archivo_seleccionado,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 10),
            wraplength=500,
            justify="left",
            relief="flat",
            bd=8,
            padx=15,
            pady=10
        )
        self.label_archivo.pack(fill="x", padx=20, pady=(0, 20))
        
        # Card 2: Ubicación de salida
        card2 = tk.Frame(main_frame, bg="white", relief="flat", bd=1)
        card2.pack(fill="x", pady=(0, 15))
        
        # Título de la card
        tk.Label(
            card2,
            text="💾 Ubicación de Guardado",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(15, 8), padx=20, anchor="w")
        
        # Botón de selección de salida
        btn_frame2 = tk.Frame(card2, bg="white")
        btn_frame2.pack(fill="x", padx=20, pady=(0, 15))
        
        btn_salida = tk.Button(
            btn_frame2,
            text="📁 Seleccionar Ubicación",
            command=self.seleccionar_salida,
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=30,
            pady=12,
            cursor="hand2",
            relief="flat",
            bd=0,
            activebackground="#c0392b",
            activeforeground="white"
        )
        btn_salida.pack(side="left")
        
        # Label del archivo de salida
        self.label_salida = tk.Label(
            card2,
            textvariable=self.archivo_salida,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 10),
            wraplength=500,
            justify="left",
            relief="flat",
            bd=8,
            padx=15,
            pady=10
        )
        self.label_salida.pack(fill="x", padx=20, pady=(0, 20))
        
        # Card 3: Controles y progreso
        card3 = tk.Frame(main_frame, bg="white", relief="flat", bd=1)
        card3.pack(fill="x", pady=(0, 15))
        
        # Título de la card
        tk.Label(
            card3,
            text="🎤 Control de Transcripción",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(15, 10), padx=20, anchor="w")
        
        # Frame para botón y progreso
        control_frame = tk.Frame(card3, bg="white")
        control_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Botón principal de transcripción
        self.btn_transcribir = tk.Button(
            control_frame,
            text="🚀 Iniciar Transcripción",
            command=self.iniciar_transcripcion,
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=40,
            pady=15,
            cursor="hand2",
            state="normal",
            relief="flat",
            bd=0,
            activebackground="#229954",
            activeforeground="white"
        )
        self.btn_transcribir.pack(side="left", padx=(0, 20))
        
        # Frame de progreso
        progress_frame = tk.Frame(control_frame, bg="white")
        progress_frame.pack(side="left", fill="x", expand=True)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progreso,
            maximum=100,
            length=300,
            mode='determinate',
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x", pady=(0, 5))
        
        # Información de progreso
        info_frame = tk.Frame(progress_frame, bg="white")
        info_frame.pack(fill="x")
        
        tk.Label(
            info_frame,
            textvariable=self.progreso_detallado,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#27ae60"
        ).pack(side="left")
        
        tk.Label(
            info_frame,
            textvariable=self.tiempo_restante,
            font=("Segoe UI", 9),
            bg="white",
            fg="#7f8c8d"
        ).pack(side="right")
        
        # Información de segmentos
        segment_frame = tk.Frame(progress_frame, bg="white")
        segment_frame.pack(fill="x", pady=(5, 0))
        
        tk.Label(
            segment_frame,
            textvariable=self.segmento_actual,
            font=("Segoe UI", 9),
            bg="white",
            fg="#95a5a6"
        ).pack(side="left")
        
        tk.Label(
            segment_frame,
            textvariable=self.total_segmentos,
            font=("Segoe UI", 9),
            bg="white",
            fg="#95a5a6"
        ).pack(side="right")
        
        # Card 4: Estado
        card4 = tk.Frame(main_frame, bg="white", relief="flat", bd=1)
        card4.pack(fill="x")
        
        # Título de la card
        tk.Label(
            card4,
            text="📊 Estado del Proceso",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(15, 8), padx=20, anchor="w")
        
        # Label de estado
        self.label_estado = tk.Label(
            card4,
            textvariable=self.estado,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 10),
            wraplength=600,
            justify="left",
            relief="flat",
            bd=8,
            padx=15,
            pady=12
        )
        self.label_estado.pack(fill="x", padx=20, pady=(0, 20))
    
        
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
        # Verificar que se hayan seleccionado los archivos
        if not self.archivo_seleccionado.get():
            messagebox.showerror("Error", "Por favor selecciona un archivo de audio")
            return
        
        if not self.archivo_salida.get():
            messagebox.showerror("Error", "Por favor selecciona la ubicación de guardado")
            return
        
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
    style.configure("Modern.Horizontal.TProgressbar",
                   background='#27ae60',
                   troughcolor='#ecf0f1',
                   borderwidth=0,
                   lightcolor='#27ae60',
                   darkcolor='#229954')
    
    app = TranscriptorAudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
   