"""
Patrones de diseño Django
"""
from django.db import models
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from typing import Dict, Any, List
import json


# 1. REPOSITORY PATTERN
class SongRepository:
    """Repository para manejo de canciones"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self):
        return self.model_class.objects.all()
    
    def get_by_id(self, song_id):
        return get_object_or_404(self.model_class, id=song_id)
    
    def create(self, **kwargs):
        return self.model_class.objects.create(**kwargs)
    
    def update(self, song_id, **kwargs):
        song = self.get_by_id(song_id)
        for key, value in kwargs.items():
            setattr(song, key, value)
        song.save()
        return song
    
    def delete(self, song_id):
        song = self.get_by_id(song_id)
        song.delete()
        return True
    
    def search(self, query):
        return self.model_class.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )


class PlaylistRepository:
    """Repository para manejo de playlists"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_user_playlists(self, user):
        return self.model_class.objects.filter(user=user)
    
    def add_song_to_playlist(self, playlist_id, song_id):
        playlist = get_object_or_404(self.model_class, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)
        playlist.songs.add(song)
        return playlist


# 2. SERVICE LAYER PATTERN
class MusicService:
    """Servicio para lógica de negocio de música"""
    
    def __init__(self, song_repository, playlist_repository):
        self.song_repository = song_repository
        self.playlist_repository = playlist_repository
    
    def create_playlist(self, user, name, description=""):
        """Crea una nueva playlist"""
        return self.playlist_repository.create(
            user=user,
            name=name,
            description=description
        )
    
    def add_song_to_playlist(self, playlist_id, song_id):
        """Añade una canción a una playlist"""
        return self.playlist_repository.add_song_to_playlist(playlist_id, song_id)
    
    def get_user_music_stats(self, user):
        """Obtiene estadísticas de música del usuario"""
        playlists = self.playlist_repository.get_user_playlists(user)
        total_songs = sum(playlist.songs.count() for playlist in playlists)
        
        return {
            'total_playlists': playlists.count(),
            'total_songs': total_songs,
            'favorite_genre': self._get_favorite_genre(user)
        }
    
    def _get_favorite_genre(self, user):
        """Obtiene el género favorito del usuario"""
        # Lógica para determinar género favorito
        return "Pop"


# 3. FACTORY PATTERN para Vistas
class ViewFactory:
    """Factory para crear vistas dinámicamente"""
    
    @staticmethod
    def create_crud_views(model_class, template_prefix=""):
        """Crea vistas CRUD para un modelo"""
        
        class BaseListView(ListView):
            model = model_class
            template_name = f"{template_prefix}_list.html"
            context_object_name = 'objects'
            paginate_by = 20
        
        class BaseCreateView(CreateView):
            model = model_class
            template_name = f"{template_prefix}_form.html"
            fields = '__all__'
            
            def get_success_url(self):
                return f"/{template_prefix}/"
        
        class BaseUpdateView(UpdateView):
            model = model_class
            template_name = f"{template_prefix}_form.html"
            fields = '__all__'
            
            def get_success_url(self):
                return f"/{template_prefix}/"
        
        class BaseDeleteView(DeleteView):
            model = model_class
            template_name = f"{template_prefix}_confirm_delete.html"
            
            def get_success_url(self):
                return f"/{template_prefix}/"
        
        return {
            'list': BaseListView,
            'create': BaseCreateView,
            'update': BaseUpdateView,
            'delete': BaseDeleteView
        }


# 4. STRATEGY PATTERN para Filtros
class FilterStrategy:
    """Estrategia base para filtros"""
    
    def apply(self, queryset):
        return queryset


class DateRangeFilter(FilterStrategy):
    """Filtro por rango de fechas"""
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
    
    def apply(self, queryset):
        return queryset.filter(
            created_at__range=[self.start_date, self.end_date]
        )


class GenreFilter(FilterStrategy):
    """Filtro por género"""
    
    def __init__(self, genre):
        self.genre = genre
    
    def apply(self, queryset):
        return queryset.filter(genre=self.genre)


class SearchFilter(FilterStrategy):
    """Filtro por búsqueda"""
    
    def __init__(self, search_term):
        self.search_term = search_term
    
    def apply(self, queryset):
        return queryset.filter(
            Q(title__icontains=self.search_term) |
            Q(artist__icontains=self.search_term)
        )


class FilterContext:
    """Contexto que usa estrategias de filtrado"""
    
    def __init__(self, queryset):
        self.queryset = queryset
        self.filters = []
    
    def add_filter(self, filter_strategy: FilterStrategy):
        self.filters.append(filter_strategy)
    
    def apply_filters(self):
        result = self.queryset
        for filter_strategy in self.filters:
            result = filter_strategy.apply(result)
        return result


