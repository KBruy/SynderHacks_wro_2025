# Dokumentacja — `Frontend/index.php`

Krótki opis
-----------
Plik `index.php` to prosty, prototypowy frontend napisany w PHP. Realizuje "router" oparty na query stringu `?tab=...` i renderuje kilka statycznych widoków (rekomendacje, produkty, kanały, ceny, raporty, ustawienia). Służy jako szybki prototyp UI przed migracją do React lub innego frontendu.

Główne źródła danych i wejścia
-----------------------------
- Parametr GET: `?tab=<key>` — wybiera widok/sekcję. Domyślnie `rekomendacje`.
  - Kod: `$tab = $_GET['tab'] ?? 'rekomendacje';`
- Lokalny menu array: `$menu` — mapuje klucz -> etykieta.
- Widoki treści zrealizowane są w `switch ($tab)` — obecnie zawierają statyczne placeholdery.
- Przy generowaniu linków i etykiet użyto `htmlspecialchars()` (częściowa ochrona przed XSS).

Zalecenia bezpieczeństwa
------------------------
- Zastosować whitelistę dostępnych `tab`ów: np. `$allowed = array_keys($menu); if (!in_array($tab, $allowed)) $tab = 'rekomendacje';`
- Nie include'ować plików bazując bezpośrednio na niezaufanym `$_GET` bez walidacji.
- Zawsze escapować dane pochodzące z backendu (`htmlspecialchars` dla tekstów w HTML).
- Dla każdej akcji POST/PUT dodać CSRF tokeny.

Proponowane kontrakty JSON (endpoints)
-------------------------------------
Poniżej przykłady formatów JSON, które backend może udostępnić, aby frontend stał się dynamiczny.

1) Menu
GET /api/ui/menu
{
  "menu": [
    {"key":"rekomendacje","label":"Rekomendacje","order":1},
    {"key":"produkty","label":"Produkty","order":2}
  ]
}

2) Rekomendacje
GET /api/recommendations
[
  {
    "id": "rec-1",
    "type": "price_change",
    "title": "Zmiana ceny",
    "summary": "Proponowana korekta: -7%",
    "sku": "ABC-123",
    "impact_est": {"revenue_pct": -0.07, "reach_pct": 0.12},
    "details_url": "/rekomendacje/rec-1"
  }
]

3) Produkty
GET /api/products?limit=20&page=1
{
  "items": [
    {
      "sku":"ABC-123",
      "name":"Nazwa produktu",
      "stock":42,
      "rotation":"low",
      "price":49.99,
      "channels":["woocommerce","shopify"],
      "last_sold":"2025-11-07T12:34:00Z"
    }
  ],
  "meta": {"page":1,"limit":20,"total":152}
}

4) Ostatnie zdarzenia
GET /api/events?limit=10
[
  {"time":"2025-11-08T09:12:00Z","message":"Import danych z WooCommerce","meta":{"count":152}}
]

5) Kanały sprzedaży
GET /api/channels
[
  {"id":"woocommerce","name":"WooCommerce","status":"connected","last_sync":"2025-11-08T10:00:00Z"},
  {"id":"ebay","name":"eBay","status":"disconnected"}
]

6) Raporty (generowanie)
POST /api/reports
Body: {"type":"sales","from":"2025-01-01","to":"2025-10-31","format":"pdf"}
Response: {"report_id":"rpt-123","download_url":"/reports/rpt-123.pdf"}

Uwagi implementacyjne i miejsca refaktora
-----------------------------------------
- Wydzielić `views/` i przenieść każdy case z `switch` do osobnego pliku (np. `views/rekomendacje.php`).
- Dodać `lib/api_client.php` — centralny klient REST (base URL, timeout, retry, dekodowanie JSON, cache krótkoterminowy).
- Wydzielić helpery (np. `lib/helpers.php`) z `is_active()` i funkcjami sanitizacji.
- Dodać prostą warstwę cache (np. plikową lub opcache) dla list produktów i rekomendacji podczas prototypowania.

Szybkie testy które warto dodać
------------------------------
- Unit test `is_active('produkty','produkty') => ' is-active'`.
- Integration: GET `?tab=nieistnieje` => fallback do `rekomendacje`.
- XSS: umieścić w menu etykietę z tagami HTML i sprawdzić, że w wyjściu są escaped.

Proponowane pliki do dodania
----------------------------
- `Frontend/views/rekomendacje.php` — widok rekomendacji
- `Frontend/views/produkty.php` — widok produktów
- `Frontend/lib/api_client.php` — klient REST
- `Frontend/lib/helpers.php` — funkcje pomocnicze
- `Frontend/README.md` — krótka dokumentacja i instrukcja uruchomienia

Kolejne kroki (szybkie priorytety)
---------------------------------
1. Dodać whitelistę `tab` i proste przeniesienie `switch` -> `views/` (niski risk).
2. Dodać `api_client` i podłączyć `produkty` do `/api/products` (średni effort).
3. Dodać testy PHPUnit dla helperów i routera (średni effort).

---


