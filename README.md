# FCHM Blog Application

Blog aplikacja dla Forum Chemików Medycznych zbudowana w architekturze MVT (Model-View-Template) z Django.

<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/9e76cf6d-be05-465b-b4e6-59b2d927e2ab" />

## Architektura Aplikacji

### Backend (`backend/`)
Główna konfiguracja projektu Django zawierająca settings, URL routing i WSGI/ASGI.

### Apps (`apps/`)

#### Posts (`apps/posts/`)
Aplikacja zarządzająca artykułami blogowymi z obsługą kategorii, tagów, komentarzy i mediów.

**Główne komponenty:**
- `models.py` - Modele: Post, Category, Tag, Comment, Gallery z relacjami i metadanymi
- `managers.py` - Custom managery dla zaawansowanych zapytań do postów i kategorii
- `serializers.py` - DRF serializery do REST API z obsługą zagnieżdżonych relacji
- `views.py` - API endpoints (ViewSets) i widoki webowe do wyświetlania postów
- `admin.py` - Panel administracyjny z inline'ami dla komentarzy i galerii
- `urls.py` - REST API routing (`/api/posts/`, `/api/categories/`, `/api/tags/`)
- `urls_web.py` - Routing dla widoków webowych szczegółów postów
- `templates/` - Szablony HTML do renderowania pojedynczych postów

#### Pages (`apps/pages/`)
Aplikacja obsługująca wszystkie statyczne i dynamiczne strony witryny.

**Struktura modułowa:**
- `home/` - Strona główna z wyróżnionymi i najnowszymi postami (3 sekcje layout)
- `about/` - Strona "O nas" z informacjami o fundacji
- `contact/` - Formularz kontaktowy z wysyłką email
- `search/` - Inteligentne wyszukiwanie artykułów (po tytule, treści, tagach)
- `mozg/` - Strona statyczna poświęcona tematyce neurochemii
- `statut/` - Statut fundacji
- `categories/` - Lista i szczegóły kategorii z paginacją postów
- `base.html` - Bazowy szablon z nawigacją, menu dropdown i footer
- `templatetags/` - Custom template tags do pobierania kategorii w nawigacji

#### Banners (`apps/banners/`)
System rotujących banerów reklamowych na różnych pozycjach strony.

**Główne komponenty:**
- `models.py` - Model Banner z polami: obraz, link, pozycja, aktywność
- `managers.py` - Managery do filtrowania aktywnych banerów po pozycji
- `admin.py` - Panel administracyjny do zarządzania banerami
- `templatetags/` - Template tags do wyświetlania banerów w szablonach
- **Pozycje**: `home_banner_1`, `home_banner_2`, `home_banner_3` (rotacja co 5s)

#### Map (`apps/map/`)
Interaktywna mapa ośrodków medycznych z integracją Google Maps API.

**Główne komponenty:**
- `models.py` - Model MedicalCenter: nazwa, adres, współrzędne, typ, opis
- `managers.py` - Managery z geolokalizacją i wyszukiwaniem w promieniu
- `serializers.py` - Serializery do API zwracające dane ośrodków
- `views.py` - API endpoints i widok webowy mapy
- `static/` - JavaScript do renderowania mapy i markerów
- `templates/` - Szablon HTML z osadzoną mapą Google
- `management/commands/` - Komendy do importu danych ośrodków

### Baza Danych
PostgreSQL z konfiguracją przez Docker Compose, zmienne środowiskowe w `.env`.

### Media i Statyki
- `media/` - Pliki przesyłane przez użytkowników (zdjęcia postów, galerie, banery)
- `static/` - Statyczne pliki CSS/JS/obrazy dla poszczególnych aplikacji
- CKEditor do bogatej edycji treści z upload obrazów

### API REST
Django REST Framework z tokenową autentykacją, filtrowaniem i paginacją (20 elementów/strona).

### Technologie
- **Backend**: Django 5.1, PostgreSQL, Django REST Framework
- **Frontend**: Tailwind CSS, JavaScript vanilla, Google Maps API
- **Inne**: CKEditor, Pillow, django-cors-headers, django-filter
- **Deployment**: Docker + Docker Compose

### Konfiguracja środowiska
- `backend/settings/base.py` - Wspólne ustawienia dla wszystkich środowisk
- `backend/settings/development.py` - Konfiguracja developerska (DEBUG=True)
- `backend/settings/production.py` - Konfiguracja produkcyjna
- `.env` - Zmienne środowiskowe (DB credentials, SECRET_KEY, API keys)
