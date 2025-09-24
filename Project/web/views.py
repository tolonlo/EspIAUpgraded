import os
import json
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .model.gesture_detector import GestureDetector

# Inicializa el detector solo una vez
detector = GestureDetector()

@csrf_exempt
@require_http_methods(["POST"])
def detectar_gesto(request):
    try:
        data = json.loads(request.body)
        image_data = data.get("image")
        if not image_data:
            return JsonResponse({"error": "No se envió imagen"}, status=400)

        header, encoded = image_data.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_bytes))
        img_np = np.array(img)
        # Convertir PIL a OpenCV
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        result, error_msg = detector.process_image(img_cv)
        if error_msg:
            return JsonResponse({"error": error_msg}, status=200)

        gesture_name = result["gesture_name"]

        return JsonResponse({"gesto": gesture_name})

    except Exception as e:
        print("Error procesando gesto:", e)
        return JsonResponse({"error": str(e)}, status=500)


def home(request):
    return render(request, 'index.html')


def terminos(request):
    return render(request, 'terminos.html')


def login(request):
    return render(request, 'login.html')


def lista_canciones(request):
    carpeta_audio = os.path.join(settings.BASE_DIR, 'static', 'audio')
    archivos = []

    if os.path.exists(carpeta_audio):
        for archivo in os.listdir(carpeta_audio):
            if archivo.endswith('.mp3'):
                archivos.append({
                    'nombre': os.path.splitext(archivo)[0].replace('_', ' ').capitalize(),
                    'ruta': f'/static/audio/{archivo}'
                })

    return JsonResponse({'canciones': archivos})
