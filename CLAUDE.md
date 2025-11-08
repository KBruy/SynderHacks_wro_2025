# CLAUDE.md

This file provides guidance to Claude Code when working with this repository. It ensures consistent AI-assisted development across all team members.

---

## Project Overview

**Name**: Sales Optimizer (SynderHacks Wrocław 2025)

**Goal**: AI-powered platform for small business e-commerce management with:
- Multi-platform synchronization (Shopify, WooCommerce, eBay)
- AI-driven market analysis and recommendations (pricing, promotions, bundles)
- Automated offer creation and posting
- Analytics and insights dashboard

**Tech Stack**:
- **Frontend**: React + TypeScript, shadcn/ui, TanStack Query, Recharts
- **Backend**: Node.js + TypeScript, NestJS/Express, Prisma ORM
- **Database**: PostgreSQL + Redis
- **AI/ML**: OpenAI GPT-4, LangChain
- **Queue**: BullMQ (Redis-based)
- **Deployment**: Vercel (frontend), Railway/Render (backend), Supabase (DB)

---

## Team Structure & Roles

### Person 1: Frontend Developer
**Branch**: `frontend/*`
**Focus**: React UI, components, state management, API integration
**Primary directories**: `/frontend`, `/frontend/src`

### Person 2: AI/Analysis Developer
**Branch**: `ai/*`
**Focus**: GPT-4 integration, recommendation engine, market analysis, LangChain workflows
**Primary directories**: `/backend/src/ai`, `/backend/src/services/analysis`

### Person 3: Backend/Sync Developer
**Branch**: `backend/*`
**Focus**: API endpoints, platform connectors (Shopify/WooCommerce/eBay), synchronization logic
**Primary directories**: `/backend/src/api`, `/backend/src/connectors`, `/backend/src/sync`

---

## Repository Structure

```
SynderHacks_wro_2025/
├── CLAUDE.md                    # This file
├── TEAM_WORKFLOW.md             # Collaboration guidelines
├── README.md                    # Project overview
├── docs/                        # Documentation
│   ├── API_SPEC.md             # API contracts (source of truth)
│   ├── SETUP.md                # Development setup
│   └── ARCHITECTURE.md         # System architecture
├── frontend/                    # React application
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── components/         # Reusable UI components
│       ├── routes/             # Page components
│       ├── lib/                # Utilities, API client
│       ├── hooks/              # Custom React hooks
│       └── types/              # TypeScript types (sync with backend)
├── backend/                     # Node.js backend
│   ├── package.json
│   ├── tsconfig.json
│   ├── prisma/
│   │   └── schema.prisma       # Database schema
│   └── src/
│       ├── api/                # REST API controllers
│       ├── connectors/         # Platform integrations
│       │   ├── shopify/
│       │   ├── woocommerce/
│       │   └── ebay/
│       ├── ai/                 # AI/ML services
│       │   ├── analysis.service.ts
│       │   ├── recommendations.service.ts
│       │   └── prompts/        # GPT-4 prompt templates
│       ├── sync/               # Synchronization logic
│       ├── queue/              # Job queue processors
│       ├── types/              # Shared TypeScript types
│       └── main.ts             # Entry point
└── .github/
    └── workflows/              # CI/CD pipelines
```

---

## Git Workflow & Branching Strategy

### Branch Naming Convention

```
main                          # Production-ready code (protected)
├── frontend/feature-name     # Frontend features
├── ai/feature-name          # AI/analysis features
├── backend/feature-name     # Backend/sync features
└── hotfix/bug-description   # Critical fixes
```

**Examples**:
- `frontend/recommendation-cards`
- `ai/market-analysis-engine`
- `backend/shopify-connector`
- `hotfix/auth-token-expiry`

### Commit Message Convention

