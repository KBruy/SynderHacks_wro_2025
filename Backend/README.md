# Sales Optimizer Backend

> Node.js + NestJS + Prisma + PostgreSQL

## Quick Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your credentials:
# - DATABASE_URL (Supabase or local PostgreSQL)
# - REDIS_URL (Upstash or local Redis)
# - OPENAI_API_KEY (from OpenAI)
```

### 3. Setup Database

```bash
# Generate Prisma Client
npm run prisma:generate

# Run migrations
npm run prisma:migrate

# (Optional) Seed with test data
npm run prisma:seed
```

### 4. Start Development Server

```bash
npm run dev
```

Server runs on `http://localhost:3000`

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm test` | Run tests |
| `npm run prisma:studio` | Open Prisma Studio (DB GUI) |
| `npm run prisma:migrate` | Run database migrations |
| `npm run prisma:generate` | Generate Prisma Client |

## API Endpoints

Base URL: `http://localhost:3000/api/v1`

### Health Check
- `GET /health` - Server health status

### Products
- `GET /products` - List products (with pagination, filters)
- `GET /products/:sku` - Get product details

### Recommendations
- `GET /recommendations` - List recommendations (with pagination, filters)
- `GET /recommendations/:id` - Get recommendation details
- `POST /recommendations/:id/apply` - Apply recommendation
- `POST /recommendations/:id/reject` - Reject recommendation

See [Backend/backend_api_spec.md](../Backend/backend_api_spec.md) for full API documentation.

## Project Structure

```
backend/
├── src/
│   ├── api/                    # API controllers
│   │   ├── products/          # Products module
│   │   └── recommendations/   # Recommendations module
│   ├── common/                # Shared utilities
│   │   └── prisma.service.ts # Prisma service
│   ├── types/                 # Shared TypeScript types
│   ├── app.module.ts          # Root module
│   └── main.ts                # Entry point
├── prisma/
│   ├── schema.prisma          # Database schema
│   ├── migrations/            # Migration history
│   └── seed.ts                # Test data
├── package.json
└── tsconfig.json
```

## Database Schema

See `prisma/schema.prisma` for full schema.

**Key models**:
- `Product` - Product information
- `Channel` - Platform integrations
- `Recommendation` - AI recommendations
- `SyncJob` - Sync job history

## Environment Variables

See `.env.example` for all available variables.

**Required**:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `OPENAI_API_KEY` - OpenAI API key
- `JWT_SECRET` - JWT signing secret

## Development

### View Database

```bash
npm run prisma:studio
```

Opens GUI at `http://localhost:5555`

### Create Migration

```bash
npx prisma migrate dev --name your_migration_name
```

### Reset Database

```bash
npx prisma migrate reset
```

**Warning**: This will delete all data!

## Testing

```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Coverage
npm run test:cov
```

## Troubleshooting

### "Database connection failed"

Check:
1. `DATABASE_URL` is correct in `.env`
2. PostgreSQL is running (if local)
3. Database exists

### "Redis connection failed"

Check:
1. `REDIS_URL` is correct in `.env`
2. Redis is running (if local)

### "Prisma Client not generated"

Run:
```bash
npm run prisma:generate
```

## Next Steps

### For Backend Developer (Person 3)

1. Implement Shopify connector (`src/connectors/shopify/`)
2. Add sync service (`src/sync/`)
3. Add authentication (JWT)

### For AI Developer (Person 2)

1. Implement AI service (`src/ai/`)
2. Add market analysis with GPT-4
3. Add recommendation generation

## Resources

- [NestJS Docs](https://docs.nestjs.com)
- [Prisma Docs](https://www.prisma.io/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

**Questions?** See [docs/SETUP.md](../docs/SETUP.md) or ask in team chat
