from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from itertools import count
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Book:
    book_id: str
    title: str
    author: str
    total_copies: int


@dataclass
class Loan:
    loan_id: str
    book_id: str
    borrower_id: str
    due_date: date
    returned: bool = False
    returned_at: Optional[date] = None


@dataclass
class _BookRecord:
    book: Book
    available_copies: int


class LibrarySystem:
    def __init__(self) -> None:
        self._books: Dict[str, _BookRecord] = {}
        self._loans: Dict[str, Loan] = {}
        self._loan_counter = count(1)

    def add_book(self, book_id: str, title: str, author: str, total_copies: int) -> None:
        if total_copies <= 0:
            raise ValueError("total_copies must be positive")
        if book_id in self._books:
            raise ValueError("book_id already exists")
        book = Book(book_id=book_id, title=title, author=author, total_copies=total_copies)
        self._books[book_id] = _BookRecord(book=book, available_copies=total_copies)

    def list_catalog(self) -> List[dict]:
        return [
            {
                "book_id": record.book.book_id,
                "title": record.book.title,
                "author": record.book.author,
                "total_copies": record.book.total_copies,
                "available_copies": record.available_copies,
            }
            for record in self._books.values()
        ]

    def loan_book(self, book_id: str, borrower_id: str, due_date: date) -> str:
        if not isinstance(due_date, date):
            raise TypeError("due_date must be a date")
        record = self._books.get(book_id)
        if record is None:
            raise ValueError("book_id not found")
        if record.available_copies <= 0:
            raise ValueError("no copies available")
        loan_id = f"L{next(self._loan_counter):04d}"
        self._loans[loan_id] = Loan(
            loan_id=loan_id,
            book_id=book_id,
            borrower_id=borrower_id,
            due_date=due_date,
        )
        record.available_copies -= 1
        return loan_id

    def return_book(self, loan_id: str, return_date: Optional[date] = None) -> None:
        loan = self._loans.get(loan_id)
        if loan is None:
            raise ValueError("loan_id not found")
        if loan.returned:
            raise ValueError("loan already returned")
        loan.returned = True
        loan.returned_at = return_date or date.today()
        record = self._books[loan.book_id]
        record.available_copies += 1

    def extend_loan(self, loan_id: str, new_due_date: date) -> None:
        if not isinstance(new_due_date, date):
            raise TypeError("new_due_date must be a date")
        loan = self._loans.get(loan_id)
        if loan is None:
            raise ValueError("loan_id not found")
        if loan.returned:
            raise ValueError("loan already returned")
        if new_due_date <= loan.due_date:
            raise ValueError("new_due_date must be after current due_date")
        loan.due_date = new_due_date

    def manager_view(self) -> dict:
        return {
            "catalog": [
                {
                    "book_id": record.book.book_id,
                    "title": record.book.title,
                    "available_copies": record.available_copies,
                }
                for record in self._books.values()
            ],
            "active_loans": [
                {
                    "loan_id": loan.loan_id,
                    "book_id": loan.book_id,
                    "borrower_id": loan.borrower_id,
                    "due_date": loan.due_date,
                }
                for loan in self._loans.values()
                if not loan.returned
            ],
        }
