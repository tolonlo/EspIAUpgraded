"""
Implementación de patrones de diseño Python
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
import time
import threading
from enum import Enum


# 1. SINGLETON PATTERN
class AudioManager:
    """Singleton para manejar el estado global del audio"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.current_song = None
            self.is_playing = False
            self.volume = 0.8
            self.initialized = True
    
    def set_current_song(self, song: str):
        self.current_song = song
    
    def get_current_song(self) -> Optional[str]:
        return self.current_song


# 2. OBSERVER PATTERN
class Observer(ABC):
    """Interface para observadores"""
    
    @abstractmethod
    def update(self, subject, event: str, data: Any = None):
        pass


class Subject:
    """Sujeto observable"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: str, data: Any = None):
        for observer in self._observers:
            observer.update(self, event, data)


class MusicPlayer(Subject):
    """Reproductor de música que notifica cambios"""
    
    def __init__(self):
        super().__init__()
        self.current_song = None
        self.is_playing = False
        self.position = 0.0
    
    def play(self, song: str):
        self.current_song = song
        self.is_playing = True
        self.notify("song_started", {"song": song})
    
    def pause(self):
        self.is_playing = False
        self.notify("song_paused", {"song": self.current_song})
    
    def stop(self):
        self.is_playing = False
        self.position = 0.0
        self.notify("song_stopped", {"song": self.current_song})


class PlaylistObserver(Observer):
    """Observador que actualiza la playlist"""
    
    def update(self, subject, event: str, data: Any = None):
        if event == "song_started":
            print(f"🎵 Reproduciendo: {data['song']}")
        elif event == "song_paused":
            print(f"⏸️ Pausado: {data['song']}")
        elif event == "song_stopped":
            print(f"⏹️ Detenido: {data['song']}")


class GestureObserver(Observer):
    """Observador que maneja gestos"""
    
    def update(self, subject, event: str, data: Any = None):
        if event == "song_started":
            print("🤖 Gesto: Iniciando detección de gestos")
        elif event == "song_paused":
            print("🤖 Gesto: Pausando detección de gestos")


# 3. STRATEGY PATTERN
class GestureStrategy(ABC):
    """Estrategia para interpretar gestos"""
    
    @abstractmethod
    def execute(self, player: MusicPlayer) -> bool:
        pass


class PlayPauseStrategy(GestureStrategy):
    """Estrategia para play/pause"""
    
    def execute(self, player: MusicPlayer) -> bool:
        if player.is_playing:
            player.pause()
        else:
            player.play(player.current_song or "default_song")
        return True


class NextSongStrategy(GestureStrategy):
    """Estrategia para siguiente canción"""
    
    def execute(self, player: MusicPlayer) -> bool:
        # Lógica para siguiente canción
        print("⏭️ Siguiente canción")
        return True


class PreviousSongStrategy(GestureStrategy):
    """Estrategia para canción anterior"""
    
    def execute(self, player: MusicPlayer) -> bool:
        # Lógica para canción anterior
        print("⏮️ Canción anterior")
        return True


class GestureContext:
    """Contexto que usa estrategias"""
    
    def __init__(self):
        self._strategies: Dict[str, GestureStrategy] = {}
    
    def set_strategy(self, gesture: str, strategy: GestureStrategy):
        self._strategies[gesture] = strategy
    
    def execute_gesture(self, gesture: str, player: MusicPlayer) -> bool:
        strategy = self._strategies.get(gesture)
        if strategy:
            return strategy.execute(player)
        return False


# 4. FACTORY PATTERN
class AudioFormat(Enum):
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"


class AudioPlayerFactory:
    """Factory para crear reproductores de audio"""
    
    @staticmethod
    def create_player(format_type: AudioFormat):
        if format_type == AudioFormat.MP3:
            return MP3Player()
        elif format_type == AudioFormat.WAV:
            return WAVPlayer()
        elif format_type == AudioFormat.OGG:
            return OGGPlayer()
        else:
            raise ValueError(f"Formato no soportado: {format_type}")


class AudioPlayer(ABC):
    """Clase base para reproductores de audio"""
    
    @abstractmethod
    def play(self, file_path: str) -> bool:
        pass


class MP3Player(AudioPlayer):
    def play(self, file_path: str) -> bool:
        print(f"🎵 Reproduciendo MP3: {file_path}")
        return True


class WAVPlayer(AudioPlayer):
    def play(self, file_path: str) -> bool:
        print(f"🎵 Reproduciendo WAV: {file_path}")
        return True


class OGGPlayer(AudioPlayer):
    def play(self, file_path: str) -> bool:
        print(f"🎵 Reproduciendo OGG: {file_path}")
        return True


# 5. DECORATOR PATTERN
class AudioPlayerDecorator(AudioPlayer):
    """Decorador base para reproductores de audio"""
    
    def __init__(self, player: AudioPlayer):
        self._player = player
    
    def play(self, file_path: str) -> bool:
        return self._player.play(file_path)


class VolumeControlDecorator(AudioPlayerDecorator):
    """Decorador para control de volumen"""
    
    def __init__(self, player: AudioPlayer, volume: float = 1.0):
        super().__init__(player)
        self.volume = volume
    
    def play(self, file_path: str) -> bool:
        print(f"🔊 Volumen ajustado a: {self.volume * 100}%")
        return self._player.play(file_path)


class EqualizerDecorator(AudioPlayerDecorator):
    """Decorador para ecualizador"""
    
    def __init__(self, player: AudioPlayer, preset: str = "normal"):
        super().__init__(player)
        self.preset = preset
    
    def play(self, file_path: str) -> bool:
        print(f"🎛️ Ecualizador: {self.preset}")
        return self._player.play(file_path)


class LoggingDecorator(AudioPlayerDecorator):
    """Decorador para logging"""
    
    def play(self, file_path: str) -> bool:
        print(f"📝 Log: Iniciando reproducción de {file_path}")
        result = self._player.play(file_path)
        print(f"📝 Log: Reproducción {'exitosa' if result else 'fallida'}")
        return result


# 6. COMMAND PATTERN
class Command(ABC):
    """Comando abstracto"""
    
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        pass


class PlayCommand(Command):
    """Comando para reproducir"""
    
    def __init__(self, player: MusicPlayer, song: str):
        self.player = player
        self.song = song
        self.previous_state = None
    
    def execute(self) -> bool:
        self.previous_state = {
            'song': self.player.current_song,
            'playing': self.player.is_playing
        }
        self.player.play(self.song)
        return True
    
    def undo(self) -> bool:
        if self.previous_state:
            if self.previous_state['playing']:
                self.player.play(self.previous_state['song'])
            else:
                self.player.pause()
        return True


class PauseCommand(Command):
    """Comando para pausar"""
    
    def __init__(self, player: MusicPlayer):
        self.player = player
        self.was_playing = False
    
    def execute(self) -> bool:
        self.was_playing = self.player.is_playing
        if self.was_playing:
            self.player.pause()
        return True
    
    def undo(self) -> bool:
        if self.was_playing:
            self.player.play(self.player.current_song)
        return True


class CommandInvoker:
    """Invocador de comandos"""
    
    def __init__(self):
        self.history: List[Command] = []
    
    def execute_command(self, command: Command) -> bool:
        if command.execute():
            self.history.append(command)
            return True
        return False
    
    def undo_last(self) -> bool:
        if self.history:
            command = self.history.pop()
            return command.undo()
        return False


# 7. CHAIN OF RESPONSIBILITY PATTERN
class GestureHandler(ABC):
    """Manejador abstracto de gestos"""
    
    def __init__(self):
        self._next_handler: Optional['GestureHandler'] = None
    
    def set_next(self, handler: 'GestureHandler') -> 'GestureHandler':
        self._next_handler = handler
        return handler
    
    def handle(self, gesture: str, player: MusicPlayer) -> bool:
        if self._next_handler:
            return self._next_handler.handle(gesture, player)
        return False


class CloseGestureHandler(GestureHandler):
    """Manejador para gesto Close"""
    
    def handle(self, gesture: str, player: MusicPlayer) -> bool:
        if gesture == "Close":
            if player.is_playing:
                player.pause()
            else:
                player.play(player.current_song or "default")
            return True
        return super().handle(gesture, player)


class NextGestureHandler(GestureHandler):
    """Manejador para gesto Next"""
    
    def handle(self, gesture: str, player: MusicPlayer) -> bool:
        if gesture == "Next":
            print("⏭️ Siguiente canción")
            return True
        return super().handle(gesture, player)


class PreviousGestureHandler(GestureHandler):
    """Manejador para gesto Previous"""
    
    def handle(self, gesture: str, player: MusicPlayer) -> bool:
        if gesture == "Previous":
            print("⏮️ Canción anterior")
            return True
        return super().handle(gesture, player)


# Función para configurar la cadena de responsabilidad
def setup_gesture_handlers() -> GestureHandler:
    """Configura la cadena de manejadores de gestos"""
    close_handler = CloseGestureHandler()
    next_handler = NextGestureHandler()
    previous_handler = PreviousGestureHandler()
    
    close_handler.set_next(next_handler).set_next(previous_handler)
    return close_handler
