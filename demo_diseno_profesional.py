#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo del nuevo diseño profesional con cards y botones modernos
"""

import tkinter as tk
from tkinter import ttk

def crear_demo_profesional():
    """Crea una ventana de demostración del nuevo diseño profesional"""
    root = tk.Tk()
    root.title("🎨 Demo - Diseño Profesional")
    root.geometry("700x600")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)
    
    # Header con gradiente
    header = tk.Frame(root, bg="#667eea", height=120)
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
        text="Convierte audio a texto con precisión profesional",
        font=("Segoe UI", 11),
        bg="#667eea",
        fg="#e8f0fe"
    )
    subtitulo.pack()
    
    # Contenido principal
    main_frame = tk.Frame(root, bg="#f8f9fa")
    main_frame.pack(fill="both", expand=True, padx=30, pady=20)
    
    # Card 1: Selección de archivo
    card1 = tk.Frame(main_frame, bg="white", relief="flat", bd=0)
    card1.pack(fill="x", pady=(0, 20))
    
    # Sombra de la card
    shadow1 = tk.Frame(main_frame, bg="#000000", height=2)
    shadow1.place(in_=card1, x=2, y=2, relwidth=1, relheight=1)
    
    # Título de la card
    tk.Label(
        card1,
        text="📁 Seleccionar Archivo de Audio",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#2c3e50"
    ).pack(pady=(20, 10), padx=20, anchor="w")
    
    # Botón de selección
    btn_frame1 = tk.Frame(card1, bg="white")
    btn_frame1.pack(fill="x", padx=20, pady=(0, 15))
    
    btn_seleccionar = tk.Button(
        btn_frame1,
        text="📂 Examinar Archivos",
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
    tk.Label(
        card1,
        text="📄 mi_audio.mp3",
        bg="#ecf0f1",
        fg="#2c3e50",
        font=("Segoe UI", 10),
        wraplength=500,
        justify="left",
        relief="flat",
        bd=8,
        padx=15,
        pady=10
    ).pack(fill="x", padx=20, pady=(0, 20))
    
    # Card 2: Ubicación de salida
    card2 = tk.Frame(main_frame, bg="white", relief="flat", bd=0)
    card2.pack(fill="x", pady=(0, 20))
    
    # Sombra de la card
    shadow2 = tk.Frame(main_frame, bg="#000000", height=2)
    shadow2.place(in_=card2, x=2, y=2, relwidth=1, relheight=1)
    
    # Título de la card
    tk.Label(
        card2,
        text="💾 Ubicación de Guardado",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#2c3e50"
    ).pack(pady=(20, 10), padx=20, anchor="w")
    
    # Botón de selección de salida
    btn_frame2 = tk.Frame(card2, bg="white")
    btn_frame2.pack(fill="x", padx=20, pady=(0, 15))
    
    btn_salida = tk.Button(
        btn_frame2,
        text="📁 Seleccionar Ubicación",
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
    tk.Label(
        card2,
        text="💾 transcripcion.txt",
        bg="#ecf0f1",
        fg="#2c3e50",
        font=("Segoe UI", 10),
        wraplength=500,
        justify="left",
        relief="flat",
        bd=8,
        padx=15,
        pady=10
    ).pack(fill="x", padx=20, pady=(0, 20))
    
    # Card 3: Controles y progreso
    card3 = tk.Frame(main_frame, bg="white", relief="flat", bd=0)
    card3.pack(fill="x", pady=(0, 20))
    
    # Sombra de la card
    shadow3 = tk.Frame(main_frame, bg="#000000", height=2)
    shadow3.place(in_=card3, x=2, y=2, relwidth=1, relheight=1)
    
    # Título de la card
    tk.Label(
        card3,
        text="🎤 Control de Transcripción",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#2c3e50"
    ).pack(pady=(20, 15), padx=20, anchor="w")
    
    # Frame para botón y progreso
    control_frame = tk.Frame(card3, bg="white")
    control_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    # Botón principal de transcripción
    btn_transcribir = tk.Button(
        control_frame,
        text="🚀 Iniciar Transcripción",
        bg="#27ae60",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=40,
        pady=15,
        cursor="hand2",
        relief="flat",
        bd=0,
        activebackground="#229954",
        activeforeground="white"
    )
    btn_transcribir.pack(side="left", padx=(0, 20))
    
    # Frame de progreso
    progress_frame = tk.Frame(control_frame, bg="white")
    progress_frame.pack(side="left", fill="x", expand=True)
    
    # Barra de progreso
    progress = ttk.Progressbar(
        progress_frame,
        length=300,
        mode='determinate'
    )
    progress.pack(fill="x", pady=(0, 5))
    progress['value'] = 65
    
    # Información de progreso
    info_frame = tk.Frame(progress_frame, bg="white")
    info_frame.pack(fill="x")
    
    tk.Label(
        info_frame,
        text="65.0%",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#27ae60"
    ).pack(side="left")
    
    tk.Label(
        info_frame,
        text="⏱️ 2m 15s restantes",
        font=("Segoe UI", 9),
        bg="white",
        fg="#7f8c8d"
    ).pack(side="right")
    
    # Información de segmentos
    segment_frame = tk.Frame(progress_frame, bg="white")
    segment_frame.pack(fill="x", pady=(5, 0))
    
    tk.Label(
        segment_frame,
        text="Segmento: 3",
        font=("Segoe UI", 9),
        bg="white",
        fg="#95a5a6"
    ).pack(side="left")
    
    tk.Label(
        segment_frame,
        text="de 5",
        font=("Segoe UI", 9),
        bg="white",
        fg="#95a5a6"
    ).pack(side="right")
    
    # Card 4: Estado
    card4 = tk.Frame(main_frame, bg="white", relief="flat", bd=0)
    card4.pack(fill="x")
    
    # Sombra de la card
    shadow4 = tk.Frame(main_frame, bg="#000000", height=2)
    shadow4.place(in_=card4, x=2, y=2, relwidth=1, relheight=1)
    
    # Título de la card
    tk.Label(
        card4,
        text="📊 Estado del Proceso",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#2c3e50"
    ).pack(pady=(20, 10), padx=20, anchor="w")
    
    # Label de estado
    tk.Label(
        card4,
        text="🎤 Transcribiendo segmento 3 de 5...",
        bg="#ecf0f1",
        fg="#2c3e50",
        font=("Segoe UI", 10),
        wraplength=600,
        justify="left",
        relief="flat",
        bd=8,
        padx=15,
        pady=12
    ).pack(fill="x", padx=20, pady=(0, 20))
    
    # Texto informativo
    info_text = tk.Label(
        root,
        text="✨ Diseño profesional con cards modernas\n🎨 Botones con colores Material Design\n📱 Interfaz limpia y organizada",
        font=("Segoe UI", 10),
        bg="#f8f9fa",
        fg="#7f8c8d",
        justify="center"
    )
    info_text.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    crear_demo_profesional()
