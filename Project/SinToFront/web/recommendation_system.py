"""
Sistema de recomendaciones de música con patrones de diseño
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
import random
import time
from django.db import models
from django.contrib.auth.models import User


# 1. STRATEGY PATTERN para Algoritmos de Recomendación
class RecommendationStrategy(ABC):
    """Estrategia base para algoritmos de recomendación"""
    
    @abstractmethod
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class CollaborativeFilteringStrategy(RecommendationStrategy):
    """Filtrado colaborativo"""
    
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Simular filtrado colaborativo
        similar_users = self._find_similar_users(user)
        recommendations = []
        
        for similar_user in similar_users:
            user_songs = self._get_user_songs(similar_user)
            recommendations.extend(user_songs)
        
        return self._remove_duplicates(recommendations)[:10]
    
    def _find_similar_users(self, user):
        # Lógica para encontrar usuarios similares
        return [f"user_{i}" for i in range(3)]
    
    def _get_user_songs(self, user_id):
        # Lógica para obtener canciones del usuario
        return [
            {"title": f"Song {i}", "artist": f"Artist {i}", "score": random.uniform(0.7, 1.0)}
            for i in range(5)
        ]
    
    def _remove_duplicates(self, recommendations):
        seen = set()
        unique = []
        for rec in recommendations:
            key = (rec["title"], rec["artist"])
            if key not in seen:
                seen.add(key)
                unique.append(rec)
        return unique


class ContentBasedStrategy(RecommendationStrategy):
    """Recomendaciones basadas en contenido"""
    
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        user_preferences = self._get_user_preferences(user)
        current_song = context.get('current_song')
        
        if current_song:
            return self._recommend_similar_songs(current_song, user_preferences)
        else:
            return self._recommend_by_preferences(user_preferences)
    
    def _get_user_preferences(self, user):
        # Lógica para obtener preferencias del usuario
        return {
            'genres': ['Pop', 'Rock', 'Jazz'],
            'artists': ['Artist A', 'Artist B'],
            'mood': 'happy'
        }
    
    def _recommend_similar_songs(self, current_song, preferences):
        # Lógica para recomendar canciones similares
        return [
            {"title": f"Similar to {current_song}", "artist": "Similar Artist", "score": 0.9}
            for _ in range(5)
        ]
    
    def _recommend_by_preferences(self, preferences):
        # Lógica para recomendar por preferencias
        return [
            {"title": f"Recommended Song {i}", "artist": f"Artist {i}", "score": 0.8}
            for i in range(5)
        ]


class HybridStrategy(RecommendationStrategy):
    """Estrategia híbrida que combina múltiples algoritmos"""
    
    def __init__(self, strategies: List[RecommendationStrategy], weights: List[float]):
        self.strategies = strategies
        self.weights = weights
    
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        all_recommendations = []
        
        for strategy, weight in zip(self.strategies, self.weights):
            recommendations = strategy.recommend(user, context)
            # Aplicar peso a las recomendaciones
            for rec in recommendations:
                rec['score'] *= weight
            all_recommendations.extend(recommendations)
        
        # Combinar y ordenar recomendaciones
        return self._merge_recommendations(all_recommendations)
    
    def _merge_recommendations(self, recommendations):
        # Agrupar por canción y sumar scores
        song_scores = {}
        for rec in recommendations:
            key = (rec["title"], rec["artist"])
            if key in song_scores:
                song_scores[key]["score"] += rec["score"]
            else:
                song_scores[key] = rec
        
        # Ordenar por score y retornar top 10
        sorted_recommendations = sorted(
            song_scores.values(), 
            key=lambda x: x["score"], 
            reverse=True
        )
        return sorted_recommendations[:10]


# 2. FACTORY PATTERN para Crear Estrategias
class RecommendationStrategyFactory:
    """Factory para crear estrategias de recomendación"""
    
    @staticmethod
    def create_strategy(strategy_type: str) -> RecommendationStrategy:
        if strategy_type == "collaborative":
            return CollaborativeFilteringStrategy()
        elif strategy_type == "content":
            return ContentBasedStrategy()
        elif strategy_type == "hybrid":
            collaborative = CollaborativeFilteringStrategy()
            content = ContentBasedStrategy()
            return HybridStrategy([collaborative, content], [0.6, 0.4])
        else:
            raise ValueError(f"Estrategia no soportada: {strategy_type}")


# 3. OBSERVER PATTERN para Actualizar Recomendaciones
class RecommendationObserver(ABC):
    """Observador para cambios en recomendaciones"""
    
    @abstractmethod
    def on_recommendations_updated(self, user, recommendations):
        pass


class CacheObserver(RecommendationObserver):
    """Observador que actualiza caché"""
    
    def on_recommendations_updated(self, user, recommendations):
        cache_key = f"recommendations_{user.id}"
        # Actualizar caché con nuevas recomendaciones
        print(f"🔄 Actualizando caché para usuario {user.id}")


class NotificationObserver(RecommendationObserver):
    """Observador que envía notificaciones"""
    
    def on_recommendations_updated(self, user, recommendations):
        print(f"📧 Enviando notificaciones a usuario {user.id}")


# 4. COMMAND PATTERN para Operaciones de Recomendación
class RecommendationCommand(ABC):
    """Comando abstracto para operaciones de recomendación"""
    
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        pass


class UpdateUserPreferencesCommand(RecommendationCommand):
    """Comando para actualizar preferencias del usuario"""
    
    def __init__(self, user, preferences):
        self.user = user
        self.new_preferences = preferences
        self.old_preferences = None
    
    def execute(self) -> bool:
        # Guardar preferencias anteriores
        self.old_preferences = self._get_user_preferences(self.user)
        
        # Actualizar preferencias
        self._update_preferences(self.user, self.new_preferences)
        return True
    
    def undo(self) -> bool:
        if self.old_preferences:
            self._update_preferences(self.user, self.old_preferences)
            return True
        return False
    
    def _get_user_preferences(self, user):
        # Lógica para obtener preferencias actuales
        return {"genres": ["Pop"], "artists": []}
    
    def _update_preferences(self, user, preferences):
        # Lógica para actualizar preferencias
        print(f"🔄 Actualizando preferencias para {user.username}")


class GenerateRecommendationsCommand(RecommendationCommand):
    """Comando para generar recomendaciones"""
    
    def __init__(self, user, strategy, context):
        self.user = user
        self.strategy = strategy
        self.context = context
        self.generated_recommendations = None
    
    def execute(self) -> bool:
        self.generated_recommendations = self.strategy.recommend(self.user, self.context)
        return True
    
    def undo(self) -> bool:
        # No se puede deshacer la generación de recomendaciones
        return False


# 5. DECORATOR PATTERN para Mejorar Recomendaciones
class RecommendationDecorator(RecommendationStrategy):
    """Decorador base para recomendaciones"""
    
    def __init__(self, strategy: RecommendationStrategy):
        self.strategy = strategy
    
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.strategy.recommend(user, context)


class DiversityDecorator(RecommendationDecorator):
    """Decorador para diversificar recomendaciones"""
    
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        recommendations = self.strategy.recommend(user, context)
        return self._diversify_recommendations(recommendations)
    
    def _diversify_recommendations(self, recommendations):
        # Lógica para diversificar recomendaciones
        diversified = []
        used_artists = set()
        
        for rec in recommendations:
            if rec.get('artist') not in used_artists:
                diversified.append(rec)
                used_artists.add(rec.get('artist'))
        
        return diversified[:10]


class FreshnessDecorator(RecommendationDecorator):
    """Decorador para priorizar contenido fresco"""
    
    def recommend(self, user, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        recommendations = self.strategy.recommend(user, context)
        return self._prioritize_fresh_content(recommendations)
    
    def _prioritize_fresh_content(self, recommendations):
        # Lógica para priorizar contenido fresco
        for rec in recommendations:
            # Simular fecha de lanzamiento
            rec['release_date'] = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            rec['freshness_score'] = random.uniform(0.5, 1.0)
        
        return sorted(recommendations, key=lambda x: x['freshness_score'], reverse=True)


# 6. FACADE PATTERN para Sistema Completo
class RecommendationFacade:
    """Facade para el sistema completo de recomendaciones"""
    
    def __init__(self):
        self.strategy_factory = RecommendationStrategyFactory()
        self.observers = []
        self.command_history = []
    
    def add_observer(self, observer: RecommendationObserver):
        self.observers.append(observer)
    
    def get_recommendations(self, user, strategy_type="hybrid", context=None):
        """Obtiene recomendaciones para un usuario"""
        if context is None:
            context = {}
        
        # Crear estrategia
        strategy = self.strategy_factory.create_strategy(strategy_type)
        
        # Aplicar decoradores
        strategy = DiversityDecorator(strategy)
        strategy = FreshnessDecorator(strategy)
        
        # Generar recomendaciones
        recommendations = strategy.recommend(user, context)
        
        # Notificar observadores
        for observer in self.observers:
            observer.on_recommendations_updated(user, recommendations)
        
        return recommendations
    
    def update_user_preferences(self, user, preferences):
        """Actualiza preferencias del usuario"""
        command = UpdateUserPreferencesCommand(user, preferences)
        if command.execute():
            self.command_history.append(command)
            return True
        return False
    
    def undo_last_operation(self):
        """Deshace la última operación"""
        if self.command_history:
            command = self.command_history.pop()
            return command.undo()
        return False


# 7. SINGLETON PATTERN para Sistema Global
class GlobalRecommendationSystem:
    """Sistema global de recomendaciones (Singleton)"""
    
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
            self.facade = RecommendationFacade()
            self.facade.add_observer(CacheObserver())
            self.facade.add_observer(NotificationObserver())
            self.initialized = True
    
    def get_recommendations(self, user, **kwargs):
        return self.facade.get_recommendations(user, **kwargs)
    
    def update_preferences(self, user, preferences):
        return self.facade.update_user_preferences(user, preferences)


# 8. BUILDER PATTERN para Configurar Sistema
class RecommendationSystemBuilder:
    """Builder para configurar el sistema de recomendaciones"""
    
    def __init__(self):
        self.strategies = []
        self.weights = []
        self.decorators = []
        self.observers = []
    
    def add_strategy(self, strategy_type: str, weight: float = 1.0):
        self.strategies.append(strategy_type)
        self.weights.append(weight)
        return self
    
    def add_decorator(self, decorator_type: str):
        self.decorators.append(decorator_type)
        return self
    
    def add_observer(self, observer_type: str):
        self.observers.append(observer_type)
        return self
    
    def build(self):
        """Construye el sistema de recomendaciones"""
        facade = RecommendationFacade()
        
        # Configurar observadores
        for observer_type in self.observers:
            if observer_type == "cache":
                facade.add_observer(CacheObserver())
            elif observer_type == "notification":
                facade.add_observer(NotificationObserver())
        
        return facade


# Ejemplo de uso del sistema
def example_usage():
    """Ejemplo de uso del sistema de recomendaciones"""
    
    # Crear sistema usando Builder
    builder = RecommendationSystemBuilder()
    system = (builder
              .add_strategy("collaborative", 0.6)
              .add_strategy("content", 0.4)
              .add_decorator("diversity")
              .add_decorator("freshness")
              .add_observer("cache")
              .add_observer("notification")
              .build())
    
    # Usar sistema global
    global_system = GlobalRecommendationSystem()
    
    # Simular usuario
    class MockUser:
        def __init__(self, id, username):
            self.id = id
            self.username = username
    
    user = MockUser(1, "test_user")
    
    # Obtener recomendaciones
    recommendations = global_system.get_recommendations(
        user, 
        strategy_type="hybrid",
        context={"current_song": "Song A"}
    )
    
    print("🎵 Recomendaciones generadas:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['artist']} (Score: {rec.get('score', 0):.2f})")
    
    return recommendations
