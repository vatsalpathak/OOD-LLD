# Question:
# Design a Library Management System that supports:
# - Adding books and multiple copies of each book
# - Registering users who can borrow books
# - Searching books by title or author
# - Borrowing available copies of a book by users, tracking borrowed copies
# - Returning borrowed copies by users, updating availability accordingly


import uuid
from datetime import datetime
class Book:
    def __init__(self,title,author) -> None:
        self.isbn = uuid.uuid4()
        self.title = title
        self.author = author

class BookCopy:
    def __init__(self,book:Book) -> None:
        self.copy_id = (uuid.uuid4())
        self.book = book
        self.is_borrowed = False

class User:
    def __init__(self,name) -> None:
        self.user_id = (uuid.uuid4())
        self.name = name
        self.borrowed_books = []

class BorrowedRecord:
    def __init__(self, user:User,book_copy, date) -> None:
        self.user = user
        self.book_copy = book_copy
        self.borrow_date = date


class Library:
    def __init__(self):
        self.books = []
        self.copies = []
        self.users = []
        self.borrow_records = []

    def add_book(self,title,author):
        book = Book(title,author)
        self.books.append(book)
        return book

    def add_copy(self,book,copy_count):
        for _ in range(copy_count):
            copy = BookCopy(book)
            self.copies.append(copy)
        
    def register_user(self,name):
        user = User(name)
        self.users.append(user)
        return user
    
    def search_book(self, title=None, author=None):
        result = []
        for book in self.books:
            if (title and title.lower() in book.title.lower() or 
                (author and author.lower() in book.author.lower())):
                result.append(book)
        return result
    
    def borrow_book(self, user, book_title):
        for copy in self.copies:
            if (copy.book.title.lower() == book_title.lower()) and not copy.is_borrowed:
                copy.is_borrowed = True
                user.borrowed_books.append(copy)
                record = BorrowedRecord(user, copy, datetime.now())
                self.borrow_records.append(record)
                print(f"{user.name} borrowed '{copy.book.title}' (CopyID: {copy.copy_id})")
                return
        print(f"No available copy found for '{book_title}'")
    
    def return_book(self,user,copy_id):
        for copy in user.borrowed_books:
            if str(copy.copy_id) == str(copy_id):
                copy.is_borrowed = False
                user.borrowed_books.remove(copy)
                print(f"{user.name} returned '{copy.book.title}' (CopyID: {copy.copy_id})")
                return
        print(f"No borrowed book with CopyID {copy_id} found for user {user.name}")


if __name__ == "__main__":
    library = Library()

    # Add books and copies
    book1 = library.add_book("To Kill a Mockingbird", "Harper Lee")
    book2 = library.add_book("Pride and Prejudice", "Jane Austen")

    library.add_copy(book1, 1)
    library.add_copy(book2, 2)

    # Register users
    bob = library.register_user("Bob")

    # Search for a book
    found = library.search_book(title="Pride")
    print("\nSearch Results:")
    for book in found:
        print(f"- {book.title} by {book.author}")

    # Bob borrows a copy of "Pride and Prejudice"
    library.borrow_book(bob, "Pride and Prejudice")

    # Bob borrows another copy (should succeed)
    library.borrow_book(bob, "Pride and Prejudice")

    # Bob tries to borrow again (should fail as only 2 copies exist)
    library.borrow_book(bob, "Pride and Prejudice")

    # Bob returns one copy
    if bob.borrowed_books:
        library.return_book(bob, bob.borrowed_books[0].copy_id)
