# levilibreria

Sistema minimale per gestire una libreria con funzioni di catalogo, prestito,
restituzione e prolungamento del prestito, oltre a una vista semplificata per i
gestori.

## Funzionalità
- Catalogo con copie disponibili
- Prestito e restituzione
- Prolungamento prestito
- Vista gestore con elenco sintetico

## Esempio rapido
```python
from datetime import date, timedelta
from library_system import LibrarySystem

system = LibrarySystem()
system.add_book("B001", "Il Nome della Rosa", "Umberto Eco", 2)

loan_id = system.loan_book("B001", "utente-1", date.today() + timedelta(days=14))

system.extend_loan(loan_id, date.today() + timedelta(days=21))

system.return_book(loan_id)

print(system.list_catalog())
print(system.manager_view())
```
