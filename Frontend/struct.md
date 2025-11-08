# 🎯 Cel i założenia

Aplikacja webowa dla małych sklepów/firm do analizowania skuteczności ofert i automatyzacji działań dla produktów zalegających w magazynie. Frontend w **React**, UI na **shadcn/ui**, ikony **lucide-react**. Komunikacja z backendem przez **REST API (JSON)**.

---

# 🗺️ Architektura UX / mapa widoków

* **/** – **Recommendation Hub** (priorytet: wizualizacja outputu backendu – gotowe propozycje działań)
* **/recommendations** – Kolejka rekomendacji (widok listy/kanban + batch apply)
* **/products** – Lista produktów (pomocnicza; wejście z rekomendacji)
* **/products/:id** – Szczegóły produktu (kontekst dla rekomendacji)
* **/alerts** – Alerty i reguły
* **/experiments** – Testy A/B na bazie rekomendacji
* **/integrations** – Integracje (Shopify, WooCommerce, eBay, Square) + statusy konektorów
* **/reports** – Raporty i eksporty (CSV/PNG/PDF – w kolejnych iteracjach)
* **/settings** – Organizacja, klucze API, webhooks (bez modułu Users)

---

# 🧱 Layout aplikacji

**AppShell** (responsywny)

* **Sidebar** (nawigacja, kondensuje się do ikonek <768px)
* **Topbar** (selektor sklepu/kanału, zakres dat, globalne filtry, wyszukiwarka)
* **Main** (content routes)
* **Toasts**, **Dialog host**, **Drawer/Sheet** dla akcji kontekstowych

**Komponenty (shadcn/ui):** `Card`, `Button`, `Badge`, `Tabs`, `Table`, `Dialog`, `Sheet`, `DropdownMenu`, `Select`, `Input`, `Textarea`, `Alert`, `Toast`, `Tooltip`, `Separator`, `Progress`, `Skeleton`.

**Ikony (lucide):** `Store`, `Package`, `Activity`, `TrendingDown`, `LineChart`, `Rocket`, `Wrench`, `Bell`, `Plug`, `Settings`, `AlertTriangle`, `BadgePercent`.

**Kolory/feel:** czysty, kontrastowy, dużo whitespace, delikatne cienie i zaokrąglenia (`rounded-2xl`).

---

# 🏠 Recommendation Hub (/**)

**Cel:** natychmiastowe pokazanie **propozycji backendu** z możliwością przeglądu, podglądu zmian i wdrożenia.

**Sekcje:**

* **Priority buckets**: *High Impact*, *Quick Wins*, *Low Effort* (paski liczników + filtry)
* **Recommendation Feed** (karty w 2–3 kolumnach, infinite scroll):

  * Header: typ (Price/Title/Images/Channel/Promo), **Impact**, **Effort**, Confidence, ETA
  * Preview: diff tytułu/opisu, porównanie cen (przed→po), miniatury obrazków (stare/nowe), target kanału
  * Akcje: *Apply*, *Schedule*, *Add to Queue*, *Reject* (z powodem)
  * Meta: link do produktu, spodziewana zmiana metryk (np. +4–7% CTR)
* **Execution Queue**: operacje zaplanowane/wykonywane, postęp, możliwość *Undo/Rollback*
* **Recently Applied**: lista ostatnich wdrożeń + wynik (sparklines, badge *Success/Mixed/No effect*)

**KPI Hub (nad feedem):**

* Liczba rekomendacji do wdrożenia
* Szacowany łączny wpływ (np. Δ revenue / Δ CTR)
* Średni czas wdrożenia
* Skuteczność ostatnich 14 dni (success rate)

---

# 📦 Lista produktów (/products)

**Rola pomocnicza**: narzędzie do nawigacji kontekstowej. W tabeli flagi wskazujące, które produkty mają aktywne rekomendacje.

* Kolumny minimalne: *SKU, Tytuł, Platformy, Stock, Wiek, CTR, CR, Cena, Marża, #Rekomendacji*
* Akcje masowe: *Otwórz rekomendacje dla zaznaczonych*, *Uruchom sugerowane obniżki/edycje*

---

# 📊 Szczegóły produktu (/products/:id)

**Header:** mini KPI + przyciski akcji (*Edytuj tytuł/zdjęcia/cenę*, *Uruchom eksperyment*, *Wystaw na nowy kanał*)

**Zakładki:**

* **Overview** – podsumowania, sparklines, ostatnie zmiany
* **Analytics** – wykresy: ruch, CTR, CR, porównanie cen vs konkurencja, pora dnia/tygodnia
* **Listing Quality** – score + checklist (tytuł, atrybuty, kategorie, SEO)
* **Images Audit** – miniatury, brakujące ujęcia, rekomendowane kadry
* **Price Intelligence** – konkurenci, rozkład cen, elastyczność
* **Stock & Aging** – dni w magazynie, prognoza rotacji, alerty nadmiaru
* **History** – dziennik zmian (kto/co/kiedy), przyczynowość (rekomendacja → efekt)
* **Experiments** – testy A/B (stan, metryki, p-value w kolejnych iteracjach)

