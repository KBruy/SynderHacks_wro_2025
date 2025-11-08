# Quick Start Guide - Start Coding in 5 Minutes

> Szybki przewodnik dla każdego członka zespołu

---

## Przed rozpoczęciem pracy

### 1. Przeczytaj dokumentację (15 min)

**Obowiązkowe**:
- [ ] [README.md](README.md) - Przegląd projektu
- [ ] [CLAUDE.md](CLAUDE.md) - Jak pracować z Claude Code
- [ ] [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) - Jak współpracować w zespole

**Opcjonalne** (przeczytaj później):
- [docs/SETUP.md](docs/SETUP.md) - Szczegółowy setup
- [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) - Git workflow
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architektura

---

## Setup (zależnie od roli)

### Wszyscy członkowie zespołu

```bash
# 1. Sklonuj repo
git clone https://github.com/CZIWELLO/KNAlgo.git
cd KNAlgo/SynderHacks_wro_2025

# 2. Sprawdź czy masz Node.js 18+
node --version

# 3. Skonfiguruj Git
git config user.name "Twoje Imię"
git config user.email "twoj@email.com"

# 4. Stwórz swoją branch
git checkout -b <role>/<feature-name>
# Przykład: frontend/initial-setup
```

---

### Person 1: Frontend Developer

```bash
# 1. Przejdź do katalogu frontend
cd frontend

# 2. Zainstaluj zależności
npm install

# 3. Stwórz plik .env
cat > .env << EOF
VITE_API_URL=http://localhost:3000/api/v1
VITE_ENV=development
EOF

# 4. Uruchom dev server
npm run dev

# ✅ Frontend działa na http://localhost:5173
```

**Co dalej?**:
1. Przeczytaj `Frontend/struct.md`
2. Zainstaluj VSCode extensions (ESLint, Prettier)
3. Rozpocznij pracę nad AppShell lub Recommendation Hub

---

### Person 2 & 3: Backend/AI Developers

#### Opcja A: Lokalna baza (więcej pracy)

```bash
# 1. Zainstaluj PostgreSQL
brew install postgresql@14  # macOS
# LUB
sudo apt-get install postgresql  # Linux

# 2. Zainstaluj Redis
brew install redis  # macOS
# LUB
sudo apt-get install redis-server  # Linux

# 3. Uruchom serwisy
brew services start postgresql
brew services start redis

# 4. Stwórz bazę danych
createdb sales_optimizer
```

#### Opcja B: Cloud (szybsza, rekomendowana)

**Supabase** (PostgreSQL):
1. Idź na https://supabase.com
2. Zarejestruj się
3. Stwórz nowy projekt
4. Skopiuj **Connection String**

**Upstash** (Redis):
1. Idź na https://upstash.com
2. Zarejestruj się
3. Stwórz Redis database
4. Skopiuj **Connection String**

#### Backend Setup

```bash
# 1. Przejdź do katalogu backend
cd backend

# 2. Zainstaluj zależności
npm install

# 3. Stwórz plik .env
cat > .env << EOF
NODE_ENV=development
PORT=3000

# Database (użyj swojego connection string)
DATABASE_URL="postgresql://user:pass@localhost:5432/sales_optimizer"

# Redis (użyj swojego connection string)
REDIS_URL="redis://localhost:6379"

# OpenAI (dodaj swój klucz)
OPENAI_API_KEY="sk-your-key-here"

# JWT Secret (wygeneruj losowy)
JWT_SECRET="$(openssl rand -base64 32)"

# Platform API Keys (dodaj później)
SHOPIFY_CLIENT_ID=""
SHOPIFY_CLIENT_SECRET=""
WOOCOMMERCE_CONSUMER_KEY=""
WOOCOMMERCE_CONSUMER_SECRET=""
EOF

# 4. Uruchom migracje
npx prisma migrate dev
npx prisma generate

# 5. Uruchom dev server
npm run dev

# ✅ Backend działa na http://localhost:3000
```

**Weryfikacja**:
```bash
curl http://localhost:3000/api/v1/health
# Powinno zwrócić: {"status":"ok","time":"..."}
```

---

## Twój pierwszy task

### Person 1 (Frontend)

**Task**: Stwórz podstawowy AppShell (layout)

```bash
# 1. Stwórz branch
git checkout -b frontend/app-shell

# 2. Uruchom Claude Code i powiedz:
"Pomóż mi stworzyć AppShell component zgodnie z Frontend/struct.md.
Potrzebuję:
- Sidebar z nawigacją
- Topbar z filtrami
- Main content area
Użyj shadcn/ui components."

# 3. Testuj zmiany
npm run dev

# 4. Commit i push
git add .
git commit -m "feat(frontend): add AppShell layout component"
git push origin frontend/app-shell

# 5. Stwórz PR
```

### Person 2 (AI Developer)

**Task**: Stwórz podstawowy prompt template dla analizy rynku

