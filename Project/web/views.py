from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os

def home(request):
    return render(request, 'index.html')
def terminos(request):
    return render(request, 'terminos.html')

def login(request):
    return render(request, 'login.html')

def lista_canciones(request):
    carpeta_audio = os.path.join(settings.BASE_DIR, 'static', 'audio')
    archivos = []

    # Validar que la carpeta existe para evitar errores
    if os.path.exists(carpeta_audio):
        for archivo in os.listdir(carpeta_audio):
            if archivo.endswith('.mp3'):
                archivos.append({
                    'nombre': os.path.splitext(archivo)[0].replace('_', ' ').capitalize(),  # nombre sin extensión, con espacios y capitalizado
                    'ruta': f'/static/audio/{archivo}'
                })

    return JsonResponse({'canciones': archivos})
