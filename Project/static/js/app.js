document.getElementById('acceptTerms').addEventListener('click', () => {
    document.getElementById('termsModal').style.display = 'none';
});

const canciones = [
    { nombre: "La Quemona", archivo: "/static/audio/cancion1.mp3" },
    { nombre: "El perdedor", archivo: "/static/audio/cancion2.mp3" },
    { nombre: "El condor herido", archivo: "/static/audio/cancion3.mp3" },
    { nombre: "Hermans Habit", archivo: "/static/audio/Hermans.mp3" },
    { nombre: "Techo de astros y truenos", archivo: "/static/audio/Margarita.mp3" },
    { nombre: "Moanin", archivo: "/static/audio/Moanin.mp3" },
    { nombre: "The pink panther theme", archivo: "/static/audio/Pink.mp3" },
    { nombre: "Quitamancha", archivo: "/static/audio/Rescate.mp3" }
];

let currentIndex = 0;
const audio = document.getElementById("audioPlayer");
const songList = document.getElementById("songList");
const progress = document.querySelector(".progress");
const playButton = document.querySelector(".middle");
const currentSongTitle = document.getElementById("currentSongTitle");
const progressBar = document.getElementById("progressBar");

function cargarCanciones() {
    songList.innerHTML = "";
    canciones.forEach((c, i) => {
        const li = document.createElement("li");
        li.textContent = c.nombre;
        li.onclick = () => {
            currentIndex = i;
            reproducirCancion();
        };
        songList.appendChild(li);
    });
    actualizarListaActiva();
}

function actualizarListaActiva() {
    const items = songList.querySelectorAll("li");
    items.forEach((item, i) => {
        item.classList.toggle("active", i === currentIndex);
    });
}

function reproducirCancion() {
    audio.src = canciones[currentIndex].archivo;
    audio.play();
    playButton.textContent = "⏸";
    actualizarListaActiva();
    currentSongTitle.textContent = canciones[currentIndex].nombre;
}

function manualPlay() {
    if (audio.paused) {
        audio.play();
        playButton.textContent = "⏸";
    } else {
        audio.pause();
        playButton.textContent = "▶";
    }
}

function manualNext() {
    currentIndex = (currentIndex + 1) % canciones.length;
    reproducirCancion();
}

function manualPrev() {
    currentIndex = (currentIndex - 1 + canciones.length) % canciones.length;
    reproducirCancion();
}

audio.ontimeupdate = () => {
    if (audio.duration) {
        const porcentaje = (audio.currentTime / audio.duration) * 100;
        progress.style.width = porcentaje + "%";
    }
};

audio.onended = () => {
    playButton.textContent = "▶";
};

progressBar.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;
    const porcentaje = clickX / width;
    audio.currentTime = porcentaje * audio.duration;
});

cargarCanciones();

let video = document.getElementById('video');
const canvas = document.getElementById('canvas');
let cameraOn = false;

function toggleCamera() {
    if (cameraOn) {
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }
        video.srcObject = null;
        cameraOn = false;
    } else {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                cameraOn = true;
                startGestureLoop();
            })
            .catch(error => console.error("Error al acceder a la cámara", error));
    }
}

function startGestureLoop() {
    const gestureBox = document.getElementById("gestureBox");

    setInterval(() => {
        if (!cameraOn || video.readyState < 2) {
            gestureBox.textContent = "Esperando cámara...";
            return;
        }

        gestureBox.textContent = "Analizando gesto...";
        enviarImagen();
    }, 2000); // Cada 2 segundos
}


function enviarImagen() {
    const context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL("image/jpeg");
    console.log("Imagen capturada:", imageData.substring(0, 100));

    fetch("/detectar-gesto/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Gesto detectado:", data.gesto);
        gestureBox.textContent = `Gesto detectado: ${data.gesto}`;
        interpretarGesto(data.gesto);
    })
    .catch(error => {
        console.error("Error en detección de gesto:", error);
        gestureBox.textContent = "Error al detectar gesto.";
    });
}


function interpretarGesto(gesto) {
    switch (gesto) {
        case "Close":
            manualPlay();
            break;
        case "Previous":
            manualNext();
            break;
        case "Next":
            manualPrev();
            break;
        default:
            console.log("Gesto no reconocido");
    }
}

function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : "";
}
