import json
import os
from .book import Book
from .member import Member

BOOK_FILE = "data/books.json"
MEMBER_FILE = "data/members.json"

class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.load_data()

    def add_book(self, book):
        self.books[book.isbn] = book

    def register_member(self, member):
        self.members[member.member_id] = member

    def borrow_book(self, isbn, member_id):
        book = self.books.get(isbn)
        member = self.members.get(member_id)

        if not book or not member:
            return "Invalid book or member ID"

        if not member.can_borrow():
            return "Member has reached borrowing limit"

        success, msg = book.check_out(member_id)
        if success:
            member.borrow_book(isbn)
        return msg

    def return_book(self, isbn):
        book = self.books.get(isbn)
        if not book or book.available:
            return "Invalid return"

        member = self.members.get(book.borrowed_by)
        member.return_book(isbn)
        book.return_book()
        return "Book returned"

    def search_books(self, keyword):
        return [b for b in self.books.values()
                if keyword.lower() in b.title.lower()
                or keyword.lower() in b.author.lower()
                or keyword == b.isbn]

    def save_data(self):
        os.makedirs("data", exist_ok=True)
        with open(BOOK_FILE, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.books.items()}, f, indent=4)

        with open(MEMBER_FILE, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.members.items()}, f, indent=4)

    def load_data(self):
        if os.path.exists(BOOK_FILE):
            with open(BOOK_FILE) as f:
                data = json.load(f)
                for k, v in data.items():
                    self.books[k] = Book.from_dict(v)

        if os.path.exists(MEMBER_FILE):
            with open(MEMBER_FILE) as f:
                data = json.load(f)
                for k, v in data.items():
                    self.members[k] = Member.from_dict(v)

    def statistics(self):
        return {
            "total_books": len(self.books),
            "available_books": len([b for b in self.books.values() if b.available]),
            "members": len(self.members)
        }
