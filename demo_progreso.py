#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de la nueva barra de progreso mejorada
Este archivo demuestra las nuevas características de la barra de progreso
"""

import time
import os
import sys

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

def demo_transcripcion():
    """Simula el proceso de transcripción con la nueva barra de progreso"""
    print("🎵 === DEMO DE TRANSCRIPCIÓN CON BARRA DE PROGRESO MEJORADA ===")
    print("Este demo simula el proceso de transcripción para mostrar las nuevas características.\n")
    
    tiempo_inicio = time.time()
    
    # Simular diferentes etapas del proceso
    etapas = [
        (5, "🔍 Verificando archivo..."),
        (10, "📁 Cargando archivo de audio..."),
        (15, "🔄 Preparando audio para transcripción..."),
        (20, "✂️ Dividiendo audio en 5 segmentos..."),
    ]
    
    # Mostrar etapas iniciales
    for progreso, estado in etapas:
        mostrar_progreso_detallado(progreso, estado, tiempo_inicio=tiempo_inicio)
        time.sleep(0.5)
    
    # Simular transcripción de segmentos
    total_segmentos = 5
    for i in range(total_segmentos):
        progreso_segmento = 25 + (i * 65 / total_segmentos)
        mostrar_progreso_detallado(
            progreso_segmento, 
            f"🎤 Transcribiendo segmento {i + 1}...", 
            segmento_actual=i + 1, 
            total_segmentos=total_segmentos,
            tiempo_inicio=tiempo_inicio
        )
        time.sleep(1)  # Simular tiempo de procesamiento
        print(f"\n✅ Segmento {i + 1} transcrito con éxito.")
    
    # Etapas finales
    etapas_finales = [
        (90, "💾 Guardando transcripción..."),
        (95, "🧹 Limpiando archivos temporales..."),
        (100, "✅ ¡Transcripción completada!")
    ]
    
    for progreso, estado in etapas_finales:
        mostrar_progreso_detallado(progreso, estado, tiempo_inicio=tiempo_inicio)
        time.sleep(0.3)
    
    # Mostrar estadísticas finales
    tiempo_total = time.time() - tiempo_inicio
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    
    print(f"\n📊 Estadísticas de transcripción:")
    print(f"• Segmentos procesados: {total_segmentos}/{total_segmentos}")
    print(f"• Tiempo total: {minutos}m {segundos}s")
    print(f"• Archivo guardado en: transcripcion_demo.txt")
    
    print("\n🎉 === DEMO COMPLETADO ===")
    print("¡La nueva barra de progreso muestra información detallada en tiempo real!")

if __name__ == "__main__":
    demo_transcripcion()
