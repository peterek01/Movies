from storage.istorage import IStorage
import json
import os


class StorageJson(IStorage):
    """
    Storage class for managing movies using JSON files.
    """
    def __init__(self, file_path):
        """
        Initialize the StorageJson with a file path inside the 'data' directory.
        """
        self.data_folder = "data"
        self.file_path = os.path.join(self.data_folder, file_path)

        # Create 'data' folder if it doesn't exist
        os.makedirs(self.data_folder, exist_ok=True)

        # Create file if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)

    def list_movies(self):
        """
        List all movies in the storage file.

        Returns:
            dict: A dictionary of movies with titles as keys and details as values.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the storage file.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): URL or path to the poster.
        """
        movies = self.list_movies()
        if title in movies:
            raise ValueError(f"The movie '{title}' already exists.")
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Delete a movie from the storage file.

        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"The movie '{title}' does not exist.")
        del movies[title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Update the rating of a movie in the storage file.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating.
        """
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"The movie '{title}' does not exist.")
        movies[title]['rating'] = rating
        self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Save the movie data to the JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)
