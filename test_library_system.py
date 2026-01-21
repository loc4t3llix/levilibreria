import unittest
from datetime import date, timedelta

from library_system import LibrarySystem


class LibrarySystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.system = LibrarySystem()
        self.system.add_book("B001", "Il Nome della Rosa", "Umberto Eco", 2)

    def test_catalog_and_manager_view(self) -> None:
        catalog = self.system.list_catalog()
        self.assertEqual(catalog[0]["available_copies"], 2)
        view = self.system.manager_view()
        self.assertEqual(view["catalog"][0]["available_copies"], 2)
        self.assertEqual(view["active_loans"], [])

    def test_loan_return_and_extend(self) -> None:
        due_date = date.today() + timedelta(days=14)
        loan_id = self.system.loan_book("B001", "utente-1", due_date)
        view = self.system.manager_view()
        self.assertEqual(view["catalog"][0]["available_copies"], 1)
        self.assertEqual(view["active_loans"][0]["loan_id"], loan_id)

        new_due = due_date + timedelta(days=7)
        self.system.extend_loan(loan_id, new_due)
        self.assertEqual(self.system.manager_view()["active_loans"][0]["due_date"], new_due)

        self.system.return_book(loan_id)
        self.assertEqual(self.system.manager_view()["active_loans"], [])
        self.assertEqual(self.system.list_catalog()[0]["available_copies"], 2)


if __name__ == "__main__":
    unittest.main()
