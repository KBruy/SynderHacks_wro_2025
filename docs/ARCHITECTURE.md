# System Architecture

> Architektura techniczna Sales Optimizer Platform

---

## Spis Treści

1. [Przegląd Systemu](#przegląd-systemu)
2. [Architektura Wysokiego Poziomu](#architektura-wysokiego-poziomu)
3. [Komponenty Frontend](#komponenty-frontend)
4. [Komponenty Backend](#komponenty-backend)
5. [Baza Danych](#baza-danych)
6. [AI/ML Pipeline](#aiml-pipeline)
7. [Integracje Zewnętrzne](#integracje-zewnętrzne)
8. [Przepływ Danych](#przepływ-danych)
9. [Bezpieczeństwo](#bezpieczeństwo)
10. [Skalowalność](#skalowalność)

---

## Przegląd Systemu

### Cel Platformy

**Sales Optimizer** to platforma AI-driven do zarządzania małym biznesem e-commerce, która:
- Synchronizuje oferty między platformami (Shopify, WooCommerce, eBay)
- Analizuje rynek i generuje rekomendacje cenowe/promocyjne
- Automatycznie tworzy i modyfikuje oferty
- Dostarcza analytics i insights

### Kluczowe Funkcjonalności

1. **Multi-platform Sync**: Dwukierunkowa synchronizacja produktów
2. **AI Analysis**: GPT-4 powered analiza rynku i konkurencji
3. **Smart Recommendations**: Automatyczne propozycje akcji (ceny, promocje, bundle)
4. **Action Executor**: Wdrażanie zmian na platformach z rollback
5. **Analytics Dashboard**: Metryki, wykresy, raporty

---

## Architektura Wysokiego Poziomu

```
┌────────────────────────────────────────────────────────────┐
│                         USER                                │
│                    (Web Browser)                            │
└───────────────────────┬────────────────────────────────────┘
                        │ HTTPS
┌───────────────────────▼────────────────────────────────────┐
│                   FRONTEND LAYER                            │
│         React SPA (Vercel / CloudFlare Pages)               │
│   • React Router  • TanStack Query  • shadcn/ui             │
└───────────────────────┬────────────────────────────────────┘
                        │ REST API (JSON)
┌───────────────────────▼────────────────────────────────────┐
│                  API GATEWAY LAYER                          │
│                   NestJS / Express                          │
│   • Authentication (JWT)  • Rate Limiting                   │
│   • Request Validation    • CORS                            │
└────┬──────────────────┬──────────────────┬─────────────────┘
     │                  │                  │
     ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐
│   SYNC      │  │  AI/ML      │  │   ACTION            │
│  SERVICE    │  │ ENGINE      │  │  EXECUTOR           │
│             │  │             │  │                     │
│ • Shopify   │  │ • GPT-4     │  │ • Apply changes     │
│ • WooComm   │  │ • Analysis  │  │ • Rollback          │
│ • eBay      │  │ • Recs      │  │ • Audit log         │
└──────┬──────┘  └──────┬──────┘  └──────┬──────────────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
       ┌────────────────────────────────┐
       │      DATA LAYER                │
       │                                │
       │  ┌──────────┐  ┌───────────┐  │
       │  │PostgreSQL│  │   Redis   │  │
       │  │(Supabase)│  │ (Upstash) │  │
       │  └──────────┘  └───────────┘  │
       └────────────────────────────────┘
                        │
       ┌────────────────▼────────────────┐
       │    EXTERNAL SERVICES            │
       │  • Shopify API                  │
       │  • WooCommerce API              │
       │  • eBay API                     │
       │  • OpenAI API                   │
       └─────────────────────────────────┘
```

---

## Komponenty Frontend

### Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Routing**: React Router 6
- **State Management**: TanStack Query (server state) + React Context (UI state)
- **UI Library**: shadcn/ui + Tailwind CSS
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios / Fetch

### Struktura Komponentów

```
src/
├── components/
│   ├── ui/              # shadcn/ui base components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── layout/          # Layout components
│   │   ├── AppShell.tsx
│   │   ├── Sidebar.tsx
│   │   └── Topbar.tsx
│   ├── recommendation/  # Feature: Recommendations
│   │   ├── RecommendationCard.tsx
│   │   ├── RecommendationList.tsx
│   │   └── ApplyButton.tsx
│   └── products/        # Feature: Products
│       ├── ProductTable.tsx
│       ├── ProductCard.tsx
│       └── ProductFilters.tsx
├── routes/              # Page components
│   ├── RecommendationHub.tsx
│   ├── Products.tsx
│   ├── ProductDetails.tsx
│   └── ...
├── lib/
│   ├── api.ts          # API client
│   ├── queryClient.ts  # TanStack Query config
│   └── utils.ts        # Helpers
├── hooks/
│   ├── useRecommendations.ts
│   ├── useProducts.ts
│   └── useAuth.ts
└── types/              # TypeScript types (synced from backend)
    ├── recommendation.ts
    ├── product.ts
    └── api.ts
```

### Key Patterns

#### API Client (lib/api.ts)

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
```

#### Data Fetching with TanStack Query

```typescript
// hooks/useRecommendations.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'

export function useRecommendations() {
  return useQuery({
    queryKey: ['recommendations'],
    queryFn: () => api.get('/recommendations').then(r => r.data),
    staleTime: 30_000,
  })
}

export function useApplyRecommendation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (recId: string) =>
      api.post(`/recommendations/${recId}/apply`),
    onSuccess: () => {
      queryClient.invalidateQueries(['recommendations'])
    },
  })
}
```

---

## Komponenty Backend

### Tech Stack

- **Framework**: NestJS (Node.js + TypeScript)
- **ORM**: Prisma
- **Queue**: BullMQ (Redis)
- **Validation**: Zod / class-validator
- **Authentication**: JWT (Passport.js)
- **Testing**: Jest + Supertest

### Struktura Modułów

```
src/
├── main.ts                    # Bootstrap
├── app.module.ts              # Root module
├── config/                    # Configuration
│   ├── database.config.ts
│   └── redis.config.ts
├── common/                    # Shared utilities
│   ├── decorators/
│   ├── filters/
│   ├── guards/
│   └── interceptors/
├── modules/
│   ├── auth/                  # Authentication
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── jwt.strategy.ts
│   ├── products/              # Products module
│   │   ├── products.controller.ts
│   │   ├── products.service.ts
│   │   └── dto/
│   ├── recommendations/       # Recommendations module
│   │   ├── recommendations.controller.ts
│   │   ├── recommendations.service.ts
│   │   └── dto/
│   ├── sync/                  # Sync module
│   │   ├── sync.controller.ts
│   │   ├── sync.service.ts
│   │   ├── sync.queue.ts
│   │   └── processors/
│   ├── ai/                    # AI/ML module
│   │   ├── ai.service.ts
│   │   ├── analysis.service.ts
│   │   ├── prompts/
│   │   └── llm/
│   └── connectors/            # Platform connectors
│       ├── shopify/
│       ├── woocommerce/
│       └── ebay/
├── prisma/
│   ├── schema.prisma
│   └── migrations/
└── types/                     # Shared types
    └── index.ts
```

### Kluczowe Wzorce

#### Controller Pattern (NestJS)

```typescript
// modules/recommendations/recommendations.controller.ts
@Controller('api/v1/recommendations')
@UseGuards(JwtAuthGuard)
export class RecommendationsController {
  constructor(private recommendationsService: RecommendationsService) {}

  @Get()
  async findAll(@Query() query: RecommendationsQueryDto) {
    const items = await this.recommendationsService.findAll(query)
    return { items, meta: { page: 1, total: items.length } }
  }

  @Post(':id/apply')
  async apply(@Param('id') id: string, @Body() body: ApplyDto) {
    return await this.recommendationsService.apply(id, body)
  }
}
```

#### Service Pattern

```typescript
// modules/recommendations/recommendations.service.ts
@Injectable()
export class RecommendationsService {
  constructor(
    private prisma: PrismaService,
    private aiService: AIService,
    private actionExecutor: ActionExecutorService,
  ) {}

  async findAll(query: RecommendationsQueryDto) {
    return await this.prisma.recommendation.findMany({
      where: { status: 'pending' },
      include: { product: true },
    })
  }

  async apply(id: string, dto: ApplyDto) {
    const rec = await this.prisma.recommendation.findUnique({ where: { id } })
    return await this.actionExecutor.execute(rec)
  }
}
```

---

## Baza Danych

### Schema Prisma

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Product {
  id            String   @id @default(cuid())
  sku           String   @unique
  name          String
  description   String?
  price         Float
  stock         Int
  rotation      Rotation @default(LOW)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  channels      ProductChannel[]
  recommendations Recommendation[]
}

model Channel {
  id            String   @id @default(cuid())
  type          ChannelType
  name          String
  status        ChannelStatus
  credentials   Json     // Encrypted
  lastSync      DateTime?
  createdAt     DateTime @default(now())

  products      ProductChannel[]
  syncJobs      SyncJob[]
}

model ProductChannel {
  id            String   @id @default(cuid())
  productId     String
  channelId     String
  externalId    String   // Platform's product ID
  status        String
  lastSynced    DateTime?

  product       Product  @relation(fields: [productId], references: [id])
  channel       Channel  @relation(fields: [channelId], references: [id])

  @@unique([productId, channelId])
}

model Recommendation {
  id            String   @id @default(cuid())
  productId     String
  type          RecommendationType
  title         String
  summary       String
  impact        Float    // 0-1
  effort        Float    // 0-1
  confidence    Float    // 0-1
  status        RecommendationStatus
  proposal      Json     // Structured recommendation
  reasoning     String?
  createdAt     DateTime @default(now())
  appliedAt     DateTime?

  product       Product  @relation(fields: [productId], references: [id])
}

model SyncJob {
  id            String   @id @default(cuid())
  channelId     String
  status        JobStatus
  type          SyncType
  startedAt     DateTime @default(now())
  completedAt   DateTime?
  error         String?
  itemsProcessed Int     @default(0)

  channel       Channel  @relation(fields: [channelId], references: [id])
}

enum ChannelType {
  SHOPIFY
  WOOCOMMERCE
  EBAY
}

enum ChannelStatus {
  CONNECTED
  DISCONNECTED
  ERROR
}

enum Rotation {
  LOW
  MEDIUM
  HIGH
}

enum RecommendationType {
  PRICE_CHANGE
  PROMOTION
  BUNDLE
  TITLE_OPTIMIZATION
  IMAGE_UPDATE
  CHANNEL_DISTRIBUTION
}

enum RecommendationStatus {
  PENDING
  APPLIED
  REJECTED
  EXPIRED
}

enum JobStatus {
  QUEUED
  RUNNING
  COMPLETED
  FAILED
}

enum SyncType {
  FULL
  INCREMENTAL
  WEBHOOK
}
```

### Indeksy i Optymalizacja

```prisma
model Product {
  // ... fields ...

  @@index([sku])
  @@index([rotation])
  @@index([createdAt])
}

model Recommendation {
  // ... fields ...

  @@index([productId])
  @@index([status])
  @@index([createdAt])
}
```

---

## AI/ML Pipeline

### Architektura AI Engine

```
┌────────────────────────────────────────────┐
│         AI Analysis Pipeline               │
├────────────────────────────────────────────┤
│                                            │
│  1. Data Collection                        │
│     ├─ Product data (DB)                   │
│     ├─ Market data (web scraping/APIs)     │
│     └─ Historical performance              │
│                                            │
│  2. Preprocessing                          │
│     ├─ Normalize prices                    │
│     ├─ Calculate metrics (CTR, CR)         │
│     └─ Prepare context for LLM             │
│                                            │
│  3. LLM Analysis (GPT-4)                   │
│     ├─ Market analysis                     │
│     ├─ Competitive positioning             │
│     └─ Recommendation generation           │
│                                            │
│  4. Post-processing                        │
│     ├─ Validate recommendations            │
│     ├─ Calculate confidence scores         │
│     └─ Prioritize by impact/effort         │
│                                            │
│  5. Cache & Store                          │
│     ├─ Redis (short-term cache)            │
│     └─ PostgreSQL (persistent storage)     │
│                                            │
└────────────────────────────────────────────┘
```

### Przykład: Market Analysis Service

```typescript
// modules/ai/analysis.service.ts
import { Injectable } from '@nestjs/common'
import { OpenAI } from 'openai'
import { RedisService } from '../redis/redis.service'

@Injectable()
export class AnalysisService {
  private openai: OpenAI

  constructor(
    private redis: RedisService,
    private promptService: PromptService,
  ) {
    this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
  }

  async analyzeMarket(product: Product): Promise<MarketAnalysis> {
    // 1. Check cache
    const cacheKey = `market-analysis:${product.sku}:${dateKey}`
    const cached = await this.redis.get(cacheKey)
    if (cached) return JSON.parse(cached)

    // 2. Gather market data
    const marketData = await this.gatherMarketData(product)

    // 3. Prepare prompt
    const prompt = await this.promptService.render('market-analysis', {
      product,
      marketData,
    })

    // 4. Call GPT-4
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [{ role: 'user', content: prompt }],
      response_format: { type: 'json_object' },
      temperature: 0.3,  // Lower for consistency
    })

    // 5. Parse and validate
    const analysis = marketAnalysisSchema.parse(
      JSON.parse(response.choices[0].message.content)
    )

    // 6. Cache result (1 hour)
    await this.redis.setex(cacheKey, 3600, JSON.stringify(analysis))

    return analysis
  }
}
```

### Prompt Template System

```typescript
// modules/ai/prompts/market-analysis.ts
export const marketAnalysisPrompt = `
You are an e-commerce pricing expert. Analyze the following product and market data.

## Product
- SKU: {{product.sku}}
- Name: {{product.name}}
- Current Price: {{product.price}} {{currency}}
- Stock: {{product.stock}}
- Days in inventory: {{product.ageDays}}
- CTR: {{product.ctr}}%
- CR: {{product.cr}}%

## Market Data
{{#each competitors}}
- {{name}}: {{price}} {{../currency}}
{{/each}}

## Task
Provide a market analysis in JSON format:
{
  "competitivePosition": "string (low/medium/high)",
  "priceRecommendation": {
    "suggestedPrice": number,
    "reasoning": "string",
    "expectedImpact": {
      "ctrDelta": number,
      "crDelta": number
    }
  },
  "otherRecommendations": [
    {
      "type": "string",
      "action": "string",
      "priority": "string (low/medium/high)",
      "confidence": number (0-1)
    }
  ]
}

Be specific and data-driven. Focus on actionable insights.
`
```

---

## Integracje Zewnętrzne

### Platform Connector Interface

```typescript
// modules/connectors/platform-connector.interface.ts
export interface PlatformConnector {
  // Authentication
  connect(credentials: ConnectorCredentials): Promise<void>
  disconnect(): Promise<void>

  // Product operations
  getProducts(filters?: ProductFilters): Promise<Product[]>
  getProduct(externalId: string): Promise<Product>
  createProduct(data: CreateProductDto): Promise<Product>
  updateProduct(externalId: string, data: UpdateProductDto): Promise<Product>
  deleteProduct(externalId: string): Promise<void>

  // Sync operations
  syncAll(): Promise<SyncResult>
  syncProduct(sku: string): Promise<SyncResult>

  // Webhook handlers
  handleWebhook(payload: unknown): Promise<void>
}
```

### Shopify Connector Przykład

```typescript
// modules/connectors/shopify/shopify.connector.ts
import { shopifyApi } from '@shopify/shopify-api'

@Injectable()
export class ShopifyConnector implements PlatformConnector {
  private client: Shopify

  async connect(credentials: ShopifyCredentials) {
    this.client = shopifyApi({
      apiKey: credentials.apiKey,
      apiSecretKey: credentials.apiSecret,
      scopes: ['read_products', 'write_products'],
      hostName: credentials.shop,
    })
  }

  async getProducts(filters?: ProductFilters): Promise<Product[]> {
    const response = await this.client.product.list({ limit: 250 })
    return response.data.map(p => this.transformProduct(p))
  }

  async updateProduct(externalId: string, data: UpdateProductDto) {
    const response = await this.client.product.update(externalId, {
      title: data.title,
      variants: [{ price: data.price.toString() }],
    })
    return this.transformProduct(response.data)
  }

  async handleWebhook(payload: ShopifyWebhook) {
    switch (payload.topic) {
      case 'products/update':
        await this.handleProductUpdate(payload.data)
        break
      // ... other events
    }
  }

  private transformProduct(shopifyProduct: any): Product {
    // Transform Shopify format to our internal format
    return {
      sku: shopifyProduct.variants[0].sku,
      name: shopifyProduct.title,
      price: parseFloat(shopifyProduct.variants[0].price),
      // ...
    }
  }
}
```

---

## Przepływ Danych

### User Story: Applying Recommendation

```
User clicks "Apply" on recommendation
          │
          ▼
Frontend sends POST /api/v1/recommendations/:id/apply
          │
          ▼
Backend: RecommendationsController.apply()
          │
          ▼
RecommendationsService validates recommendation
          │
          ▼
ActionExecutorService.execute()
          │
          ├─► Get product and recommendation details
          │
          ├─► For each connected channel:
          │       │
          │       ├─► Get connector (Shopify/WooCommerce/etc)
          │       │
          │       ├─► connector.updateProduct(externalId, changes)
          │       │       │
          │       │       └─► External API call
          │       │
          │       └─► Log action for rollback
          │
          ├─► Update recommendation status to "APPLIED"
          │
          └─► Return success response
          │
          ▼
Frontend: Optimistically update UI, show success toast
          │
          ▼
TanStack Query invalidates cache, refetches recommendations
```

### Background Job: Full Sync

```
Scheduler triggers sync job (e.g., every 6 hours)
          │
          ▼
SyncService creates job in BullMQ queue
          │
          ▼
SyncProcessor picks up job
          │
          ├─► Get channel credentials from DB
          │
          ├─► connector.syncAll()
          │       │
          │       ├─► Fetch all products from platform API
          │       │
          │       ├─► For each product:
          │       │       │
          │       │       ├─► Check if exists in DB (by SKU)
          │       │       │
          │       │       ├─► If exists: update
          │       │       │   If not: create
          │       │       │
          │       │       └─► Update ProductChannel record
          │       │
          │       └─► Return sync results
          │
          ├─► Update SyncJob status
          │
          └─► Trigger AI analysis for new/updated products (optional)
```

---

## Bezpieczeństwo

### Authentication Flow

```
User logs in with email/password
          │
          ▼
POST /api/v1/auth/login
          │
          ▼
Validate credentials
          │
          ▼
Generate JWT token (expires in 7 days)
          │
          ▼
Return { token, user }
          │
          ▼
Frontend stores token in localStorage
          │
          ▼
All subsequent requests include:
Authorization: Bearer <token>
          │
          ▼
Backend verifies JWT on each request
```

### Security Best Practices

1. **Secrets Management**
   - All API keys in environment variables
   - Never commit `.env` files
   - Rotate keys regularly

2. **Input Validation**
   ```typescript
   // Use Zod schemas
   const createProductSchema = z.object({
     sku: z.string().min(1).max(64).regex(/^[A-Z0-9-_]+$/),
     price: z.number().positive(),
     stock: z.number().int().nonnegative(),
   })
   ```

3. **Rate Limiting**
   ```typescript
   @UseGuards(ThrottlerGuard)
   @Throttle(10, 60)  // 10 requests per 60 seconds
   @Post('recommendations/:id/apply')
   ```

4. **CORS Configuration**
   ```typescript
   app.enableCors({
     origin: process.env.FRONTEND_URL,
     credentials: true,
   })
   ```

5. **Webhook Verification**
   ```typescript
   // Verify HMAC signature
   const hmac = crypto.createHmac('sha256', secret)
   hmac.update(rawBody)
   const digest = hmac.digest('hex')

   if (digest !== providedSignature) {
     throw new UnauthorizedException('Invalid webhook signature')
   }
   ```

---

## Skalowalność

### Horizontal Scaling Strategy

```
┌──────────────────────────────────────┐
│     Load Balancer (Nginx/CloudFlare)│
└────────────┬─────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│ API  │ │ API  │ │ API  │  (Multiple instances)
│ Node │ │ Node │ │ Node │
└───┬──┘ └───┬──┘ └───┬──┘
    │        │        │
    └────────┼────────┘
             │
    ┌────────▼────────┐
    │  Shared State   │
    │  PostgreSQL +   │
    │     Redis       │
    └─────────────────┘
```

### Caching Strategy

**1. Redis Layers**:
- **L1**: Hot data (API responses) - TTL 30s
- **L2**: Analysis results - TTL 1 hour
- **L3**: Market data - TTL 4 hours

**2. Query Optimization**:
```typescript
// Use select to fetch only needed fields
const products = await prisma.product.findMany({
  select: {
    sku: true,
    name: true,
    price: true,
  },
  where: { rotation: 'LOW' },
  take: 20,
})
```

**3. Background Processing**:
- Use BullMQ for long-running tasks
- Implement retry logic with exponential backoff
- Monitor queue depth

### Performance Targets

| Metric | Target |
|--------|--------|
| API response time (p95) | < 500ms |
| Frontend load time | < 2s |
| AI recommendation generation | < 10s |
| Full sync (1000 products) | < 5 min |
| Uptime | > 99.5% |

---

## Monitoring & Observability

### Logging

```typescript
// Structured logging with Winston
logger.info('Recommendation applied', {
  recommendationId: rec.id,
  productSku: rec.product.sku,
  type: rec.type,
  userId: user.id,
  timestamp: new Date().toISOString(),
})
```

### Metrics to Track

- Request rate (req/min)
- Error rate (%)
- Average response time
- Database query time
- OpenAI API costs
- Sync job success rate

### Alerting Rules

- Error rate > 5% for 5 minutes → Alert
- API response time p95 > 1s → Warning
- Queue depth > 1000 → Alert
- Sync job failure → Notify

---

## Deployment Architecture

### Production Stack

```
Frontend:
- Hosting: Vercel / CloudFlare Pages
- CDN: Built-in
- Domain: sales-optimizer.com

Backend:
- Hosting: Railway.app / Render.com
- Containers: Docker
- Orchestration: Built-in

Database:
- PostgreSQL: Supabase (managed)
- Redis: Upstash (serverless)

Monitoring:
- Errors: Sentry
- Logs: LogTail / DataDog
- Uptime: UptimeRobot
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cd frontend && npm ci
      - run: npm run build
      - run: npm run test
      - uses: vercel/action@v2  # Auto-deploy

  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cd backend && npm ci
      - run: npm run build
      - run: npm test
      - run: npx prisma migrate deploy
      - uses: railway/action@v2  # Auto-deploy
```

---

**Last Updated**: 2025-11-08
**Maintainers**: All team members
