from datetime import date

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.book_id} | {self.title} | {self.author} | {status}"

#encapsulation
# User class အတွင်း data ကို directly access မလျှောက်ဘဲ,
# controlled method (can_borrow()) နဲ့ပဲ access လုပ်ထားတာ
class User:
    def __init__(self, user_id, name, max_books):
        self.user_id = user_id
        self.name = name
        self.max_books = max_books
        self.borrowed_books = {}
    def can_borrow(self):
        return len(self.borrowed_books) < self.max_books

#polymorphism
# User class ကို parent class အဖြစ်သုံးထားပြီး
# Teacher နှင့် Student ကို subclass အဖြစ်ပြုလုပ်ထားပါတယ်

# inheritance
# Teacher နဲ့ Student တို့က
# user_id, name, borrowed_books, can_borrow()
# အားလုံးကို User ကနေ အမွေဆက်ခံထားတယ်
class Teacher(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, max_books=5)
class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, max_books=3)



# polymorphism
# Library class က user object ကို User type အနေနဲ့ handle လုပ်နိုင်ပြီး၊
# သုံးသူဟာ Teacher ဖြစ်ပါစေ၊ Student ဖြစ်ပါစေ, borrow_book() သို့ return_book() method တွေကို same interface နဲ့အလုပ်လုပ်နိုင်ပါတယ်။
class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)
        print("Book added successfully")

    def register_user(self, user):
        self.users.append(user)
        print("User registered successfully")

#inheritance + polymorphism
    # userကTeacher, Student ဖြစ်နိုင်
    # ဒါပေမယ့် can_borrow() ကိုတူညီတဲ့နည်းနဲ့ခေါ်နိုင်တယ်
    def borrow_book(self, user_id, book_id):
        user = self.find_user(user_id)
        book = self.find_book(book_id)
        if not user or not book:
            print("User or Book not found")
            return
        if not book.is_available:
            print("Book is already borrowed")
            return
        if not user.can_borrow():
            print("Borrow limit reached")
            return

        book.is_available = False
        user.borrowed_books[book.book_id] = date.today()
        print("Book borrowed successfully")

    # 4. Return Book
    def return_book(self, user_id, book_id):
        user = self.find_user(user_id)
        book = self.find_book(book_id)

        if book_id not in user.borrowed_books:
            print("This book was not borrowed by user")
            return

        borrow_date = user.borrowed_books.pop(book_id)
        book.is_available = True

        print("Book returned successfully")
        print(f"Borrowed Date: {borrow_date}")

    def show_books(self):
        print("All Books:")
        for book in self.books:
            print(book)

    def show_users(self):
        print("All Users:")
        for user in self.users:
            print(f"{user.user_id} | {user.name} | Max Books: {user.max_books}")

    def find_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None



