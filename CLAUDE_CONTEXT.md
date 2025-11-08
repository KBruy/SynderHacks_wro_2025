# Claude Context - Product Suggestions Manager

> **Dla osób pracujących z Claude**: Ten plik zawiera pełny kontekst projektu, kluczowe decyzje architektoniczne i stan implementacji.

## 🎯 Cel Projektu

System zarządzania produktami e-commerce z automatycznymi sugestiami optymalizacji (cena, promocje, bundle). Demo aplikacja dla hackathonu.

## 🏗️ Architektura

### Backend (Python/Flask)
- **Port**: 5001 (zmieniony z 5000 przez konflikt)
- **Baza danych**: SQLite z volume Docker `/data/products.db`
- **Bezpieczeństwo**: Credentials szyfrowane AES (cryptography + PBKDF2HMAC)

### Frontend (React/Vite)
- **Port**: 5173
- **Styling**: Vanilla CSS (bez bibliotek)
- **State**: React hooks (useState, useEffect)

### Integracje
- WooCommerce REST API v3
- Shopify Admin API 2024-01
- **Mock mode** dla testów bez prawdziwych sklepów

## 📊 Schema Bazy Danych

### Główne Tabele

```sql
products (
  id, sku, name, price, stock, status, channel,
  connection_id, external_id, created_at, updated_at
)

suggestions (
  id, product_id, type [price|promo|bundle],
  description, status [new|applied], applied_at
)

bundles (
  id, name, sku, price, channel, connection_id, is_active
)

bundle_items (
  id, bundle_id, product_id, quantity
)

events (
  id, product_id, suggestion_id, event_type,
  description, created_at
)

store_connections (
  id, name, platform, store_url,
  api_key_encrypted, api_secret_encrypted, is_active
)
```

## 🔑 Kluczowe Rozwiązania

### 1. Timestamps
**Problem**: SQLite `CURRENT_TIMESTAMP` zwraca UTC, frontend parsował jako local time.

**Rozwiązanie**: Backend używa `datetime.now().isoformat(sep=' ', timespec='seconds')` dla explicit local time.

```python
now = datetime.now().isoformat(sep=' ', timespec='seconds')
cursor.execute('INSERT INTO events (..., created_at) VALUES (..., ?)', (..., now))
```

Frontend:
```javascript
const date = new Date(dateString.replace(' ', 'T')); // SQLite format to ISO
```

### 2. Aktualizacja Ceny z Sugestii
**Problem**: Sugestie cenowe nie aktualizowały produktu.

**Rozwiązanie**: Backend parsuje opis sugestii regex i aktualizuje cenę.

```python
# Pattern 1: "Podwyższ cenę do 169.99"
match = re.search(r'do\s+(\d+\.?\d*)', description)

# Pattern 2: "Obniż cenę o 15%"
match = re.search(r'o\s+(\d+)%', description)
```

Lokalizacja: `backend/app/main.py:233-259`

### 3. Obsługa Kliknięć w Tabeli
**Problem**: Każde kliknięcie otwierało modal.

**Rozwiązanie**:
- Kliknięcie w **wiersz** → zaznaczenie + sugestie w sidebar
- Kliknięcie w **nazwę produktu** → modal ze szczegółami

```jsx
// ProductsTable.jsx
<tr onClick={() => onSelectProduct(product)}>
  <td>
    <span className="product-name-link"
          onClick={(e) => { e.stopPropagation(); onShowDetails(product); }}>
      {product.name}
    </span>
  </td>
</tr>
```

### 4. Auto-odświeżanie po Zastosowaniu Sugestii
**Problem**: Aktywne promocje nie pojawiały się bez F5.

**Rozwiązanie**: Callback `handleSuggestionApplied` wywołuje `loadProducts()`.

```javascript
const handleSuggestionApplied = (notificationData) => {
  setNotification(notificationData);
  loadProducts(); // Refresh products & active promotions
  setHistoryRefresh(prev => prev + 1);
};
```

## 🎮 Tryb Demo

### Quick Setup
```bash
# Frontend
POST /api/connections/demo/quick-setup
# Tworzy 2 demo sklepy (WooCommerce + Shopify)

# Synchronizacja
POST /api/connections/:id/sync
# Generuje 8-20 produktów + auto-sugestie
```

### MockIntegration
- `backend/app/integrations/mock.py`
- Zwraca random produkty (8-20 sztuk) z realistycznymi cenami/stockiem
- Używany gdy `api_key == 'demo-key'`

### Auto-generowanie Sugestii
- `backend/app/suggestions_generator.py`
- Tworzy 2-4 sugestie per produkt (tylko dla demo)
- Szablony w 3 językach: price, promo, bundle

## 🐛 Znane Problemy/Fixe

### Fix #1: Import Error PBKDF2
```python
# ❌ Przed
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# ✅ Po
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
```

