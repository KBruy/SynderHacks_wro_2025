# Sales Optimizer Platform

> AI-powered e-commerce management system for small businesses
>
> **SynderHacks Wrocław 2025** 🚀

---

## What is Sales Optimizer?

Sales Optimizer is an intelligent platform that helps small e-commerce businesses:

- 🔄 **Synchronize** products across multiple platforms (Shopify, WooCommerce, eBay)
- 🤖 **Analyze** market trends and competition using GPT-4
- 💡 **Generate** smart recommendations (pricing, promotions, bundles)
- ⚡ **Automate** offer creation and posting
- 📊 **Track** performance with analytics dashboard

---

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite
- shadcn/ui + Tailwind CSS
- TanStack Query
- React Router
- Recharts

### Backend
- Node.js + TypeScript
- NestJS
- Prisma ORM
- PostgreSQL
- Redis (BullMQ)
- OpenAI GPT-4

### Infrastructure
- Vercel (Frontend)
- Railway/Render (Backend)
- Supabase (Database)
- Upstash (Redis)

---

## Quick Start

### Prerequisites

- Node.js 18+
- PostgreSQL 14+ (or Supabase account)
- Redis (or Upstash account)
- OpenAI API key

### Installation

**1. Clone repository**

```bash
git clone https://github.com/CZIWELLO/KNAlgo.git
cd KNAlgo/SynderHacks_wro_2025
```

**2. Setup Frontend**

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your API URL
npm run dev
```

Frontend runs on `http://localhost:5173`

**3. Setup Backend**

```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your database URL, Redis URL, and API keys
npx prisma migrate dev
npm run dev
```

Backend runs on `http://localhost:3000`

**For detailed setup instructions, see** [docs/SETUP.md](docs/SETUP.md)

---

## Documentation

### For New Team Members

Start here:
1. **[CLAUDE.md](CLAUDE.md)** - Guide for working with Claude Code (AI assistant)
2. **[docs/SETUP.md](docs/SETUP.md)** - Complete development setup
3. **[TEAM_WORKFLOW.md](TEAM_WORKFLOW.md)** - Collaboration guidelines
4. **[docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md)** - Git branching strategy

### Architecture & API

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
- **[Backend/backend_api_spec.md](Backend/backend_api_spec.md)** - API contracts
- **[Frontend/struct.md](Frontend/struct.md)** - Frontend structure

---

## Team Structure

| Role | Focus | Primary Directories |
|------|-------|---------------------|
| **Person 1** | Frontend | `/frontend` |
| **Person 2** | AI/Analysis | `/backend/src/ai` |
| **Person 3** | Backend/Sync | `/backend/src/api`, `/backend/src/connectors` |

---

## Project Structure

```
SynderHacks_wro_2025/
├── CLAUDE.md                    # AI assistant configuration
├── TEAM_WORKFLOW.md             # Team collaboration guide
├── README.md                    # This file
├── docs/                        # Documentation
│   ├── SETUP.md                # Development setup guide
│   ├── ARCHITECTURE.md         # System architecture
│   └── GIT_WORKFLOW.md         # Git workflow guide
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── routes/             # Page components
│   │   ├── lib/                # Utilities, API client
│   │   ├── hooks/              # Custom React hooks
│   │   └── types/              # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── backend/                     # Node.js backend
│   ├── src/
│   │   ├── api/                # REST API controllers
│   │   ├── connectors/         # Platform integrations
│   │   ├── ai/                 # AI/ML services
│   │   ├── sync/               # Synchronization logic
│   │   └── queue/              # Job queue processors
│   ├── prisma/
│   │   └── schema.prisma       # Database schema
│   └── package.json
└── Backend/                     # Legacy specs (will be moved)
    └── backend_api_spec.md
```

---

## Key Features

### 1. Multi-Platform Sync
- Connects to Shopify, WooCommerce, eBay
- Two-way synchronization
- Webhook support for real-time updates
- Conflict resolution

### 2. AI-Powered Recommendations
- Market analysis using GPT-4
- Price optimization
- Promotion suggestions
- Bundle recommendations
- Title/description optimization

### 3. Action Executor
- Apply recommendations across all platforms
- Rollback capability
- Audit trail
- Batch operations

### 4. Analytics Dashboard
- Performance metrics (CTR, CR, revenue)
- Product insights
- Recommendation effectiveness tracking
- Custom reports

---

## Git Workflow

### Branching Strategy

