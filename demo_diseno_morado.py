#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo del nuevo diseño con gradiente morado
"""

import tkinter as tk
from tkinter import ttk

def crear_demo_gradiente():
    """Crea una ventana de demostración del nuevo diseño"""
    root = tk.Tk()
    root.title("🎨 Demo - Nuevo Diseño con Gradiente Morado")
    root.geometry("600x500")
    root.configure(bg="#1a0033")
    
    # Crear canvas para el fondo con gradiente
    canvas = tk.Canvas(root, width=600, height=500, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Crear gradiente morado
    def crear_gradiente_morado():
        width = root.winfo_width()
        height = root.winfo_height()
        
        # Colores del gradiente morado
        color1 = "#1a0033"  # Morado muy oscuro
        color2 = "#4a148c"  # Morado medio
        color3 = "#7b1fa2"  # Morado claro
        color4 = "#9c27b0"  # Morado más claro
        
        # Crear gradiente vertical
        for i in range(height):
            # Calcular el color basado en la posición
            ratio = i / height
            
            if ratio < 0.25:
                # Transición de color1 a color2
                r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
                r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
                ratio_local = ratio / 0.25
            elif ratio < 0.5:
                # Transición de color2 a color3
                r1, g1, b1 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
                r2, g2, b2 = int(color3[1:3], 16), int(color3[3:5], 16), int(color3[5:7], 16)
                ratio_local = (ratio - 0.25) / 0.25
            elif ratio < 0.75:
                # Transición de color3 a color4
                r1, g1, b1 = int(color3[1:3], 16), int(color3[3:5], 16), int(color3[5:7], 16)
                r2, g2, b2 = int(color4[1:3], 16), int(color4[3:5], 16), int(color4[5:7], 16)
                ratio_local = (ratio - 0.5) / 0.25
            else:
                # Transición de color4 a color3 (para el final)
                r1, g1, b1 = int(color4[1:3], 16), int(color4[3:5], 16), int(color4[5:7], 16)
                r2, g2, b2 = int(color3[1:3], 16), int(color3[3:5], 16), int(color3[5:7], 16)
                ratio_local = (ratio - 0.75) / 0.25
            
            # Interpolar colores
            r = int(r1 + (r2 - r1) * ratio_local)
            g = int(g1 + (g2 - g1) * ratio_local)
            b = int(b1 + (b2 - b1) * ratio_local)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, width=1)
    
    crear_gradiente_morado()
    
    # Título
    titulo = tk.Label(
        root, 
        text="🎵 Transcriptor de Audio a Texto", 
        font=("Arial", 18, "bold"),
        bg="#4a148c",
        fg="white",
        relief="flat",
        bd=0
    )
    titulo.place(relx=0.5, rely=0.1, anchor="center")
    
    # Frame de demostración
    frame_demo = tk.Frame(root, bg="", relief="flat", bd=0)
    frame_demo.place(relx=0.5, rely=0.3, anchor="center", width=500)
    
    # Botones de demostración
    btn1 = tk.Button(
        frame_demo,
        text="📁 Examinar archivos",
        bg="#e91e63",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=25,
        pady=8,
        cursor="hand2",
        relief="flat",
        bd=0,
        activebackground="#c2185b",
        activeforeground="white"
    )
    btn1.pack(pady=5)
    
    btn2 = tk.Button(
        frame_demo,
        text="💾 Seleccionar ubicación",
        bg="#9c27b0",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=25,
        pady=8,
        cursor="hand2",
        relief="flat",
        bd=0,
        activebackground="#7b1fa2",
        activeforeground="white"
    )
    btn2.pack(pady=5)
    
    btn3 = tk.Button(
        frame_demo,
        text="🎤 Iniciar Transcripción",
        bg="#673ab7",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=12,
        cursor="hand2",
        relief="flat",
        bd=0,
        activebackground="#512da8",
        activeforeground="white"
    )
    btn3.pack(pady=10)
    
    # Barra de progreso de demostración
    progress = ttk.Progressbar(
        frame_demo,
        length=300,
        mode='determinate'
    )
    progress.pack(pady=10)
    progress['value'] = 65
    
    # Labels de demostración
    label_info = tk.Label(
        frame_demo,
        text="65.0%",
        font=("Arial", 9, "bold"),
        bg="",
        fg="white"
    )
    label_info.pack()
    
    label_tiempo = tk.Label(
        frame_demo,
        text="⏱️ 2m 15s restantes",
        font=("Arial", 8),
        bg="",
        fg="#e1bee7"
    )
    label_tiempo.pack()
    
    label_estado = tk.Label(
        frame_demo,
        text="🎤 Transcribiendo segmento 3 de 5...",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#4a148c",
        relief="flat",
        bd=5,
        padx=10,
        pady=5
    )
    label_estado.pack(pady=10, fill="x")
    
    # Texto informativo
    info_text = tk.Label(
        root,
        text="✨ Nuevo diseño con gradiente morado\n🎨 Colores que combinan perfectamente\n📱 Interfaz moderna y atractiva",
        font=("Arial", 10),
        bg="",
        fg="#f3e5f5",
        justify="center"
    )
    info_text.place(relx=0.5, rely=0.85, anchor="center")
    
    root.mainloop()

if __name__ == "__main__":
    crear_demo_gradiente()
