from istorage import IStorage
import json
import os


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initialize the storage with a file path.
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump({}, file)

    def list_movies(self):
        """
        List all movies in the storage.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_movie(self, title, year, rating, poster):
        """
        Add a movie to the storage.
        """
        movies = self.list_movies()
        if title in movies:
            raise ValueError(f"The movie '{title}' already exists.")
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Delete a movie by its title from the storage.

        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(f"Movie '{title}' has been successfully removed.")
        else:
            print(f"Error: Movie '{title}' not found in the database.")

    def update_movie(self, title, rating):
        """
        Update the rating of a movie in the storage.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
            print(f"Rating for '{title}' has been updated to {rating}.")
        else:
            raise ValueError(f"The movie '{title}' does not exist.")

    def _save_movies(self, movies):
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)
