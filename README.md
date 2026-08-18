# Product Suggestions Manager

System zarządzania produktami z inteligentnymi sugestiami optymalizacyjnymi (cena, promocje, bundle).

## Demo Application

Aplikacja demonstracyjna do zarządzania produktami e-commerce z automatycznymi sugestiami optymalizacji sprzedaży.

## Funkcjonalności

- **Lista produktów**: Przeglądaj produkty z różnych kanałów (WooCommerce, Shopify)
- **Inteligentne sugestie**: Otrzymuj sugestie dotyczące:
  - Optymalizacji cen
  - Promocji i rabatów
  - Pakietów produktowych (bundles)
- **Zastosowanie sugestii**: Jednym kliknięciem zastosuj sugestię
- **Historia zdarzeń**: Śledź wszystkie zmiany i akcje
- **Real-time powiadomienia**: Natychmiastowa informacja zwrotna o akcjach

## Wymagania

- Docker
- docker-compose

## Uruchomienie

### Szybki start (jedna komenda)

```bash
docker-compose up
```

Aplikacja będzie dostępna pod adresem:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5001
- **Health check**: http://localhost:5001/health

### 🎮 Tryb Demo (bez prawdziwych sklepów)

**Nie masz jeszcze sklepu? Nie ma problemu!**

1. Otwórz aplikację: http://localhost:5173
2. Przejdź do zakładki **"Połączenia ze sklepami"**
3. Kliknij przycisk **"🎮 Szybkie Demo"**
4. Dla każdego demo sklepu kliknij **"Synchronizuj"**
5. Gotowe! Przetestuj wszystkie funkcje bez prawdziwego sklepu

📖 Pełna instrukcja: [DEMO_MODE.md](DEMO_MODE.md)

### Pierwsze uruchomienie

Przy pierwszym uruchomieniu aplikacja automatycznie:
1. Utworzy bazę danych SQLite
2. Załaduje dane testowe:
   - 8 produktów
   - 15+ sugestii
   - Przykładowe zdarzenia w historii

### Zatrzymanie aplikacji

```bash
docker-compose down
```

### Czyszczenie danych (reset)

Aby usunąć bazę danych i zacząć od nowa:

```bash
docker-compose down -v
docker-compose up
```

## Struktura projektu

```
.
├── backend/                 # Flask REST API
│   ├── app/
│   │   ├── main.py         # Główny plik aplikacji
│   │   └── database.py     # Obsługa bazy danych i seed
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React + Vite
│   ├── src/
│   │   ├── components/    # Komponenty UI
│   │   ├── services/      # API client
│   │   ├── App.jsx        # Główny komponent
│   │   └── main.jsx       # Entry point
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml      # Orkiestracja
```

## API Endpoints

- `GET /health` - Status aplikacji
- `GET /api/products` - Lista wszystkich produktów
- `GET /api/suggestions?product_id=ID` - Sugestie dla produktu
- `POST /api/suggestions/:id/apply` - Zastosuj sugestię
- `GET /api/events` - Historia zdarzeń (ostatnie 20)

## Dane testowe

### Produkty

Aplikacja zawiera 8 produktów przykładowych:
- Smartwatch Fitness Pro
- Wireless Earbuds Elite
- Portable Power Bank 20000mAh
- USB-C Charging Cable 2m
- Bluetooth Speaker Waterproof
- Phone Stand Adjustable
- Laptop Sleeve 15 inch
- Gaming Mouse RGB

### Typy sugestii

- **Price** (Cena): Sugestie dotyczące optymalizacji cen
- **Promo** (Promocja): Propozycje promocji i rabatów
- **Bundle** (Pakiet): Pomysły na pakiety produktowe

## Rozwój

### Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

## Technologie

**Backend:**
- Python 3.11
- Flask 3.0
- SQLite 3
- Flask-CORS

**Frontend:**
- React 18
- Vite 5
- Vanilla CSS (bez dodatkowych bibliotek)

**Infrastructure:**
- Docker
- docker-compose

## Logi

Logi backendu są czytelne i zawierają poziomy: INFO, WARN, ERROR.

```bash
# Podgląd logów
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Wydajność

- Czas odpowiedzi API: < 300ms
- Wszystkie endpointy działają bez zewnętrznych integracji
- Lekka baza SQLite w wolumenie Docker

## Bezpieczeństwo

**UWAGA**: To jest aplikacja demonstracyjna!

- CORS jest permissive (wszystkie origins)
- Brak autentykacji użytkowników
- Brak walidacji danych po stronie backendu (tylko podstawowa)
- Nie używać w produkcji bez dodatkowych zabezpieczeń

## Kryteria akceptacji

- ✅ Uruchomienie jedną komendą `docker-compose up`
- ✅ Widoczna lista min. 5 produktów
- ✅ Min. 2 sugestie dla każdego produktu
- ✅ Akcja "Zastosuj sugestię" zmienia status i dodaje wpis do historii
- ✅ Powiadomienia o sukcesie/błędzie
- ✅ Historia wyświetla ostatnie akcje
- ✅ Endpoint /health zwraca pozytywny status
- ✅ Responsywny UI z obsługą stanów: loading, error, empty

## Licencja

MIT