```bash
# 1. Stwórz branch
git checkout -b ai/market-analysis-prompt

# 2. Uruchom Claude Code i powiedz:
"Pomóż mi stworzyć prompt template dla GPT-4 do analizy rynku produktu.
Potrzebuję:
- Template w /backend/src/ai/prompts/market-analysis.ts
- Podstawowy service do wywołania OpenAI API
- Zod schema do walidacji odpowiedzi"

# 3. Testuj
npm run dev

# 4. Commit i push
git add .
git commit -m "feat(ai): add market analysis prompt template"
git push origin ai/market-analysis-prompt

# 5. Stwórz PR
```

### Person 3 (Backend Developer)

**Task**: Stwórz podstawową strukturę API i health endpoint

```bash
# 1. Stwórz branch
git checkout -b backend/api-structure

# 2. Uruchom Claude Code i powiedz:
"Pomóż mi stworzyć strukturę API zgodnie z Backend/backend_api_spec.md.
Potrzebuję:
- Moduł products z kontrolerem
- Moduł recommendations z kontrolerem
- Health endpoint
- Podstawową konfigurację NestJS"

# 3. Testuj
npm run dev
curl http://localhost:3000/api/v1/health

# 4. Commit i push
git add .
git commit -m "feat(backend): add API structure and health endpoint"
git push origin backend/api-structure

# 5. Stwórz PR
```

---

## Praca z Claude Code

### Rozpoczęcie pracy

1. Otwórz VSCode w katalogu projektu
2. Uruchom Claude Code (jeśli używasz)
3. Powiedz Claude którą częścią projektu się zajmujesz:

**Przykłady**:
```
"Jestem frontend developerem, pracuję nad Recommendation Hub"

"Jestem AI developerem, chcę zaimplementować market analysis"

"Jestem backend developerem, buduję Shopify connector"
```

### Dobre praktyki z Claude

**DO** ✅:
- Powiedz Claude nad czym pracujesz
- Odwołuj się do dokumentacji (CLAUDE.md, API spec)
- Poproś o wyjaśnienie jeśli coś niejasne
- Testuj kod przed commitem

**DON'T** ❌:
- Nie commituj kodu bez testowania
- Nie zmieniaj API contracts bez konsultacji z zespołem
- Nie pracuj na branchu `main`

---

## Daily Workflow

### Rano (5 min)

```bash
# 1. Pull latest changes
git checkout main
git pull origin main

# 2. Update your branch
git checkout <your-branch>
git merge main

# 3. Start dev server
cd frontend  # lub backend
npm run dev
```

### Podczas pracy (każde 30-60 min)

```bash
# Commit i push regularnie
git add .
git commit -m "feat(scope): what you did"
git push origin <your-branch>
```

### Wieczorem (5 min)

```bash
# Push final changes
git add .
git commit -m "feat(scope): end of day summary"
git push origin <your-branch>

# Napisz update w team chat:
# "Dzisiaj zrobiłem X, jutro planuję Y, problemy: Z"
```

---

## Checklist przed stworzeniem PR

- [ ] Kod się kompiluje bez błędów
- [ ] Przetestowałeś funkcjonalność ręcznie
- [ ] Nie ma błędów TypeScript
- [ ] Kod sformatowany (Prettier)
- [ ] Usunięte `console.log` (chyba że celowe)
- [ ] Branch zaktualizowany z `main`
- [ ] Wypełniony opis PR

---

## Troubleshooting

### "npm install" fails

```bash
# Wyczyść cache i spróbuj ponownie
rm -rf node_modules package-lock.json
npm install
```

### "Cannot connect to database"

```bash
# Sprawdź format DATABASE_URL
echo $DATABASE_URL

# Dla lokalnej bazy:
DATABASE_URL="postgresql://user:password@localhost:5432/sales_optimizer"

# Dla Supabase:
DATABASE_URL="postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"
```

### "Port already in use"

```bash
# Backend (3000)
lsof -ti:3000 | xargs kill

# Frontend (5173)
lsof -ti:5173 | xargs kill
```

### Stuck? Potrzebujesz pomocy?

1. Sprawdź [docs/SETUP.md](docs/SETUP.md#troubleshooting)
2. Zapytaj w team chat
3. Stwórz issue z labelem `question`

---

## Przydatne Komendy

### Git

```bash
git status                    # Co się zmieniło?
git log --oneline -10        # Ostatnie commity
git diff                     # Zobacz zmiany

git stash                    # Zapisz zmiany tymczasowo
git stash pop                # Przywróć zmiany
```

### NPM

```bash
npm run dev          # Uruchom dev server
npm run build        # Zbuduj produkcję
npm run lint         # Sprawdź kod
npm run format       # Formatuj kod
```

### Prisma (Backend)

```bash
npx prisma studio           # GUI dla bazy danych
npx prisma migrate dev      # Uruchom migracje
npx prisma generate         # Wygeneruj Prisma client
```

---

## Resources

- **Team Chat**: #dev-general
- **PR Reviews**: #dev-prs
- **Documentation**: Zobacz [README.md](README.md#documentation)

---

**Gotowy do kodowania?**

1. Setup your environment ✅
2. Create your branch ✅
3. Start dev server ✅
4. Ask Claude for help ✅
5. Start coding! 🚀

---

**Pytania?** Zapytaj w team chat lub zobacz [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md)
