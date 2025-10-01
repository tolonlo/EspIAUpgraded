"""
Interfaces para inversión de dependencias
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import numpy as np


class GestureDetectorInterface(ABC):
    """Interface para detectores de gestos"""
    
    @abstractmethod
    def detect_gesture(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Detecta gestos en una imagen
        
        Args:
            image: Imagen como array de numpy
            
        Returns:
            Dict con información del gesto detectado
        """
        pass


class AudioPlayerInterface(ABC):
    """Interface para reproductores de audio"""
    
    @abstractmethod
    def play(self, audio_path: str) -> bool:
        """Reproduce un archivo de audio"""
        pass
    
    @abstractmethod
    def pause(self) -> bool:
        """Pausa la reproducción"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Detiene la reproducción"""
        pass
    
    @abstractmethod
    def get_current_time(self) -> float:
        """Obtiene el tiempo actual de reproducción"""
        pass
    
    @abstractmethod
    def get_duration(self) -> float:
        """Obtiene la duración total del audio"""
        pass


class NotificationServiceInterface(ABC):
    """Interface para servicios de notificaciones"""
    
    @abstractmethod
    def show_success(self, message: str) -> None:
        """Muestra notificación de éxito"""
        pass
    
    @abstractmethod
    def show_error(self, message: str) -> None:
        """Muestra notificación de error"""
        pass
    
    @abstractmethod
    def show_info(self, message: str) -> None:
        """Muestra notificación informativa"""
        pass


class CacheInterface(ABC):
    """Interface para sistemas de caché"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Almacena un valor en el caché"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        pass