```
<type>(<scope>): <description>

[optional body]
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
**Scopes**: `frontend`, `backend`, `ai`, `sync`, `api`, `db`

**Examples**:
```
feat(frontend): add recommendation card component
fix(ai): correct price analysis calculation
feat(backend): implement Shopify OAuth flow
docs(api): update recommendations endpoint spec
```

### Pull Request Workflow

1. Create feature branch from `main`
2. Work on your feature, commit regularly
3. Push to remote and create PR
4. Request review from at least 1 team member
5. After approval, squash merge to `main`
6. Delete feature branch after merge

---

## Claude Code Instructions

### General Guidelines (All Team Members)

When assisting with this project, Claude should:

1. **Always check current role context**: Read the branch name or ask which component the user is working on
2. **Maintain type safety**: All code must be TypeScript with proper types
3. **Follow API contracts**: Reference `/docs/API_SPEC.md` (or `Backend/backend_api_spec.md`) for endpoints
4. **Use existing patterns**: Check similar code before creating new patterns
5. **Write tests**: Include unit tests for new features
6. **Document decisions**: Add comments for complex logic
7. **Security first**: Never expose secrets, validate all inputs, sanitize outputs

### Role-Specific Instructions

#### When Working with Frontend Developer (Person 1)

**Claude should**:
- Use shadcn/ui components exclusively (never create custom button/input from scratch)
- Follow the design system in `/Frontend/struct.md`
- Use TanStack Query for all API calls (no raw fetch in components)
- Implement optimistic updates for user actions
- Add proper loading states (Skeleton components)
- Include error boundaries
- Make components responsive (mobile-first)
- Use Zod for form validation
- Reference `/frontend/src/types` for shared types

**Example interaction**:
```
User: "Add a recommendation card component"
Claude:
1. Check existing cards in /frontend/src/components
2. Use Card, Badge, Button from shadcn/ui
3. Import Recommendation type from /frontend/src/types
4. Add optimistic update with TanStack Query mutation
5. Include loading and error states
```

#### When Working with AI/Analysis Developer (Person 2)

**Claude should**:
- Use LangChain for complex AI workflows
- Store all prompts in `/backend/src/ai/prompts/` as templates
- Implement proper error handling for OpenAI API calls (rate limits, timeouts)
- Add confidence scores to all recommendations
- Log all AI decisions for debugging
- Use structured outputs (OpenAI Functions/JSON mode)
- Cache analysis results in Redis
- Implement cost tracking for API usage

**Example interaction**:
```
User: "Create market analysis for product pricing"
Claude:
1. Create prompt template in /backend/src/ai/prompts/market-analysis.ts
2. Use LangChain with GPT-4
3. Structure output with Zod schema
4. Cache results in Redis (key: market-analysis:{sku}:{date})
5. Return confidence score and reasoning
6. Log token usage
```

**Prompt Engineering Guidelines**:
- Always provide context (product data, market data)
- Request structured JSON output
- Include few-shot examples
- Add confidence/reasoning fields
- Specify output format clearly

#### When Working with Backend/Sync Developer (Person 3)

**Claude should**:
- Follow REST API spec in `/Backend/backend_api_spec.md`
- Use Prisma for all database operations
- Implement proper authentication (JWT)
- Add rate limiting to all endpoints
- Use BullMQ for async operations (syncs, reports)
- Implement idempotency for sync operations
- Add proper error handling with error codes
- Use webhooks where available (Shopify, WooCommerce)
- Implement retry logic with exponential backoff
- Add health check endpoints

**Example interaction**:
```
User: "Implement Shopify product sync"
Claude:
1. Create connector in /backend/src/connectors/shopify/
2. Use @shopify/shopify-api SDK
3. Implement OAuth flow
4. Add webhook handlers
5. Create BullMQ job for bulk sync
6. Store sync status in DB (Prisma)
7. Emit events for real-time updates
8. Add error recovery and retry logic
```

**Platform Connector Pattern**:
```typescript
interface PlatformConnector {
  connect(credentials: OAuth): Promise<void>
  sync(): Promise<SyncResult>
  getProducts(filters?: ProductFilters): Promise<Product[]>
  updateProduct(sku: string, updates: ProductUpdate): Promise<void>
  webhookHandler(payload: unknown): Promise<void>
}
```

---

## API Contracts (Source of Truth)

All team members must reference `/Backend/backend_api_spec.md` for:
- Endpoint URLs and methods
- Request/response schemas
- Error formats
- Authentication requirements
- Pagination format

**Key endpoints**:
- `GET /api/v1/recommendations` - List AI recommendations
- `GET /api/v1/products` - List products (with filters)
- `POST /api/v1/recommendations/{id}/apply` - Apply recommendation
- `GET /api/v1/channels` - Platform integration status

---

## Shared Types & Contracts

Types must be synchronized between frontend and backend:

**Process**:
1. Define types in `/backend/src/types/` (source of truth)
2. Export as package or copy to `/frontend/src/types/`
3. Never modify frontend types without updating backend

**Example**: `Recommendation` type must match on both sides.

---

## Development Setup (Quick Start)

### Prerequisites
- Node.js 18+
- PostgreSQL 14+ (or Supabase account)
- Redis (or Upstash account)
- OpenAI API key

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env  # Add API_URL
npm run dev           # Starts on localhost:5173
```

### Backend Setup
```bash
cd backend
npm install
cp .env.example .env  # Add DATABASE_URL, REDIS_URL, OPENAI_API_KEY
npx prisma migrate dev
npm run dev           # Starts on localhost:3000
```

