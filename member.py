class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.max_books = 5

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_books

    def borrow_book(self, isbn):
        if not self.can_borrow():
            return False, "Borrow limit reached"
        self.borrowed_books.append(isbn)
        return True, "Book added to member record"

    def return_book(self, isbn):
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True
        return False

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        member = cls(data["name"], data["member_id"])
        member.borrowed_books = data["borrowed_books"]
        return member

    def __str__(self):
        return f"{self.member_id} - {self.name} (Books: {len(self.borrowed_books)})"