# 5. DECORATOR PATTERN para Vistas
def cache_view(timeout=300):
    """Decorador para cachear vistas"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            cache_key = f"view_{view_func.__name__}_{request.GET.urlencode()}"
            cached_response = cache.get(cache_key)
            
            if cached_response:
                return cached_response
            
            response = view_func(request, *args, **kwargs)
            cache.set(cache_key, response, timeout)
            return response
        return wrapper
    return decorator


def require_ajax(view_func):
    """Decorador para requerir requests AJAX"""
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'AJAX request required'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper


# 6. OBSERVER PATTERN para Modelos
class ModelObserver:
    """Observador para cambios en modelos"""
    
    def model_saved(self, instance, created):
        pass
    
    def model_deleted(self, instance):
        pass


class SongObserver(ModelObserver):
    """Observador específico para canciones"""
    
    def model_saved(self, instance, created):
        if created:
            print(f"🎵 Nueva canción creada: {instance.title}")
        else:
            print(f"🎵 Canción actualizada: {instance.title}")
    
    def model_deleted(self, instance):
        print(f"🗑️ Canción eliminada: {instance.title}")


# 7. COMMAND PATTERN para Operaciones
class Command:
    """Comando abstracto"""
    
    def execute(self):
        pass
    
    def undo(self):
        pass


class AddSongToPlaylistCommand(Command):
    """Comando para añadir canción a playlist"""
    
    def __init__(self, playlist_id, song_id):
        self.playlist_id = playlist_id
        self.song_id = song_id
        self.was_added = False
    
    def execute(self):
        playlist = get_object_or_404(Playlist, id=self.playlist_id)
        song = get_object_or_404(Song, id=self.song_id)
        playlist.songs.add(song)
        self.was_added = True
        return True
    
    def undo(self):
        if self.was_added:
            playlist = get_object_or_404(Playlist, id=self.playlist_id)
            song = get_object_or_404(Song, id=self.song_id)
            playlist.songs.remove(song)
            return True
        return False


class CommandInvoker:
    """Invocador de comandos"""
    
    def __init__(self):
        self.history = []
    
    def execute_command(self, command: Command):
        if command.execute():
            self.history.append(command)
            return True
        return False
    
    def undo_last(self):
        if self.history:
            command = self.history.pop()
            return command.undo()
        return False


# 8. TEMPLATE METHOD PATTERN
class BaseMusicView:
    """Clase base con template method"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_music_context())
        return context
    
    def get_music_context(self):
        """Template method para contexto de música"""
        return {
            'current_song': self.get_current_song(),
            'playlist': self.get_playlist(),
            'user_preferences': self.get_user_preferences()
        }
    
    def get_current_song(self):
        """Hook method - debe ser implementado por subclases"""
        raise NotImplementedError
    
    def get_playlist(self):
        """Hook method - debe ser implementado por subclases"""
        raise NotImplementedError
    
    def get_user_preferences(self):
        """Hook method - implementación por defecto"""
        return {}


class MusicListView(BaseMusicView, ListView):
    """Vista de lista con template method"""
    
    def get_current_song(self):
        # Implementación específica
        return None
    
    def get_playlist(self):
        # Implementación específica
        return []


# 9. ADAPTER PATTERN
class ExternalMusicAPI:
    """API externa de música"""
    
    def get_song_info(self, song_id):
        return {
            'id': song_id,
            'title': f"Song {song_id}",
            'artist': "Unknown Artist",
            'duration': 180
        }


class MusicAPIAdapter:
    """Adaptador para API externa"""
    
    def __init__(self, external_api):
        self.external_api = external_api
    
    def get_song(self, song_id):
        """Adapta la respuesta de la API externa"""
        external_data = self.external_api.get_song_info(song_id)
        
        # Adaptar a formato interno
        return {
            'title': external_data['title'],
            'artist': external_data['artist'],
            'duration_seconds': external_data['duration']
        }


# 10. FACADE PATTERN
class MusicFacade:
    """Facade para operaciones complejas de música"""
    
    def __init__(self):
        self.song_repository = SongRepository(Song)
        self.playlist_repository = PlaylistRepository(Playlist)
        self.music_service = MusicService(
            self.song_repository, 
            self.playlist_repository
        )
    
    def create_complete_playlist(self, user, name, songs_data):
        """Crea una playlist completa con canciones"""
        # Crear playlist
        playlist = self.music_service.create_playlist(user, name)
        
        # Añadir canciones
        for song_data in songs_data:
            song = self.song_repository.create(**song_data)
            self.music_service.add_song_to_playlist(playlist.id, song.id)
        
        return playlist
    
    def get_user_dashboard_data(self, user):
        """Obtiene todos los datos para el dashboard del usuario"""
        stats = self.music_service.get_user_music_stats(user)
        playlists = self.playlist_repository.get_user_playlists(user)
        
        return {
            'stats': stats,
            'playlists': playlists,
            'recent_activity': self._get_recent_activity(user)
        }
    
    def _get_recent_activity(self, user):
        """Obtiene actividad reciente del usuario"""
        # Implementación para obtener actividad reciente
        return []
