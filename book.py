from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None

    def check_out(self, member_id, loan_days=14):
        if not self.available:
            return False, "Book already borrowed"

        self.available = False
        self.borrowed_by = member_id
        self.due_date = (datetime.now() + timedelta(days=loan_days)).strftime("%Y-%m-%d")
        return True, f"Book issued. Due date: {self.due_date}"

    def return_book(self):
        self.available = True
        self.borrowed_by = None
        self.due_date = None
        return True, "Book returned successfully"

    def is_overdue(self):
        if self.due_date and not self.available:
            return datetime.now() > datetime.strptime(self.due_date, "%Y-%m-%d")
        return False

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["isbn"], data.get("year"))
        book.available = data["available"]
        book.borrowed_by = data["borrowed_by"]
        book.due_date = data["due_date"]
        return book

    def __str__(self):
        status = "Available" if self.available else f"Borrowed (Due: {self.due_date})"
        return f"{self.title} by {self.author} [{self.isbn}] - {status}"
