import requests
import os


class MovieApp:
    """
    A class that handles the logic of a movie management application.
    It takes a storage object that implements the IStorage interface.
    """
    OMDB_API_KEY = "2e8cb9fe"
    OMDB_API_URL = "http://www.omdbapi.com/"

    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage object.

        Args:
            storage (IStorage): An object implementing the IStorage interface.
        """
        self._storage = storage

    def _fetch_movie_data(self, title):
        """
        Fetch movie data from OMDb API.
        Args:
            title (str): The title of the movie to search for.
        Returns:
            dict: Movie data including title, year, rating, and poster URL.
        Raises:
            ValueError: If the movie is not found or API request fails.
        """
        try:
            response = requests.get(self.OMDB_API_URL, params={"t": title, "apikey": self.OMDB_API_KEY})
            if response.status_code != 200:
                raise ValueError("Failed to connect to OMDb API.")

            data = response.json()
            if data.get("Response") == "False":
                raise ValueError(f"Movie '{title}' not found.")

            return {
                "title": data.get("Title"),
                "year": int(data.get("Year", 0)),
                "rating": float(data.get("imdbRating", 0.0)),
                "poster": data.get("Poster")
            }
        except requests.RequestException:
            raise ValueError("Unable to connect to the OMDb API. Check your internet connection.")

    def _command_list_movies(self):
        """
        List all movies stored in the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available in the database.")
        else:
            print("\nMovies in the database:")
            for title, details in movies.items():
                print(f"{title} ({details['year']}), Rating: {details['rating']}, Poster: {details['poster']}")

    def _command_add_movie(self):
        """
        Add new movie to the database by fetching data from OMDb API.
        """
        title = input("Enter the movie title: ")
        try:
            movie_data = self._fetch_movie_data(title)
            self._storage.add_movie(
                title=movie_data["title"],
                year=movie_data["year"],
                rating=movie_data["rating"],
                poster=movie_data["poster"]
            )
            print(f"The movie '{movie_data['title']}' has been added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def _command_delete_movie(self):
        """
        Removes a movie from the database based on its title.
        """
        title = input("Enter the title of the movie to delete: ").strip()
        if not title:
            print("Error: Movie title cannot be empty.")
            return

        self._storage.delete_movie(title)

    def _command_update_movie(self):
        """
        Update the rating of a movie.
        """
        title = input("Enter the title of the movie to update: ")
        rating = self._get_valid_rating()

        try:
            self._storage.update_movie(title, rating)
            print(f"The rating for '{title}' has been updated to {rating}.")
        except ValueError as e:
            print(f"Error: {e}")

    def _command_movie_stats(self):
        """
        Display statistics about the movies.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to calculate statistics.")
            return

        avg_rating = sum(details['rating'] for details in movies.values()) / len(movies)
        best_movie = max(movies.items(), key=lambda x: x[1]['rating'])
        worst_movie = min(movies.items(), key=lambda x: x[1]['rating'])

        print("\nMovie Statistics:")
        print(f"Average Rating: {avg_rating:.2f}")
        print(f"Best Movie: {best_movie[0]} - Rating: {best_movie[1]['rating']}")
        print(f"Worst Movie: {worst_movie[0]} - Rating: {worst_movie[1]['rating']}")

    def _generate_website(self):
        """
        Generates an HTML page with a list of movies.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to generate the website.")
            return

        template_path = os.path.join("_static", "index_template.html")
        output_path = os.path.join("_static", "index.html")

        try:
            with open(template_path, 'r') as file:
                template = file.read()
        except FileNotFoundError:
            print(f"Template file not found at: {template_path}")
            return

        movie_html = ""
        for title, details in movies.items():
            movie_html += f'''
            <li>
                <div class="movie-item">
                    <h2>{title}</h2>
                    <p>Year: {details['year']}</p>
                    <p>Rating: {details['rating']}</p>
                    <img src="{details['poster']}" alt="{title} Poster" width="150">
                </div>
            </li>
            '''

        final_html = template.replace("__TEMPLATE_TITLE__", "My Movie Collection")
        final_html = final_html.replace("__TEMPLATE_MOVIE_GRID__", movie_html)

        with open(output_path, 'w') as file:
            file.write(final_html)

        print(f"Website generated successfully at: {output_path}")

    def _get_valid_year(self):
        """
        Helper function to get a valid year from the user.
        """
        while True:
            try:
                year = int(input("Enter the release year: "))
                return year
            except ValueError:
                print("Invalid input. Please enter a valid year.")

    def _get_valid_rating(self):
        """
        Helper function to get a valid rating from the user.
        """
        while True:
            try:
                rating = float(input("Enter the movie rating (0-10): "))
                if 0 <= rating <= 10:
                    return rating
                else:
                    print("Rating must be between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a valid rating.")

    def _exit_program(self):
        """
        Displays a goodbye message and exits the program.
        """
        print("Bye")
        exit()

    def run(self):
        """
        Launches the application. Displays the menu and handles user commands.
        """
        commands = {
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._generate_website,
            "0": self._exit_program
        }

        while True:
            print("\nMenu:")
            print("1. View Movie List")
            print("2. Add a new movie")
            print("3. Remove a movie")
            print("4. Update rating of a movie")
            print("5. View movie statistics")
            print("6. Generate HTML page with movies")
            print("0. Exit")

            try:
                choice = input("Select an option: ")
                if choice not in commands:
                    raise ValueError("Please enter a valid number between 0 and 6.")
                commands[choice]()
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

