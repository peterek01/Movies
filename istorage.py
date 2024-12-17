from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface for storage management of movies.
    This class defines the blueprint for a storage system that can list, add, delete,
    and update movies.
    """

    @abstractmethod
    def list_movies(self):
        """List all movies in the storage."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Add a new movie to the storage."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Delete a movie from the storage."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Update the rating of a movie in the storage."""
        pass
