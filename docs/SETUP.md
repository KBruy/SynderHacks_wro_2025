# Development Setup Guide

> Complete setup instructions for all team members

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Repository Setup](#repository-setup)
3. [Frontend Setup (Person 1)](#frontend-setup)
4. [Backend Setup (Person 2 & 3)](#backend-setup)
5. [Database Setup](#database-setup)
6. [External Services](#external-services)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software (All Team Members)

#### 1. Node.js & npm
```bash
# Check if installed
node --version  # Should be 18.x or higher
npm --version   # Should be 9.x or higher

# Install via nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

#### 2. Git
```bash
# Check if installed
git --version

# Configure (if first time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 3. Code Editor
**Recommended**: Visual Studio Code
- Download from: https://code.visualstudio.com/

**Required Extensions**:
- ESLint (`dbaeumer.vscode-eslint`)
- Prettier (`esbenp.prettier-vscode`)
- GitLens (`eamodio.gitlens`)

**Recommended Extensions**:
- Thunder Client (`rangav.vscode-thunder-client`)
- Prisma (`Prisma.prisma`)
- Tailwind CSS IntelliSense (`bradlc.vscode-tailwindcss`)
- Error Lens (`usernamehw.errorlens`)

**VSCode Settings** (`.vscode/settings.json`):
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

---

## Repository Setup

### 1. Clone Repository

```bash
# Clone the repo
git clone https://github.com/CZIWELLO/KNAlgo.git
cd KNAlgo/SynderHacks_wro_2025

# Verify you're in the right place
ls -la
# Should see: Backend/, Frontend/, CLAUDE.md, TEAM_WORKFLOW.md, etc.
```

### 2. Create Your Feature Branch

```bash
# Update main first
git checkout main
git pull origin main

# Create your branch based on your role
# Frontend Developer:
git checkout -b frontend/initial-setup

# AI Developer:
git checkout -b ai/initial-setup

# Backend Developer:
git checkout -b backend/initial-setup
```

---

## Frontend Setup

> **For**: Person 1 (Frontend Developer)

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install:
- React 18
- TypeScript
- Vite
- shadcn/ui components
- TanStack Query
- React Router
- Recharts
- Zod
- Tailwind CSS
- etc.

### 3. Create Environment File

```bash
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_URL=http://localhost:3000/api/v1
VITE_ENV=development
```

### 4. Initialize shadcn/ui (if not already done)

```bash
npx shadcn-ui@latest init
```

Follow prompts:
- Style: **Default**
- Base color: **Slate**
- CSS variables: **Yes**

### 5. Start Development Server

```bash
npm run dev
```

Should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 6. Verify Frontend is Working

Open browser to `http://localhost:5173`

You should see the app (or a placeholder if not built yet).

### Frontend Project Structure

```
frontend/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── .env
├── index.html
└── src/
    ├── main.tsx           # Entry point
    ├── App.tsx            # Root component
    ├── components/        # Reusable UI components
    │   ├── ui/           # shadcn/ui components
    │   ├── AppShell.tsx  # Layout
    │   └── ...
    ├── routes/           # Page components
    │   ├── RecommendationHub.tsx
    │   ├── Products.tsx
    │   └── ...
    ├── lib/              # Utilities
    │   ├── api.ts       # API client
    │   └── utils.ts     # Helper functions
    ├── hooks/            # Custom React hooks
    ├── types/            # TypeScript types
    └── styles/
        └── globals.css   # Global styles
```

### Frontend Commands

```bash
npm run dev          # Start dev server (localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run type-check   # Check TypeScript types
npm run format       # Format code with Prettier
```

---

## Backend Setup

> **For**: Person 2 (AI Developer) & Person 3 (Backend Developer)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Install Dependencies

```bash
npm install
```

This will install:
- NestJS (or Express)
- TypeScript
- Prisma ORM
- BullMQ (Redis queue)
- OpenAI SDK
- LangChain
- Zod
- etc.

### 3. Create Environment File

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Server
NODE_ENV=development
PORT=3000

# Database (PostgreSQL)
DATABASE_URL="postgresql://postgres:password@localhost:5432/sales_optimizer?schema=public"

# Redis (for queue and cache)
REDIS_URL="redis://localhost:6379"

# JWT Authentication
JWT_SECRET="your-super-secret-key-change-in-production"

# OpenAI API
OPENAI_API_KEY="sk-your-api-key-here"

# Platform API Keys (add when ready)
SHOPIFY_CLIENT_ID=""
SHOPIFY_CLIENT_SECRET=""
SHOPIFY_API_VERSION="2024-01"

WOOCOMMERCE_URL=""
WOOCOMMERCE_CONSUMER_KEY=""
WOOCOMMERCE_CONSUMER_SECRET=""

EBAY_CLIENT_ID=""
EBAY_CLIENT_SECRET=""
```

### 4. Setup Database

#### Option A: Local PostgreSQL

**Install PostgreSQL**:
```bash
# macOS (with Homebrew)
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download from: https://www.postgresql.org/download/windows/
```

**Create Database**:
```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE sales_optimizer;
CREATE USER sales_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE sales_optimizer TO sales_user;
\q
```

Update `DATABASE_URL` in `.env`:
```env
DATABASE_URL="postgresql://sales_user:password@localhost:5432/sales_optimizer?schema=public"
```

#### Option B: Supabase (Cloud PostgreSQL - Recommended for Hackathon)

1. Go to https://supabase.com
2. Create free account
3. Create new project
4. Wait for database to provision (~2 min)
5. Go to **Settings** → **Database**
6. Copy **Connection String** (URI format)
7. Paste into `.env` as `DATABASE_URL`

Example:
```env
DATABASE_URL="postgresql://postgres:your-password@db.xxx.supabase.co:5432/postgres"
```

### 5. Setup Redis

#### Option A: Local Redis

**Install Redis**:
```bash
# macOS (with Homebrew)
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Windows
# Download from: https://github.com/microsoftarchive/redis/releases
```

**Verify Redis is running**:
```bash
redis-cli ping
# Should return: PONG
```

#### Option B: Upstash (Cloud Redis - Recommended for Hackathon)

1. Go to https://upstash.com
2. Create free account
3. Create Redis database
4. Copy **UPSTASH_REDIS_REST_URL** or connection string
5. Paste into `.env` as `REDIS_URL`

Example:
```env
REDIS_URL="rediss://default:xxx@xxx.upstash.io:6379"
```

### 6. Run Database Migrations

```bash
# Generate Prisma client
npx prisma generate

# Run migrations (creates tables)
npx prisma migrate dev --name init

# Optional: Seed database with test data
npx prisma db seed
```

### 7. Start Development Server

```bash
npm run dev
```

Should see:
```
[Nest] 12345  - 11/08/2025, 10:00:00 AM     LOG [NestFactory] Starting Nest application...
[Nest] 12345  - 11/08/2025, 10:00:00 AM     LOG [InstanceLoader] AppModule dependencies initialized
[Nest] 12345  - 11/08/2025, 10:00:00 AM     LOG Application listening on http://localhost:3000
```

### 8. Verify Backend is Working

**Test health endpoint**:
```bash
curl http://localhost:3000/api/v1/health
```

Should return:
```json
{
  "status": "ok",
  "time": "2025-11-08T10:00:00Z"
}
```

### Backend Project Structure

```
backend/
├── package.json
├── tsconfig.json
├── .env
├── prisma/
│   ├── schema.prisma      # Database schema
│   ├── migrations/        # Migration history
│   └── seed.ts           # Test data seeding
└── src/
    ├── main.ts           # Entry point
    ├── app.module.ts     # Root module
    ├── api/              # REST API controllers
    │   ├── recommendations.controller.ts
    │   ├── products.controller.ts
    │   └── ...
    ├── connectors/       # Platform integrations
    │   ├── shopify/
    │   │   ├── shopify.service.ts
    │   │   ├── shopify.connector.ts
    │   │   └── shopify.types.ts
    │   ├── woocommerce/
    │   └── ebay/
    ├── ai/               # AI/ML services
    │   ├── analysis.service.ts
    │   ├── recommendations.service.ts
    │   └── prompts/
    │       ├── market-analysis.ts
    │       └── price-optimization.ts
    ├── sync/             # Synchronization logic
    │   ├── sync.service.ts
    │   └── sync.scheduler.ts
    ├── queue/            # Job queue processors
    │   ├── queue.module.ts
    │   └── processors/
    ├── types/            # Shared TypeScript types
    ├── utils/            # Utilities
    └── config/           # Configuration
```

### Backend Commands

```bash
npm run dev          # Start dev server with hot reload
npm run build        # Build for production
npm run start:prod   # Run production build
npm run lint         # Run ESLint
npm run test         # Run unit tests
npm run test:e2e     # Run integration tests

# Prisma commands
npx prisma studio    # Open database GUI (localhost:5555)
npx prisma migrate dev --name <name>  # Create new migration
npx prisma generate  # Regenerate Prisma client
npx prisma db seed   # Seed database with test data
```

---

## Database Setup

### Prisma Schema Overview

The database schema is defined in `backend/prisma/schema.prisma`:

**Key models**:
- `Product` - Product information
- `Channel` - Platform integrations (Shopify, WooCommerce, etc.)
- `Recommendation` - AI-generated recommendations
- `SyncJob` - Sync job history
- `Report` - Generated reports

### Viewing Database

**Prisma Studio** (GUI):
```bash
cd backend
npx prisma studio
```

Opens browser at `http://localhost:5555` with database viewer.

**Direct SQL**:
```bash
# PostgreSQL
psql $DATABASE_URL

# Or with connection string
psql "postgresql://user:pass@localhost:5432/sales_optimizer"
```

---

## External Services

### OpenAI API Key

**Required for**: AI analysis and recommendations

1. Go to https://platform.openai.com
2. Create account / Login
3. Go to **API Keys** section
4. Click **Create new secret key**
5. Copy key (starts with `sk-`)
6. Add to `backend/.env`:
   ```env
   OPENAI_API_KEY="sk-your-key-here"
   ```

**Important**:
- Keep track of usage (costs money!)
- Set usage limits in OpenAI dashboard
- Never commit API keys to git

### Platform API Keys (Optional for MVP)

These can be added later when implementing integrations:

#### Shopify
1. Create Shopify Partner account: https://partners.shopify.com
2. Create development store
3. Create app
4. Get API credentials

#### WooCommerce
1. Install WooCommerce on WordPress site
2. Go to **WooCommerce** → **Settings** → **Advanced** → **REST API**
3. Add key
4. Copy Consumer Key and Secret

#### eBay
1. Create eBay Developer account: https://developer.ebay.com
2. Create app
3. Get Client ID and Secret

---

## Verification

### Full Stack Test

**1. Start Backend**:
```bash
cd backend
npm run dev
# Should be running on localhost:3000
```

**2. Start Frontend** (new terminal):
```bash
cd frontend
npm run dev
# Should be running on localhost:5173
```

**3. Test Connection**:

Open browser to `http://localhost:5173`

Check browser console (F12):
- No CORS errors
- API calls working (check Network tab)

**4. Test API Directly**:
```bash
# Health check
curl http://localhost:3000/api/v1/health

# Get recommendations (should return empty array or mock data)
curl http://localhost:3000/api/v1/recommendations
```

---

## Troubleshooting

### Frontend Issues

#### "Cannot connect to backend"
```bash
# Check backend is running
curl http://localhost:3000/api/v1/health

# Check VITE_API_URL in frontend/.env
cat frontend/.env

# Check browser console for CORS errors
# If CORS error: add CORS config in backend
```

#### "Module not found" errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend Issues

#### "Database connection failed"
```bash
# Test database connection
cd backend
npx prisma db pull

# Check DATABASE_URL format
echo $DATABASE_URL

# For PostgreSQL, ensure database exists
psql postgres -c "\l"
```

#### "Redis connection failed"
```bash
# Test Redis connection
redis-cli ping
# Should return: PONG

# If not working, start Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

#### "Prisma Client not generated"
```bash
cd backend
npx prisma generate
```

#### "Migration failed"
```bash
# Reset database (⚠️ deletes all data)
npx prisma migrate reset

# Or fix manually in Prisma Studio
npx prisma studio
```

### OpenAI API Issues

#### "Invalid API key"
```bash
# Verify key in .env
cat backend/.env | grep OPENAI_API_KEY

# Test key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### "Rate limit exceeded"
- Wait a few seconds
- Implement retry logic with exponential backoff
- Consider caching results

### Git Issues

#### "Cannot push to main"
```bash
# Main is protected - create PR instead
git checkout -b <role>/feature-name
git push origin <role>/feature-name
# Then create PR on GitHub
```

#### "Merge conflict"
```bash
# See TEAM_WORKFLOW.md for detailed resolution steps
git status  # Shows conflicted files
# Edit files to resolve
git add .
git commit -m "merge: resolve conflicts"
```

---

## Next Steps

### Frontend Developer
1. ✅ Complete setup above
2. Read `/Frontend/struct.md` for UI architecture
3. Start with AppShell layout
4. Implement Recommendation Hub

### AI Developer
1. ✅ Complete backend setup above
2. Read OpenAI API docs
3. Start with simple prompt template
4. Implement basic recommendation service

### Backend Developer
1. ✅ Complete backend setup above
2. Read `/Backend/backend_api_spec.md`
3. Implement health endpoint
4. Start with products API endpoint

---

## Useful Resources

### Documentation
- [Project CLAUDE.md](../CLAUDE.md)
- [Team Workflow](../TEAM_WORKFLOW.md)
- [Backend API Spec](../Backend/backend_api_spec.md)
- [Frontend Structure](../Frontend/struct.md)

### External Docs
- [React](https://react.dev)
- [TypeScript](https://www.typescriptlang.org/docs/)
- [shadcn/ui](https://ui.shadcn.com)
- [TanStack Query](https://tanstack.com/query/latest)
- [NestJS](https://docs.nestjs.com)
- [Prisma](https://www.prisma.io/docs)
- [OpenAI API](https://platform.openai.com/docs)

---

## Need Help?

1. Check troubleshooting section above
2. Search in documentation
3. Ask in team chat (#dev-general)
4. Create issue with `question` label

---

**Last Updated**: 2025-11-08

Happy coding! 🚀
