# SinTo – Reconocimiento de gestos con Django + TensorFlow + Mediapipe

Este proyecto es una aplicación web construida con Django que permite detectar gestos de mano mediante la cámara del navegador. Utiliza un modelo entrenado con TensorFlow Lite y la detección de puntos clave de la mano proporcionada por Mediapipe.

---

## Funcionalidades

- Captura de imagen desde la cámara web del usuario.
- Detección de gestos con un modelo `.tflite`.
- Control de acciones (como reproducir música, cambiar canción, etc.) según el gesto detectado.
- Compatible con despliegue en plataformas como Render.com.

---

## Requisitos

### Python
- Python 3.10

### Dependencias

Estas son las principales dependencias usadas en el proyecto:

```txt
Django
Pillow
numpy
opencv-python
tensorflow-cpu==2.18.0
mediapipe
gunicorn
dj-database-url
whitenoise
requests
social-auth-app-django
```

## Instalación local
### Clona el repositorio

```bash
   git clone https://github.com/DisakHK/espIA
   cd espIA
```
### Crea y activa un entorno virtual

```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
```
### Instala los paquetes

```bash
   pip install -r requirements.txt
```
### Migraciones y archivos estáticos

```bash
   python manage.py migrate
   python manage.py collectstatic
```
### Ejecuta el servidor

```bash
   python manage.py runserver
```

## Creditos
Recomendamos visitar el repositorio de https://github.com/kinivi/hand-gesture-recognition-mediapipe de donde nos basamos para entrenar y usar el modelo.
