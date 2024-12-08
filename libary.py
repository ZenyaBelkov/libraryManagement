import random
import json
from typing import List

# Global list to store all book objects
book_list: List['Book'] = []


# Define the Book class to represent a book entity
class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str):
        """
        Initializes a new book instance with the given details.

        :param id: Unique identifier for the book
        :param title: Title of the book
        :param author: Author of the book
        :param year: Year of publication
        :param status: Availability status of the book (e.g., "Available")
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status


def load_books() -> None:
    """
    Loads books from the 'books.json' file into the global book_list.
    If the file does not exist or the data is invalid, a message is printed.
    """
    try:
        with open("books.json", "r") as file:
            data = json.load(file)
            for book_data in data:
                book = Book(book_data["id"], book_data["title"], book_data["author"], book_data["year"],
                            book_data["status"])
                book_list.append(book)
    except FileNotFoundError:
        print("No previous data found, starting with an empty library.")
    except json.JSONDecodeError:
        print("Error reading the book data.")


def save_books() -> None:
    """
    Saves the current state of the book_list to the 'books.json' file in JSON format.
    """
    data = []
    for book in book_list:
        data.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "status": book.status
        })
    with open("books.json", "w") as file:
        json.dump(data, file, indent=4)


def add_book() -> None:
    """
    Prompts the user to enter details for a new book, validates the input,
    and adds the book to the library's book_list with a unique ID and default status.
    """
    book_title = str(input("Enter the title of the book: "))

    while True:
        book_author = input("Enter the author of the book: ")
        if book_author.replace(" ", "").isalpha():
            break
        else:
            print("Invalid input. Author's name must contain only letters. Please try again.")

    while True:
        try:
            book_year = int(input("Enter the year of the book: "))
            break
        except ValueError:
            print("Invalid input. Year must be a number. Please try again")

    book_status = "Available"
    book_id = random.randint(1000, 9999)

    book = Book(book_id, book_title, book_author, book_year, book_status)
    book_list.append(book)
    print(f"Your book is {book_status} now. Book id is {book_id}.")


def delete_book() -> None:
    """
    Prompts the user to enter the ID of a book to delete. Validates the input and removes the book from the list.
    If no books exist, prints an appropriate message.
    """
    if not book_list:
        print("There are no books to delete now. Please add the book if you need.")
        return

    while True:
        try:
            book_id = int(input("Please enter the book id to delete: "))
            for book in book_list:
                if book.id == book_id:
                    book_list.remove(book)
                    print(f"The book with id {book_id} has been deleted.")
                    return

            print("There is no book with such id. Please try again")
        except ValueError:
            print("Invalid input. Book id must be a number. Please try again")


def find_book() -> None:
    """
    Allows the user to search for books by title, author, or year.
    If no books match the search criteria, prints an appropriate message.
    """
    if not book_list:
        print("There are no books to find now. Please add the book first.")
        return

    print("Please enter the way you want to find the book: \n"
          "1. Title \n"
          "2. Author \n"
          "3. Year \n")
    choice = input("Enter your choice: 1/2/3 \n")
    while True:
        if choice == '1':
            key_word = str(input("Enter the title of the book: "))
            for book in book_list:
                if book.title == key_word:
                    print(
                        f"Title found '{book.title}' \n "
                        f"ID          '{book.id}'    \n "
                        f"Author      '{book.author}'\n "
                        f"Year        '{book.year}'  \n "
                        f"Status:     '{book.status}'\n")
                    return
            print("No book found with this title. Please try again")

        elif choice == '2':
            while True:
                key_word = input("Enter the author of the book: ")
                if not key_word.replace(" ", "").isalpha():
                    print("Invalid input. Author's name must contain only letters. Please try again.")
                    continue

                found = False
                for book in book_list:
                    if book.author == key_word:
                        print(
                            f"Author found '{book.author}' \n "
                            f"ID           '{book.id}'     \n "
                            f"Title        '{book.title}'  \n "
                            f"Year         '{book.year}'   \n "
                            f"Status:      '{book.status}' \n")
                        found = True
                if found:
                    return
                else:
                    print("No book found with this author. Please try again.")

        elif choice == '3':
            while True:
                try:
                    key_word = int(input("Enter the year of the book: ").strip())
                    for book in book_list:
                        if book.year == key_word:
                            print(
                                f"Year found '{book.year}'   \n "
                                f"ID         '{book.id}'     \n "
                                f"Title      '{book.title}'  \n "
                                f"Author     '{book.author}' \n "
                                f"Status:    '{book.status}' \n")
                            return
                    print("No book found with this year. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid year.")

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


def show_all_books() -> None:
    """
    Displays a list of all books in the library, including their ID, title, author, year, and status.
    If no books are available, prints an appropriate message.
    """
    if not book_list:
        print("There are no books in the library.")
        return

    print("List of all books in the library:")
    for book in book_list:
        print(
            f"ID:     '{book.id}'     \n"
            f"Title:  '{book.title}'  \n"
            f"Author: '{book.author}' \n"
            f"Year:   '{book.year}'   \n"
            f"Status: '{book.status}' \n"
        )


def status_change() -> None:
    """
    Allows the user to change the status of a book to either 'Available' or 'Borrowed'.
    If the book does not exist, an appropriate message is printed.
    """
    if not book_list:
        print("There are no books in the library to update. Please add some books first.")
        return

    while True:
        try:
            key_word = int(input("Enter the ID of the book to update its status: "))
            for book in book_list:
                if book.id == key_word:
                    print(f"Current status of the book '{book.title}' is '{book.status}'.")
                    new_status = input("Enter the new status ('Available' or 'Borrowed'): ")
                    if new_status in ["Available", "Borrowed"]:
                        book.status = new_status
                        print(f"The status of the book '{book.title}' has been updated to '{book.status}'.")
                        return
                    else:
                        print("Invalid status. Please enter 'Available' or 'Borrowed'.")
            else:
                print("No book found with the given ID. Please try again.")
        except ValueError:
            print("Invalid input. Book ID must be a number. Please try again.")


def main() -> None:
    """
    Main function that drives the application and displays the menu for the user to choose from various actions.
    The function keeps running until the user chooses to exit.
    """
    load_books()

    print("Welcome to the library management database! \n"
          "Please choose what you want to do: \n"
          "Add the book      (type Add) \n"
          "Delete the book   (type Delete) \n"
          "Find the book     (type Find) \n"
          "Show all books    (type Show) \n")

    while True:
        print("Library Management System")
        print("Choose an action:")
        print("1. Add books")
        print("2. Delete books")
        print("3. Find books")
        print("4. Show all books")
        print("5. Change book status")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            while True:
                add_book()
                cont = input("Do you want to add another book? (yes/no): ")
                if cont != 'yes':
                    break

        elif choice == '2':
            while True:
                delete_book()
                if not book_list:
                    print("No books left to delete.")
                    break
                cont = input("Do you want to delete another book? (yes/no): ")
                if cont != 'yes':
                    break

        elif choice == '3':
            while True:
                find_book()
                if not book_list:
                    print("No books in the library to search.")
                    break
                cont = input("Do you want to search for another book? (yes/no): ")
                if cont != 'yes':
                    break

        elif choice == '4':
            show_all_books()

        elif choice == '5':
            while True:
                status_change()
                if not book_list:
                    print("No books in the library to update.")
                    break
                cont = input("Do you want to change the status of another book? (yes/no): ")
                if cont != 'yes':
                    break

        elif choice == '6':
            print("Exiting the library management system. Goodbye!")
            save_books()
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