See `/docs/SETUP.md` for detailed instructions.

---

## Testing Strategy

### Frontend Tests
- **Unit**: Vitest for components and hooks
- **Integration**: React Testing Library
- **E2E**: Playwright (optional for hackathon)

### Backend Tests
- **Unit**: Jest for services and utilities
- **Integration**: Supertest for API endpoints
- **E2E**: Test full sync workflows

**Coverage target**: 70%+ for critical paths

---

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:3000/api/v1
VITE_ENV=development
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/sales_optimizer
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret-key

# Platform API keys
SHOPIFY_CLIENT_ID=...
SHOPIFY_CLIENT_SECRET=...
WOOCOMMERCE_CONSUMER_KEY=...
WOOCOMMERCE_CONSUMER_SECRET=...
```

**Never commit `.env` files!**

---

## Code Quality & Standards

### TypeScript
- Strict mode enabled
- No `any` types (use `unknown` if needed)
- Prefer interfaces over types for object shapes
- Use enums for constants

### Code Style
- **Formatter**: Prettier (auto-format on save)
- **Linter**: ESLint (must pass before commit)
- **Line length**: 100 characters max
- **Indentation**: 2 spaces

### Naming Conventions
- **Components**: PascalCase (`RecommendationCard.tsx`)
- **Functions**: camelCase (`analyzeMarket()`)
- **Constants**: UPPER_SNAKE_CASE (`API_VERSION`)
- **Files**: kebab-case for utilities (`market-analysis.service.ts`)

---

## Security Best Practices

1. **Never expose secrets**: Use environment variables
2. **Validate all inputs**: Use Zod schemas
3. **Sanitize outputs**: Prevent XSS
4. **Use parameterized queries**: Prisma handles this
5. **Implement rate limiting**: Protect API endpoints
6. **HTTPS only**: In production
7. **Secure webhooks**: Verify signatures (HMAC)

---

## Common Patterns

### Frontend: Fetching Data with TanStack Query
```typescript
function useRecommendations() {
  return useQuery({
    queryKey: ['recommendations'],
    queryFn: () => api.get<Recommendation[]>('/recommendations'),
    staleTime: 30_000,
  })
}
```

### Backend: Creating API Endpoint
```typescript
@Get('/recommendations')
async getRecommendations(@Query() query: RecommendationsQueryDto) {
  const items = await this.recommendationsService.findAll(query)
  return { items, meta: { page: 1, total: items.length } }
}
```

### AI: GPT-4 Analysis
```typescript
async analyzeProduct(product: Product): Promise<Analysis> {
  const prompt = await this.promptService.render('market-analysis', { product })
  const response = await this.openai.chat.completions.create({
    model: 'gpt-4-turbo',
    messages: [{ role: 'user', content: prompt }],
    response_format: { type: 'json_object' },
  })
  return analysisSchema.parse(JSON.parse(response.choices[0].message.content))
}
```

---

## Troubleshooting

### Common Issues

**Frontend can't connect to backend**:
- Check `VITE_API_URL` in `.env`
- Ensure backend is running on correct port
- Check CORS settings in backend

**Database connection errors**:
- Verify `DATABASE_URL` format
- Run `npx prisma migrate dev`
- Check PostgreSQL is running

**OpenAI API errors**:
- Verify `OPENAI_API_KEY` is valid
- Check rate limits
- Implement retry logic with exponential backoff

**Sync fails silently**:
- Check job queue (BullMQ UI or Redis)
- Review error logs
- Verify platform credentials

---

## Resources & Documentation

- [Backend API Spec](Backend/backend_api_spec.md)
- [Frontend Structure](Frontend/struct.md)
- [Shopify API Docs](https://shopify.dev/docs/api)
- [WooCommerce API](https://woocommerce.github.io/woocommerce-rest-api-docs/)
- [OpenAI API](https://platform.openai.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [TanStack Query](https://tanstack.com/query/latest)

---

## Communication & Sync

- **Daily sync**: 15 min standup (progress, blockers)
- **Slack/Discord**: Real-time communication
- **PR reviews**: Within 4 hours
- **Merge conflicts**: Resolve immediately, communicate

---

## When to Ask for Help

Claude should ask the user for clarification when:
1. **Uncertain about role context**: Which component are you working on?
2. **Multiple valid approaches**: Should we use approach A or B?
3. **Breaking changes needed**: This requires changing the API contract
4. **Missing information**: I need the platform credentials format
5. **Architecture decisions**: Should this be a separate service?

---

**Last Updated**: 2025-11-08
**Maintainers**: All team members
**Next Review**: After hackathon / before production