```
main (protected)
├── frontend/*      # Frontend features (Person 1)
├── ai/*           # AI/ML features (Person 2)
├── backend/*      # Backend features (Person 3)
└── hotfix/*       # Critical fixes
```

### Commit Convention

```
<type>(<scope>): <description>

Examples:
feat(frontend): add recommendation card component
fix(ai): correct price calculation
docs(api): update recommendations endpoint
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

**Scopes**: `frontend`, `backend`, `ai`, `sync`, `api`, `db`

See [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) for details.

---

## API Endpoints

Base URL: `http://localhost:3000/api/v1`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommendations` | List AI recommendations |
| POST | `/recommendations/:id/apply` | Apply recommendation |
| GET | `/products` | List products with filters |
| GET | `/products/:sku` | Get product details |
| GET | `/channels` | Platform integration status |
| POST | `/reports` | Generate report |
| GET | `/health` | Health check |

For full API spec, see [Backend/backend_api_spec.md](Backend/backend_api_spec.md)

---

## Development

### Frontend

```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run format       # Format with Prettier
```

### Backend

```bash
cd backend
npm run dev          # Start dev server
npm run build        # Build for production
npm run test         # Run tests
npx prisma studio    # Open database GUI
```

---

## Environment Variables

### Frontend (.env)

```env
VITE_API_URL=http://localhost:3000/api/v1
VITE_ENV=development
```

### Backend (.env)

```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/sales_optimizer
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-your-key-here
JWT_SECRET=your-secret-key
```

See `.env.example` files for complete list.

---

## Testing

### Frontend Tests

```bash
cd frontend
npm run test         # Run unit tests (Vitest)
npm run test:ui      # Run tests with UI
```

### Backend Tests

```bash
cd backend
npm run test         # Run unit tests (Jest)
npm run test:e2e     # Run integration tests
```

---

## Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Connect to Vercel and deploy
```

### Backend (Railway)

```bash
cd backend
npm run build
# Push to Railway via Git
```

See deployment docs for details.

---

## Contributing

### For Team Members

1. Read [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md)
2. Create feature branch: `git checkout -b <role>/<feature-name>`
3. Make changes, commit regularly
4. Create PR, request review
5. After approval, squash merge to main

### Code Quality

- TypeScript strict mode
- ESLint + Prettier
- 70%+ test coverage for critical paths
- No `any` types, no secrets in code

---

## Troubleshooting

### Common Issues

**Frontend can't connect to backend**
- Ensure backend is running: `curl http://localhost:3000/api/v1/health`
- Check `VITE_API_URL` in frontend `.env`
- Check CORS settings in backend

**Database errors**
- Run migrations: `npx prisma migrate dev`
- Check DATABASE_URL format
- Verify PostgreSQL is running

**OpenAI API errors**
- Verify OPENAI_API_KEY in `.env`
- Check usage limits in OpenAI dashboard
- Implement retry logic

See [docs/SETUP.md#troubleshooting](docs/SETUP.md#troubleshooting) for more.

---

## Resources

### Documentation
- [React](https://react.dev)
- [NestJS](https://docs.nestjs.com)
- [Prisma](https://www.prisma.io/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [shadcn/ui](https://ui.shadcn.com)

### External APIs
- [Shopify API](https://shopify.dev/docs/api)
- [WooCommerce API](https://woocommerce.github.io/woocommerce-rest-api-docs/)
- [eBay API](https://developer.ebay.com)

---

## License

MIT

---

## Team

**SynderHacks Wrocław 2025**

- Frontend Developer (Person 1)
- AI/Analysis Developer (Person 2)
- Backend/Sync Developer (Person 3)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/CZIWELLO/KNAlgo/issues)
- **Questions**: Create issue with `question` label
- **Team Chat**: #dev-general channel

---

## Roadmap

### Phase 1: MVP (Hackathon)
- [x] Project setup and documentation
- [ ] Frontend: Recommendation Hub, Product List
- [ ] Backend: API endpoints, database schema
- [ ] AI: Basic market analysis with GPT-4
- [ ] Sync: Shopify connector MVP
- [ ] Integration: Connect all components

### Phase 2: Post-Hackathon
- [ ] WooCommerce + eBay connectors
- [ ] Advanced AI recommendations (bundles, A/B testing)
- [ ] Reports and exports
- [ ] User authentication and multi-tenant
- [ ] Production deployment

---

**Built with ❤️ for small businesses**

**Happy coding!** 🚀
