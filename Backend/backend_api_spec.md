# Backend API — specyfikacja (propozycja)

Cel
----
Dokument określa kontrakty JSON i endpointy, które backend może udostępnić dla prototypu frontendu znajdującego się w `Frontend/index.php`. Ma służyć jako jasny kontrakt do implementacji backendu lub do mockowania podczas pracy nad frontendem (i późniejszą migracją do React).

Wersjonowanie
------------
- Wszystkie endpointy powinny być pod ścieżką `/api/v1/...` (pierwsza wersja).
- W przypadku zmian kompatybilnych wstecz, dodać nowe pola; przy zmianach niekompatybilnych zwiększyć numer wersji.

Autentykacja i autoryzacja
-------------------------
Opcje (wybierz jedną dla prototypu):
- API key: nagłówek `Authorization: ApiKey <key>` (prosty do testów)
- JWT (Bearer): `Authorization: Bearer <jwt>` (lepsze dla użytkowników)
- Mechanizmy: sprawdzać uprawnienia do zasobów (np. generowanie raportów)

Nagłówki i formaty
------------------
- Content-Type: `application/json` dla requestów i response'ów JSON.
- Accept: `application/json`.
- Timestamp/Request-Id (opcjonalnie) dla logowania i korelacji: `X-Request-Id`.

Format błędów
-------------
Standardowy shape:
{
  "error": {
    "code": "INVALID_INPUT",    // short machine code
    "message": "Opis błędu dla deva/klienta",
    "details": {"field":"price","reason":"negative"},
    "status": 400
  }
}

Paginacja
---------
- W listach użyć paginacji: query params `page` (1-based) i `limit`.
- Response zawiera `meta` z total, page, limit.

Common meta example:
{
  "items": [...],
  "meta": {"page":1, "limit":20, "total":152}
}

Endpoints
---------
1) GET /api/v1/ui/menu
- Opis: Pobiera listę elementów menu (klucz, label, order). Przydatne gdy menu ma się dynamicznie zmieniać.
- Params: (none)
- Response 200:
{
  "menu": [
    {"key":"rekomendacje","label":"Rekomendacje","order":1},
    {"key":"produkty","label":"Produkty","order":2},
    {"key":"kanaly","label":"Kanały sprzedaży","order":3}
  ]
}

2) GET /api/v1/recommendations
- Opis: Lista rekomendacji AI dla produktów.
- Params (opcjonalne): `limit`, `page`, `sku` (filter)
- Response 200 (lista):
{
  "items": [
    {
      "id": "rec-1",
      "type": "price_change",
      "title": "Zmiana ceny",
      "summary": "Proponowana korekta: -7%",
      "sku": "ABC-123",
      "severity": "medium", // low|medium|high
      "impact_est": {"revenue_pct": -0.07, "reach_pct": 0.12},
      "created_at": "2025-11-08T09:12:00Z",
      "details_url": "/rekomendacje/rec-1"
    }
  ],
  "meta": {"page":1,"limit":20,"total":3}
}

3) GET /api/v1/products
- Opis: Lista produktów (paginowana).
- Query params: `limit`, `page`, `rotation` (low|medium|high), `q` (search), `channel`
- Response 200:
{
  "items": [
    {
      "sku":"ABC-123",
      "name":"Nazwa produktu",
      "stock":42,
      "rotation":"low",
      "price":49.99,
      "currency":"PLN",
      "channels":["woocommerce","shopify"],
      "last_sold":"2025-11-07T12:34:00Z",
      "image_url":"https://.../abc-123.jpg"
    }
  ],
  "meta": {"page":1,"limit":20,"total":152}
}

4) GET /api/v1/products/{sku}
- Opis: Szczegóły produktu.
- Response 200:
{
  "sku":"ABC-123",
  "name":"Nazwa produktu",
  "description":"Dłuższy opis...",
  "stock":42,
  "price":49.99,
  "rotation":"low",
  "channels":[{"id":"woocommerce","status":"connected"}],
  "attributes": {"color":"red","size":"M"}
}

5) GET /api/v1/events
- Opis: Ostatnie zdarzenia/aktywności systemu (importy, sync, aktualizacje).
- Params: `limit` (domyślnie 10)
- Response 200:
[
  {"time":"2025-11-08T09:12:00Z","message":"Import danych z WooCommerce","meta":{"count":152}},
  {"time":"2025-11-07T17:00:00Z","message":"Dodano kanał: Shopify"}
]

