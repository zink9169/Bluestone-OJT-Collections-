from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"'{self.title}' by {self.author} [{status}]"


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []
        self.limit = 0

    def can_borrow(self):
        return len(self.borrowed_books) < self.limit

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (ID: {self.user_id}) - Books: {len(self.borrowed_books)}/{self.limit}"


class Teacher(User):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.limit = 5


class Student(User):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.limit = 3


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, title, author):
        new_book = Book(title, author)
        self.books.append(new_book)
        print(f"Book added: {title}")

    def register_user(self, user):
        self.users.append(user)
        print(f"User registered: {user.name} as {user.__class__.__name__}")

    def borrow_book(self, user_id, book_title):
        user = next((u for u in self.users if u.user_id == user_id), None)
        book = next((b for b in self.books if b.title == book_title and b.is_available), None)

        if not user:
            print("User not found.")
            return
        if not book:
            print("Book not available or doesn't exist.")
            return

        if user.can_borrow():
            book.is_available = False
            user.borrowed_books.append(book)
            print(f"{user.name} successfully borrowed '{book.title}'")
        else:
            print(f"Limit reached! {user.name} cannot borrow more than {user.limit} books.")

    def return_book(self, user_id, book_title):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user:
            for book in user.borrowed_books:
                if book.title == book_title:
                    book.is_available = True
                    user.borrowed_books.remove(book)
                    print(f"Book '{book_title}' returned. (Checked for due date: {datetime.now().date()})")
                    return
        print("Record not found.")

    def show_all_books(self):
        print("\n--- Library Inventory ---")
        for book in self.books:
            print(book)

    def show_all_users(self):
        print("\n--- Registered Users ---")
        for user in self.users:
            print(user)