from istorage import IStorage
import csv
from typing import Dict


class StorageCsv(IStorage):
    """
    A storage class to manage movies using a CSV file.
    """
    def __init__(self, file_path):
        """
        Initialize the storage with a file path.

        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        List all movies from the CSV file.

        Returns:
            dict: A dictionary containing movies and their details.
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:  # type: Dict[str, str]
                    movies[row['title']] = {
                        'rating': float(row['rating']),
                        'year': int(row['year']),
                        'poster': row['poster']
                    }
        except FileNotFoundError:
            # If the file does not exist, return an empty dictionary
            pass
        return movies

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the CSV file.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): URL or path to the movie poster.
        """
        movies = self.list_movies()
        if title in movies:
            raise ValueError(f"The movie '{title}' already exists in the storage.")

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            if file.tell() == 0:
                writer.writeheader()  # Write the header if the file is empty
            writer.writerow({'title': title, 'year': year, 'rating': rating, 'poster': poster})

    def delete_movie(self, title):
        """
        Delete a movie from the CSV file.

        Args:
            title (str): The title of the movie to delete.

        Raises:
            ValueError: If the movie does not exist.
        """
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"The movie '{title}' does not exist in the storage.")

        # Rewrite the CSV file without the deleted movie
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            writer.writeheader()
            for movie_title, details in movies.items():
                if movie_title != title:
                    writer.writerow({
                        'title': movie_title,
                        'year': details['year'],
                        'rating': details['rating'],
                        'poster': details['poster']
                    })

    def update_movie(self, title, rating):
        """
        Update the rating of a movie in the CSV file.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating to set.

        Raises:
            ValueError: If the movie does not exist.
        """
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"The movie '{title}' does not exist in the storage.")

        # Update the movie's rating and rewrite the file
        movies[title]['rating'] = rating
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            writer.writeheader()
            for movie_title, details in movies.items():
                writer.writerow({
                    'title': movie_title,
                    'year': details['year'],
                    'rating': details['rating'],
                    'poster': details['poster']
                })