6) GET /api/v1/channels
- Opis: Lista integracji / kanałów sprzedaży i ich statusy.
- Response 200:
[
  {"id":"woocommerce","name":"WooCommerce","status":"connected","last_sync":"2025-11-08T10:00:00Z"},
  {"id":"shopify","name":"Shopify","status":"connected","last_sync":"2025-11-07T09:00:00Z"},
  {"id":"ebay","name":"eBay","status":"disconnected"}
]

7) POST /api/v1/reports
- Opis: Generowanie raportu (PDF/CSV). Może być asynchroniczne (zwrócić job id) lub synchroniczne dla małych raportów.
- Body example:
{
  "type":"sales",
  "from":"2025-01-01",
  "to":"2025-10-31",
  "format":"pdf",
  "filters": {"channels":["shopify"]}
}
- Response 202 (async):
{
  "job_id":"rpt-job-123",
  "status":"queued",
  "poll_url":"/api/v1/reports/jobs/rpt-job-123"
}
- Polling GET /api/v1/reports/jobs/{job_id}
  - 200 when ready: {"job_id":"...","status":"done","download_url":"/reports/rpt-123.pdf"}

8) GET /api/v1/health
- Opis: prosty health check dla CI/monitoringu
- Response 200:
{"status":"ok","time":"2025-11-08T10:00:00Z"}

Opcjonalne / dodatkowe endpointy
--------------------------------
- POST /api/v1/channels/{id}/connect — inicjuje OAuth/connection flow dla Shopify/eBay.
- POST /api/v1/products/import — ręczny trigger importu z kanału (z body: {channel:"woocommerce"}).
- Webhooky: `/webhooks/channel-sync` — przydatne, gdy integracja zewnętrzna może powiadamiać o zakończeniu sync.

Walidacja i reguły biznesowe
----------------------------
- SKU: string, 1-64 znaki, tylko alfanum i -/_ (walidować po stronie API).
- price: liczba >= 0.
- stock: integer >= 0.
- rotation: enum {"low","medium","high"} — można obliczać po stronie backendu i zwracać gotową wartość.

Rate limiting i cache
---------------------
- Dla prototypu: limit 60 req/min per API key.
- Dla list (produkty, rekomendacje) implementować cache warstwy (30s–60s) aby zmniejszyć obciążenie podczas testów.

Bezpieczeństwo
--------------
- Escapować/cleanować wszystkie pola, które będą renderowane w HTML po stronie klienta.
- Dla download URL do raportu: generować krótkotrwałe, podpisane URL (signed URL) lub zabezpieczyć dostęp poprzez auth.
- Nie ujawniać stack trace w response (tylko generować przyjazny komunikat i szczegóły w logu serwera).

Monitoring i logowanie
----------------------
- Logować błędy serwera (500) z unikalnym request id.
- Eksponować metryki: request rate, error rate, average latency (endpointy kluczowe: /products, /recommendations, /reports).

Przykładowe scenariusze użycia
------------------------------
1) Frontend ładuje menu i domyślny widok:
- GET /api/v1/ui/menu
- GET /api/v1/recommendations?limit=10

2) Użytkownik przechodzi do widoku produktów:
- GET /api/v1/products?page=1&limit=20
- Dla szczegółów klikniętego SKU: GET /api/v1/products/{sku}

3) Generowanie raportu (async):
- POST /api/v1/reports (body)
- Poll GET /api/v1/reports/jobs/{job_id} aż status == done
- GET download_url (autoryzacja lub signed URL)

Mockowanie i testy
------------------
- Sugerowane narzędzia: Postman / Insomnia do mocków, json-server do szybkiego lokalnego mocka.
- Przy testach integracyjnych: stubować 3rd-party (Shopify/WooCommerce) i testować retry/circuit-breaker.

OpenAPI / Swagger
-----------------
- Zdecydowanie polecam przygotować minimalne OpenAPI (yaml/json) z wymienionymi endpointami — ułatwi front-endowi generowanie klientów i mocków.

Checklista przed wdrożeniem
--------------------------
- [ ] Autentykacja i uprawnienia działają poprawnie.
- [ ] Wszystkie pola walidowane po stronie backendu.
- [ ] Testy integracyjne dla krytycznych ścieżek.
- [ ] Mechanizm generowania raportów i bezpieczne downloady.
- [ ] Monitoring i alerty skonfigurowane.

---

Plik ten to propozycja kontraktów i zasad. Mogę z tego wygenerować:
- gotowy OpenAPI (yaml) z powyższymi endpointami,
- minimalne mocki json-server lub Postman collection,
- implementację prostego mock API w PHP (lub Node) w repo jeśli chcesz — którą opcję preferujesz?