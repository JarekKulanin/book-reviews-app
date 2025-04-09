Recenzaria - aplikacja webowa stworzona w Django, umożliwiająca przeglądanie książek, dodawanie recenzji oraz zarządzanie zasobami przez administratora. Projekt zawiera również API do dodawania książek.


Funkcjonalności:
-Rejestracja i logowanie użytkownika
-Przeglądanie książek z paginacją, kategoriami i wyszukiwarką
-Szczegóły książki z recenzjami
-Dodawanie recenzji
-Panel admina do zarządzania książkami
-Możliwość dodawania książek przez API
-Interfejs z wykorzystaniem Bootstrapa
-Obsługa komunikatów i walidacji formularzy


Zastosowane technologie:
-Python 3.11+
-Django 4+
-Django REST Framework
-Bootstrap 5
-JavaScript 
-SQLite


Instrukcja:
git clone https://github.com/JarekKulanin/book-reviews-app.git
cd book-reviews-app
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser - aby utworzyć użytkownika z uprawnieniami admina


Endopointy API:
-POST /api/books/add/ - dodanie książki (tylko dla administratorów)
-GET /api/categories/ - lista kategorii
