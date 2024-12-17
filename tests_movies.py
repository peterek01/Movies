from storage_json import StorageJson
from movie_app import MovieApp
from storage_csv import StorageCsv


# john_storage = StorageJson('john.json')
john_storage = StorageCsv('john.csv')
# peter_storage = StorageJson('peter.json')
# johanna_storage = StorageJson('johanna.json')

john_app = MovieApp(john_storage)
# john_app = MovieApp(john_storage)
# peter_app = MovieApp(peter_storage)
# johanna_app = MovieApp(johanna_storage)

print("John's App:")
john_app.run()
#
# print("Peter's App:")
# peter_app.run()
#
# print("Johanna's App:")
# johanna_app.run()

print("Adding movies...")
john_storage.add_movie("The Matrix", 1999, 8.7, "https://example.com/matrix.jpg")
john_storage.add_movie("Inception", 2010, 8.8, "https://example.com/inception.jpg")

# print("\nMovies:")
# print(john_storage.list_movies())
#
# print("\nUpdating 'The Matrix' rating...")
# john_storage.update_movie("The Matrix", 9.0)
# print(john_storage.list_movies())

# print("\nDeleting 'Inception'...")
# john_storage.delete_movie("Inception")
# print(john_storage.list_movies())
