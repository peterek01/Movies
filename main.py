from storage_json import StorageJson
from movie_app import MovieApp
from storage_csv import StorageCsv


def main():
    # john_storage = StorageJson('john.json')
    john_storage = StorageCsv('john.csv')
    # peter_storage = StorageJson('peter.json')
    # johanna_storage = StorageJson('johanna.json')
    #
    # john_app = MovieApp(john_storage)
    john_app = MovieApp(john_storage)
    # peter_app = MovieApp(peter_storage)
    # johanna_app = MovieApp(johanna_storage)
    #
    print("Welcome to the Movie App!")
    print("")
    print("John's App:")
    john_app.run()
    #
    # print("Peter's App:")
    # peter_app.run()
    #
    # print("Johanna's App:")
    # johanna_app.run()


if __name__ == "__main__":
    main()