### Fix #2: Cascade Delete Produktów
```python
# Przy usuwaniu connection, najpierw usuń produkty
cursor.execute('DELETE FROM products WHERE connection_id = ?', (connection_id,))
cursor.execute('DELETE FROM store_connections WHERE id = ?', (connection_id,))
```

### Fix #3: Stock Field Missing
Dodano kolumnę `stock INTEGER DEFAULT 0` do tabeli products + update sync logic.

## 📦 Bundle System (W TRAKCIE)

### Stan Implementacji
✅ Tabele (`bundles`, `bundle_items`) utworzone
❌ Tworzenie bundle z sugestii - TODO
❌ Kalkulacja dostępności: `min(product.stock / bundle_item.quantity)` - TODO
❌ Synchronizacja nakładu między produktami - TODO

### Założenia Biznesowe
1. Bundle składa się z 2+ produktów
2. Dostępność bundle = minimum z `floor(product.stock / quantity_in_bundle)`
3. Sprzedaż bundle OR pojedynczego produktu zmniejsza stock obu
4. Bundle to osobny listing z własnym SKU

### Przykład
```
Bundle: "Gaming Set"
- Gaming Mouse RGB (qty: 1, stock: 15)
- Mouse Pad (qty: 1, stock: 20)
→ Bundle availability: min(15/1, 20/1) = 15
```

## 🚀 Deployment

### Development
```bash
docker-compose up
# Frontend: http://localhost:5173
# Backend: http://localhost:5001
# Health: http://localhost:5001/health
```

### Clean Reset
```bash
docker-compose down -v  # Usuwa volume z bazą
docker-compose up
```

## 📝 Konwencje Kodu

### Backend
- **Logging**: `logger.info()` dla operacji, `logger.error()` dla błędów
- **Errors**: Return `jsonify({'error': 'message'})` z odpowiednim status code
- **Transactions**: Context manager `with get_db() as conn:` auto-commit/rollback

### Frontend
- **API errors**: Catch w `try/catch`, display w state `error`
- **Loading states**: Zawsze `loading` state dla async operacji
- **Notifications**: Auto-dismiss po 3s, typ: success/error

### Database
- **Timestamps**: Zawsze explicit `created_at` dla zdarzeń
- **Foreign keys**: Używane, ale bez CASCADE (explicit delete)
- **Text fields**: VARCHAR nie istnieje w SQLite, używaj TEXT

## 🔮 Następne Kroki

1. **Bundle System**
   - Endpoint: `POST /api/bundles/create`
   - Logika kalkulacji dostępności
   - UI dla tworzenia bundle z sugestii

2. **Stock Synchronization**
   - Webhook/endpoint dla zakupów
   - Aktualizacja stock w produktach bundle

3. **Monitoring Konkurencji**
   - Tabela `competitor_prices` jest utworzona
   - BeautifulSoup scraping - do implementacji

## 🆘 Troubleshooting

### Backend nie startuje
```bash
docker-compose logs backend
# Sprawdź czy port 5001 jest wolny
```

### Frontend nie łączy się z API
```bash
# frontend/.env
VITE_API_URL=http://localhost:5001
```

### Baza danych corrupted
```bash
docker-compose down -v
docker volume rm synderhacks_wro_2025_sqlite-data
docker-compose up
```

## 📚 Przydatne Pliki

- `backend/app/main.py` - Wszystkie endpointy API
- `backend/app/database.py` - Schema + seed data
- `frontend/src/App.jsx` - Main component, state management
- `frontend/src/index.css` - Wszystkie style
- `DEMO_MODE.md` - Instrukcje trybu demo
- `STORE_API_SETUP.md` - Setup prawdziwych sklepów

## 🤝 Praca Zespołowa z Claude

### Dla Nowej Osoby
1. Przeczytaj ten plik najpierw
2. Uruchom `docker-compose up`
3. Przetestuj demo: http://localhost:5173 → "🎮 Szybkie Demo"
4. Sprawdź `git log` dla historii zmian

### Przed Zadaniem Pytania Claude
- Podaj kontekst: "Pracuję nad Product Suggestions Manager, przeczytałem CLAUDE_CONTEXT.md"
- Wskaż konkretny problem/feature
- Załącz relevantny kod jeśli potrzeba

### Commitowanie
```bash
git add .
git commit -m "feat(feature): opis zmiany

- szczegóły
- co zostało naprawione/dodane
"
```

## 📊 Metryki Projektu

- **Backend endpoints**: 11
- **React components**: 7
- **Database tables**: 8
- **Docker containers**: 2
- **Lines of code**: ~2500 (backend) + ~1200 (frontend)
- **Test coverage**: Demo mode (manual testing)

---

**Ostatnia aktualizacja**: 2025-11-08
**Status**: MVP ukończone, Bundle system w trakcie
**Autorzy**: Igor Olewicz + Claude