**Prawy panel akcji:** *Apply now*, *Schedule*, *Rollback*, *Add note*.

---

# 🧠 Rekomendacje (/recommendations)

**Widoki:**

* **Feed/Board** (domyślny) – identyczny jak Recommendation Hub z dodatkowymi filtrami (typ, kanał, produkt, zakres dat, status)
* **Batch Apply** – tryb zbiorczy z podsumowaniem wpływu

**Karta rekomendacji – spec:**

* *type*: `price|title|images|seo|distribution|promo`
* *impact/effort/confidence*: skala 0–1 z labelami
* *proposal*: struktura zależna od typu, np. `{ newPrice, compareAt, channel }`, `{ newTitle, seoScoreΔ }`, `{ newImages[] }`
* *preview*: `diff(text)`, `before/after(price)`, `gallery(old/new)`
* *actions*: `apply`, `schedule`, `reject(reason)`, `openProduct`

---

# 🚨 Alerty (/alerts)

* Reguły: *CTR spadek o X% d/d, CR < próg, Wiek zapasu > N dni, Rozjazd cen > Y% vs konkurencja*
* Widok: lista otwartych alertów + timeline rozwiązania

---

# 🧪 Eksperymenty (/experiments)

* Lista testów: hipoteza, warianty, metryki primary/secondary, status
* Szybkie stworzenie testu z produktu lub rekomendacji

---

# 🔌 Integracje (/integrations)

* Konektory: **Shopify, WooCommerce, eBay, Square**
* Statusy: *Connected / Syncing / Error*, ostatnia synchronizacja, logi

---

# ⚙️ Ustawienia (/settings)

* Organizacja, zespół, role
* API keys, webhooki
* Preferencje (waluta, strefa czasu, domyślne zakresy dat)

---

# 🔗 Kontrakt API (REST, przykładowe)

```
GET /api/v1/recommendations?storeId=xyz&status=pending&limit=50
{
  "items": [
    {
      "id":"r42","productId":"p1","type":"price",
      "impact":0.07,"effort":0.2,"confidence":0.72,
      "proposal":{"newPrice":27.99,"channel":"shopify"},
      "preview":{"before":29.99,"after":27.99,"marketMedian":28.49},
      "expected":{"ctrDelta":0.03,"crDelta":0.012}
    }
  ],
  "total": 128
}

POST /api/v1/recommendations/{id}/apply
{ "actor":"userId", "schedule": null }

GET /api/v1/recommendations/applied?from=2025-10-25&to=2025-11-08
{
  "items": [{"id":"r42","appliedAt":"2025-11-07T10:21Z","result":{"ctr":+0.022,"cr":+0.006}}]
}
```

**Uwaga**: **brak modułu Users** – autoryzacja przez token organizacji. Aplikacja zakłada tryb **cloud** (brak lokalnego działania).

---

# 🔌 Warstwa danych & stan

* **TanStack Query (React Query)** do cache’owania i re-fetchu
* **Zod** do walidacji payloadów
* **ErrorBoundary** + **Retry** + **Skeletony**
* Optimistic UI przy **apply recommendation**

---

# 🧩 Biblioteka komponentów (mapowanie)

* **Karty KPI**: `Card` + `CardHeader/Content/Description` + ikony lucide
* **Wykresy**: `recharts` (LineChart, BarChart) – proste konfiguracje, tooltips
* **Tabela**: `Table` + sticky header, kolumny sortowalne, `Badge` dla statusów
* **Panel akcji**: `Sheet` na mobile, `Dialog` na desktop
* **Toasty**: success/error/undo
* **Pills/Tagi**: `Badge` (varianty: default/secondary/destructive)

---

# 📱 Responsywność & stany pustek

* Mobile-first: feed rekomendacji w 1 kolumnie; filtry w `Sheet`
* Pustki: komunikat „Połącz sklep i uruchom pierwszą analizę” + CTA do `/integrations`
* Ładowanie: `Skeleton` dla kart rekomendacji
* **Tryb cloud only**: brak lokalnego uruchomienia – w UI komunikat w Integrations

---

# 🔒 Dostępność & jakość

* Kontrast WCAG AA, focus ringi, `aria-*`, klawiszologia (ESC zamyka Dialog/Sheet)
* Testy e2e *happy path* dla kluczowych flow (Cypress – do rozważenia po hackatonie)

---

# 🧭 Kluczowe flow (MVP)

1. **Onboarding** → `/integrations` → połącz sklep → `/` Dashboard z KPI
2. **Znajdź problematyczne SKU** → `/products` → filtr *Age>60 & Stock>50 & CTR<1%*
3. **Wejdź w szczegóły** → `/products/:id` → zobacz *Listing Quality* & *Images Audit*
4. **Zastosuj rekomendację** → `/recommendations` → *Apply* (optimistic), toast + rollback

