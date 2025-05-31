# Question:
# Extend the Library Management System to include:
# - Borrowed records that track borrow date and calculate due date (14 days from borrow)
# - Display due date when a user borrows a book copy
# - View all available books with counts of available copies
# Implement borrowing and returning functionality with due date tracking.


import uuid
from datetime import datetime, timedelta
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
    def __init__(self, user:User,book_copy, borrow_date: datetime) -> None:
        self.user = user
        self.book_copy = book_copy
        self.borrow_date = borrow_date
        self.due_date = borrow_date + timedelta(days=14)


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
                print(f"{user.name} borrowed '{book_title}' (CopyID: {copy.copy_id}) - Due by {record.due_date.strftime('%Y-%m-%d')}")
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

    def view_available_books(self):
        availability = {}
        for copy in self.copies:
            if not copy.is_borrowed:
                book = copy.book
                key = (book.title, book.author)
                availability[key] = availability.get(key, 0) + 1

        print("\n📚 Available Books:")
        for (title, author), count in availability.items():
            print(f"- {title} by {author} ({count} copies available)")

if __name__ == "__main__":
    library = Library()
    b1 = library.add_book("1984", "George Orwell")
    library.add_copy(b1, 3)

    alice = library.register_user("Alice")

    library.view_available_books()  # Before borrow

    library.borrow_book(alice, "1984")

    library.view_available_books()  # After borrow
