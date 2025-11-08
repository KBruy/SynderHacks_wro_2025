<?php
// Prosty "router" po query stringu, np. ?tab=produkty
$tab = $_GET['tab'] ?? 'rekomendacje';

$menu = [
  'rekomendacje' => 'Rekomendacje',
  'produkty' => 'Produkty',
  'kanaly' => 'Kanały sprzedaży',
  'ceny' => 'Ceny & Promocje',
  'raporty' => 'Raporty',
  'ustawienia' => 'Ustawienia',
];

function is_active(string $key, string $current): string {
  return $key === $current ? ' is-active' : '';
}
?>
<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Hackaton – Dashboard (PHP)</title>
  <link rel="stylesheet" href="./styles.css" />
</head>
<body>
  <header class="topbar">
    <div class="topbar__title">Hackaton • Sales Optimizer</div>
    <nav class="topbar__nav">
      <a href="?tab=rekomendacje"<?= $tab==='rekomendacje' ? ' aria-current="page"' : '' ?>>Dashboard</a>
      <a href="?tab=raporty"<?= $tab==='raporty' ? ' aria-current="page"' : '' ?>>Raporty</a>
      <a href="?tab=ustawienia"<?= $tab==='ustawienia' ? ' aria-current="page"' : '' ?>>Ustawienia</a>
    </nav>
  </header>

  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar__brand">
        <span class="logo">🧭</span>
        <span class="brand">Panel</span>
      </div>

      <nav class="menu">
        <?php foreach ($menu as $key => $label): ?>
          <a class="menu__item<?= is_active($key, $tab) ?>" href="?tab=<?= htmlspecialchars($key) ?>">
            <?= htmlspecialchars($label) ?>
          </a>
        <?php endforeach; ?>
      </nav>

      <div class="sidebar__footer">
        <small>v0.1 • prototyp (PHP)</small>
      </div>
    </aside>

    <!-- Content -->
    <main class="content">
      <?php switch ($tab):
        case 'rekomendacje': ?>
          <section class="card">
            <h1>Rekomendacje AI</h1>
            <p>Najważniejsze działania dla produktów o niskiej rotacji.</p>

            <div class="grid">
              <article class="tile">
                <h2>Zmiana ceny</h2>
                <p>Proponowana korekta: <strong>−7%</strong> dla SKU: <code>ABC-123</code>.</p>
                <a class="btn" href="#">Zobacz szczegóły</a>
              </article>

              <article class="tile">
                <h2>SEO/Opis</h2>
                <p>Dodaj frazy „outdoor, wodoodporny, lekki” do tytułu/opisu.</p>
                <a class="btn" href="#">Podgląd zmian</a>
              </article>

              <article class="tile">
                <h2>Dystrybucja</h2>
                <p>Włącz na: <strong>eBay</strong> i <strong>Shopify</strong> — wzrost zasięgu 18–24%.</p>
                <a class="btn" href="#">Konfiguruj kanały</a>
              </article>
            </div>
          </section>

          <section class="card">
            <h2>Ostatnie zdarzenia</h2>
            <ul class="events">
              <li><time>08.11</time> Import danych z WooCommerce (152 pozycje)</li>
              <li><time>08.11</time> Aktualizacja prognoz sprzedaży</li>
              <li><time>07.11</time> Dodano kanał: Shopify</li>
            </ul>
          </section>
        <?php break; ?>

        <?php case 'produkty': ?>
          <section class="card">
            <h1>Produkty</h1>
            <p>Tu wczytamy listę produktów z backendu (REST). Na razie placeholder.</p>
            <div class="grid">
              <article class="tile">
                <h2>SKU: ABC-123</h2>
                <p>Stan: 42 szt. • Rotacja: niska</p>
                <a class="btn" href="#">Szczegóły</a>
              </article>
              <article class="tile">
                <h2>SKU: XYZ-987</h2>
                <p>Stan: 8 szt. • Rotacja: średnia</p>
                <a class="btn" href="#">Szczegóły</a>
              </article>
            </div>
          </section>
        <?php break; ?>

        <?php case 'kanaly': ?>
          <section class="card">
            <h1>Kanały sprzedaży</h1>
            <p>WooCommerce • Shopify • eBay • Square — statusy integracji.</p>
            <div class="grid">
              <article class="tile">
                <h2>WooCommerce</h2>
                <p>Status: połączono • Ostatnia sync: 08.11</p>
                <a class="btn" href="#">Ustawienia</a>
              </article>
              <article class="tile">
                <h2>Shopify</h2>
                <p>Status: połączono • Ostatnia sync: 07.11</p>
                <a class="btn" href="#">Ustawienia</a>
              </article>
              <article class="tile">
                <h2>eBay</h2>
                <p>Status: rozłączono</p>
                <a class="btn" href="#">Połącz</a>
              </article>
            </div>
          </section>
        <?php break; ?>

        <?php case 'ceny': ?>
          <section class="card">
            <h1>Ceny & Promocje</h1>
            <p>Tu pojawią się rekomendacje korekt cen i reguły promocji.</p>
          </section>
        <?php break; ?>

        <?php case 'raporty': ?>
          <section class="card">
            <h1>Raporty</h1>
            <p>Generowanie raportów PDF/CSV (sprzedaż, rotacja, skuteczność rekomendacji).</p>
          </section>
        <?php break; ?>

        <?php case 'ustawienia': ?>
          <section class="card">
            <h1>Ustawienia</h1>
            <p>Konfiguracja API, klucze, preferencje UI.</p>
          </section>
        <?php break; ?>

        <?php default: ?>
          <section class="card">
            <h1>Nie znaleziono sekcji</h1>
            <p>Sprawdź parametr <code>?tab=</code>.</p>
          </section>
      <?php endswitch; ?>
    </main>
  </div>

  <footer class="footer">
    <p>© 2025 Hackaton Team • Frontend: React (docelowo), REST API (JSON)</p>
  </footer>
</body>
</html>