---

# 🏗️ Szkielet kodu (skrót)

```tsx
// src/App.tsx – routing ustawiony pod Recommendation Hub
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import AppShell from './components/AppShell'
import RecommendationHub from './routes/RecommendationHub'
import Products from './routes/Products'
import ProductDetails from './routes/ProductDetails'
import Alerts from './routes/Alerts'
import Experiments from './routes/Experiments'
import Integrations from './routes/Integrations'
import Settings from './routes/Settings'

const qc = new QueryClient()
export default function App(){
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <AppShell>
          <Routes>
            <Route path="/" element={<RecommendationHub/>} />
            <Route path="/recommendations" element={<RecommendationHub/>} />
            <Route path="/products" element={<Products/>} />
            <Route path="/products/:id" element={<ProductDetails/>} />
            <Route path="/alerts" element={<Alerts/>} />
            <Route path="/experiments" element={<Experiments/>} />
            <Route path="/integrations" element={<Integrations/>} />
            <Route path="/settings" element={<Settings/>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AppShell>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
```

```tsx
// src/components/AppShell.tsx (priorytet: rekomendacje; bez modułu Users)
import { PropsWithChildren } from 'react'
import { BadgePercent, Bell, Plug, Settings, Store, Boxes, LineChart } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function AppShell({children}: PropsWithChildren){
  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-[260px_1fr]">
      <aside className="hidden lg:flex flex-col border-r p-4 gap-2">
        <div className="text-xl font-semibold flex items-center gap-2"><Store className="h-5 w-5"/>Sales Optimizer</div>
        <nav className="mt-4 grid gap-1">
          <NavItem to="/" label="Recommendation Hub" icon={<BadgePercent className="h-4 w-4"/>} />
          <NavItem to="/products" label="Products" icon={<Boxes className="h-4 w-4"/>} />
          <NavItem to="/alerts" label="Alerts" icon={<Bell className="h-4 w-4"/>} />
          <NavItem to="/experiments" label="Experiments" icon={<LineChart className="h-4 w-4"/>} />
          <NavItem to="/integrations" label="Integrations" icon={<Plug className="h-4 w-4"/>} />
          <NavItem to="/settings" label="Settings" icon={<Settings className="h-4 w-4"/>} />
        </nav>
      </aside>
      <main className="flex flex-col">
        <header className="h-16 border-b flex items-center justify-between px-4 gap-2">
          <div className="font-medium">Store selector • Date range • Global filters</div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">Feedback</Button>
            <Button size="sm">Apply batch</Button>
          </div>
        </header>
        <div className="p-4">{children}</div>
      </main>
    </div>
  )
}

function NavItem({to,label,icon}:{to:string,label:string,icon?:React.ReactNode}){
  return (
    <a href={to} className="px-2 py-2 rounded-lg hover:bg-muted flex items-center gap-2 text-sm">
      {icon}<span>{label}</span>
    </a>
  )
}
```

```tsx
// src/routes/Dashboard.tsx (szkic UI)
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function Dashboard(){
  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 xl:grid-cols-4">
      {['Revenue','Conversion','Slow stock value','Stuck SKUs'].map(k => (
        <Card key={k}><CardHeader><CardTitle>{k}</CardTitle></CardHeader><CardContent>—</CardContent></Card>
      ))}
      <div className="xl:col-span-2">
        <Card><CardHeader><CardTitle>Traffic & Sales</CardTitle></CardHeader><CardContent>LineChart</CardContent></Card>
      </div>
      <div className="xl:col-span-2">
        <Card><CardHeader><CardTitle>Funnel</CardTitle></CardHeader><CardContent>Bars</CardContent></Card>
      </div>
      <div className="xl:col-span-4">
        <Card><CardHeader><CardTitle>Top Stuck SKUs</CardTitle></CardHeader><CardContent>Table</CardContent></Card>
      </div>
    </div>
  )
}
```

---

# 🧪 Dane mock do szybkiej implementacji

```ts
export type Product = {
  id: string; sku: string; title: string; platforms: string[];
  price: number; marginPct: number; stock: number; ageDays: number;
  views: number; ctr: number; cr: number; returnsPct: number; listingScore: number;
}
```

---

# ✅ Roadmap (hackaton)

**Dzień 1**: Layout, routing, Dashboard MVP, lista produktów (mock)

**Dzień 2**: Szczegóły produktu (2–3 zakładki), Rekomendacje (kolejka + apply), Integracje – widok statusu

**Dzień 3**: Alerty, proste eksperymenty, dopieszczony dashboard, polish & demo flow

---

# 🎁 Dodatki „nice to have”

* Undo/rollback po *Apply*
* Presety filtrów i shareable URL
* Eksport CSV z aktualnymi filtrami
* Notatki zespołowe (mini-CRM przy produkcie)
