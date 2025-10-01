"""
Servicio principal que usa inversión de dependencias
"""
from typing import Dict, Any
import numpy as np
from .interfaces import GestureDetectorInterface, NotificationServiceInterface, CacheInterface
from .services import MockGestureDetector, ConsoleNotificationService, InMemoryCache


class GestureControlService:
    """
    Servicio principal para control de gestos con inversión de dependencias
    """
    
    def __init__(
        self,
        gesture_detector: GestureDetectorInterface,
        notification_service: NotificationServiceInterface,
        cache_service: CacheInterface
    ):
        self.gesture_detector = gesture_detector
        self.notification_service = notification_service
        self.cache_service = cache_service
    
    def process_gesture(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Procesa una imagen para detectar gestos
        
        Args:
            image: Imagen como array de numpy
            
        Returns:
            Dict con información del gesto detectado
        """
        try:
            # Verificar caché primero
            cache_key = f"gesture_{hash(image.tobytes())}"
            cached_result = self.cache_service.get(cache_key)
            
            if cached_result:
                self.notification_service.show_info("Gesto obtenido del caché")
                return cached_result
            
            # Detectar gesto
            result = self.gesture_detector.detect_gesture(image)
            
            # Guardar en caché
            self.cache_service.set(cache_key, result, ttl=60)
            
            # Mostrar notificación
            if result['gesture_name'] != 'No detectado':
                self.notification_service.show_success(f"Gesto detectado: {result['gesture_name']}")
            else:
                self.notification_service.show_info("No se detectó gesto")
            
            return result
            
        except Exception as e:
            self.notification_service.show_error(f"Error al procesar gesto: {str(e)}")
            return {
                'gesture_name': 'Error',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_gesture_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de gestos detectados"""
        # Implementación para obtener estadísticas
        return {
            'total_gestures': 0,
            'success_rate': 0.0,
            'most_common_gesture': 'None'
        }


# Factory para crear instancias del servicio
class GestureServiceFactory:
    """Factory para crear instancias del servicio de gestos"""
    
    @staticmethod
    def create_mock_service() -> GestureControlService:
        """Crea un servicio con implementaciones mock"""
        return GestureControlService(
            gesture_detector=MockGestureDetector(),
            notification_service=ConsoleNotificationService(),
            cache_service=InMemoryCache()
        )
    
    @staticmethod
    def create_production_service() -> GestureControlService:
        """Crea un servicio para producción"""
        from .services import RealGestureDetector, ToastNotificationService, RedisCache
        
        return GestureControlService(
            gesture_detector=RealGestureDetector(),
            notification_service=ToastNotificationService(),
            cache_service=RedisCache()
        )
