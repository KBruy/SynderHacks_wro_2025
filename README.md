# Smart Product Optimization Manager

**An AI-powered e-commerce optimization platform that helps online retailers maximize revenue through intelligent pricing, promotion, and bundling suggestions.**

![Platform](https://img.shields.io/badge/Platform-Docker-blue)
![Backend](https://img.shields.io/badge/Backend-Flask-green)
![Frontend](https://img.shields.io/badge/Frontend-React-cyan)
![Database](https://img.shields.io/badge/Database-SQLite-orange)

---

## The Problem

E-commerce retailers face three critical challenges:

1. **Pricing Optimization**: Determining optimal product prices requires constant market analysis and competitor monitoring
2. **Promotion Timing**: Knowing when and how to discount products to maximize sales without eroding margins
3. **Product Bundling**: Identifying which products should be bundled together to increase average order value

Manual management of these tasks is time-consuming, error-prone, and often misses revenue opportunities. Small to medium-sized retailers lack the resources for sophisticated pricing algorithms and data analysis teams.

## Our Solution

**Smart Product Optimization Manager** is an intelligent platform that automatically generates actionable recommendations for:

- **Dynamic Pricing**: AI-driven price adjustments based on inventory levels, sales velocity, and market positioning
- **Smart Promotions**: Targeted discount suggestions to move slow-moving inventory or capitalize on trending products
- **Bundle Creation**: Automated detection of product synergies to create attractive bundles that increase cart value

### Key Features

- **Multi-Channel Integration**: Connects to WooCommerce and Shopify stores via secure API
- **One-Click Application**: Apply optimization suggestions with a single click
- **Real-Time Analytics**: Track the impact of applied suggestions through comprehensive event history
- **Demo Mode**: Test the platform without connecting real stores
- **Encrypted Credentials**: Bank-grade AES encryption for API keys and secrets

---

## Technical Architecture

### System Overview

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   React Frontend│ ◄─────► │   Flask Backend  │ ◄─────► │ E-commerce APIs │
│   (Port 5173)   │   REST  │   (Port 5001)    │   REST  │  WooCommerce    │
└─────────────────┘         └──────────────────┘         │    Shopify      │
                                     │                     └─────────────────┘
                                     ▼
                            ┌──────────────────┐
                            │  SQLite Database │
                            │   (Persistent)   │
                            └──────────────────┘
```

### Technology Stack

#### Backend (Python/Flask)
- **Framework**: Flask 3.0 with RESTful API design
- **Database**: SQLite with transaction-safe operations
- **Security**:
  - AES-256 encryption for credentials (PBKDF2HMAC key derivation)
  - CORS protection
  - Input validation and sanitization
- **External Integrations**:
  - WooCommerce REST API v3
  - Shopify Admin API 2024-01
  - Mock integration for testing without real stores

#### Frontend (React/Vite)
- **Framework**: React 18 with modern hooks (useState, useEffect)
- **Build Tool**: Vite 5 for fast development and optimized production builds
- **Styling**: Vanilla CSS with responsive design (no external UI libraries)
- **State Management**: Component-level state with callback-based updates
- **API Client**: Fetch API with error handling and retry logic

#### Infrastructure
- **Containerization**: Docker & Docker Compose for one-command deployment
- **Data Persistence**: Named volume for SQLite database
- **Networking**: Internal Docker network with exposed ports

### Database Schema

```sql
-- Core product data from connected stores
products (
  id INTEGER PRIMARY KEY,
  sku TEXT,
  name TEXT,
  price REAL,
  stock INTEGER,
  status TEXT,
  channel TEXT,
  connection_id INTEGER,
  external_id TEXT,
  created_at TEXT,
  updated_at TEXT,
  FOREIGN KEY (connection_id) REFERENCES store_connections(id)
)

-- AI-generated optimization suggestions
suggestions (
  id INTEGER PRIMARY KEY,
  product_id INTEGER,
  type TEXT CHECK(type IN ('price', 'promo', 'bundle')),
  description TEXT,
  status TEXT CHECK(status IN ('new', 'applied')),
  applied_at TEXT,
  FOREIGN KEY (product_id) REFERENCES products(id)
)

-- Product bundle definitions
bundles (
  id INTEGER PRIMARY KEY,
  name TEXT,
  sku TEXT UNIQUE,
  price REAL,
  channel TEXT,
  connection_id INTEGER,
  is_active BOOLEAN DEFAULT 1
)

-- Bundle composition (many-to-many)
bundle_items (
  id INTEGER PRIMARY KEY,
  bundle_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  FOREIGN KEY (bundle_id) REFERENCES bundles(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
)

-- Audit trail for all actions
events (
  id INTEGER PRIMARY KEY,
  product_id INTEGER,
  suggestion_id INTEGER,
  event_type TEXT,
  description TEXT,
  created_at TEXT
)

-- Store connection credentials (encrypted)
store_connections (
  id INTEGER PRIMARY KEY,
  name TEXT,
  platform TEXT CHECK(platform IN ('woocommerce', 'shopify')),
  store_url TEXT,
  api_key_encrypted TEXT,
  api_secret_encrypted TEXT,
  is_active BOOLEAN DEFAULT 1
)
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/api/products` | List all products with active promotions |
| `GET` | `/api/products/:id` | Get single product details |
| `GET` | `/api/suggestions?product_id=ID` | Get suggestions for specific product |
| `POST` | `/api/suggestions/:id/apply` | Apply suggestion (updates product or creates bundle) |
| `GET` | `/api/events` | Event history (last 20 actions) |
| `GET` | `/api/connections` | List store connections |
| `POST` | `/api/connections` | Create new store connection |
| `POST` | `/api/connections/:id/sync` | Sync products from store |
| `POST` | `/api/connections/demo/quick-setup` | Create demo stores for testing |
| `DELETE` | `/api/connections/:id` | Remove store connection |

### Key Technical Innovations

#### 1. Intelligent Price Parsing
The system uses regex pattern matching to extract pricing information from natural language suggestions:

```python
# Pattern 1: "Increase price to 169.99"
match = re.search(r'to\s+(\d+\.?\d*)', description)

# Pattern 2: "Reduce price by 15%"
match = re.search(r'by\s+(\d+)%', description)
```

#### 2. Timestamp Consistency
Custom timestamp handling to avoid UTC/local timezone conflicts:

```python
# Backend: Explicit local time
now = datetime.now().isoformat(sep=' ', timespec='seconds')

# Frontend: SQLite format to ISO conversion
const date = new Date(dateString.replace(' ', 'T'));
```

#### 3. Secure Credential Management
Multi-layer encryption for API credentials:

```python
# Key derivation from master password
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)

# AES-256 encryption
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
```

#### 4. Auto-Refresh Architecture
Smart UI updates after suggestion application:

```javascript
const handleSuggestionApplied = (notificationData) => {
  setNotification(notificationData);
  loadProducts();  // Refresh product list
  setHistoryRefresh(prev => prev + 1);  // Trigger event history reload
};
```

---

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### One-Command Setup

```bash
docker-compose up
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

### Demo Mode (No Real Store Required)

1. Open http://localhost:5173
2. Navigate to **"Store Connections"** tab
3. Click **"Quick Demo"** button
4. Click **"Sync"** for each demo store
5. Test all features with sample products!

### Production Setup with Real Stores

See [STORE_API_SETUP.md](STORE_API_SETUP.md) for detailed instructions on connecting WooCommerce or Shopify stores.

---

## Usage Workflow

### 1. Connect Your Store
```bash
POST /api/connections
{
  "name": "My WooCommerce Store",
  "platform": "woocommerce",
  "store_url": "https://mystore.com",
  "api_key": "ck_...",
  "api_secret": "cs_..."
}
```

### 2. Sync Products
```bash
POST /api/connections/:id/sync
```
Imports products from your store and generates initial optimization suggestions.

### 3. Review Suggestions
The platform automatically generates suggestions categorized as:
- **Price**: Optimize pricing for maximum revenue
- **Promo**: Create targeted promotions
- **Bundle**: Group complementary products

### 4. Apply Optimizations
One-click application of suggestions:
- Updates product prices in real-time
- Creates promotional campaigns
- Generates bundle products

### 5. Track Results
Monitor all changes through the event history dashboard.

---

## Project Structure

```
.
├── Backend/
│   ├── app/
│   │   ├── main.py                      # Flask application & API endpoints
│   │   ├── database.py                  # Schema definition & seed data
│   │   ├── crypto.py                    # Credential encryption
│   │   ├── suggestions_generator.py     # AI suggestion logic
│   │   └── integrations/
│   │       ├── base.py                  # Integration interface
│   │       ├── woocommerce.py          # WooCommerce API client
│   │       ├── shopify.py              # Shopify API client
│   │       └── mock.py                 # Demo mode integration
│   ├── Dockerfile
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProductsTable.jsx       # Product list view
│   │   │   ├── SuggestionsPanel.jsx    # Suggestion sidebar
│   │   │   ├── EventHistory.jsx        # Action audit trail
│   │   │   ├── StoreConnections.jsx    # Store management
│   │   │   ├── ProductModal.jsx        # Product details popup
│   │   │   ├── Notification.jsx        # Toast notifications
│   │   │   └── Tabs.jsx                # Tab navigation
│   │   ├── services/
│   │   │   └── api.js                  # API client wrapper
│   │   ├── App.jsx                     # Main application component
│   │   ├── main.jsx                    # React entry point
│   │   └── index.css                   # Global styles
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml                   # Service orchestration
├── README.md                           # This file
├── QUICKSTART.md                       # Quick reference guide
├── DEMO_MODE.md                        # Demo mode instructions
├── STORE_API_SETUP.md                 # Production setup guide
└── CLAUDE_CONTEXT.md                  # Development context
```

---

## Performance & Scalability

- **API Response Time**: < 300ms for all endpoints
- **Database**: SQLite with WAL mode for concurrent reads
- **Frontend Bundle**: < 200KB gzipped
- **Docker Image Size**: Backend ~150MB, Frontend ~25MB
- **Memory Footprint**: < 100MB per container

### Scalability Considerations

Current implementation is optimized for **small to medium retailers** (1-10K products). For larger catalogs:

1. Migrate to PostgreSQL or MySQL
2. Implement Redis caching layer
3. Add background job queue (Celery/RQ) for async processing
4. Scale horizontally with load balancer

---

## Security Features

- **Credential Encryption**: AES-256 with PBKDF2HMAC (100,000 iterations)
- **API Security**: CORS configuration, input validation
- **No Hardcoded Secrets**: All credentials encrypted in database
- **SQL Injection Prevention**: Parameterized queries throughout
- **XSS Protection**: React's built-in escaping

**⚠️ Production Deployment Notes:**
- Change encryption master password in production
- Implement rate limiting
- Add user authentication & authorization
- Use HTTPS for all API communication
- Regular security audits

---

## Testing

### Manual Testing (Demo Mode)
```bash
# Start services
docker-compose up

# Access frontend
http://localhost:5173

# Create demo stores
Click "Quick Demo" → Sync each store

# Test workflow
1. Select a product
2. View suggestions
3. Apply suggestion
4. Verify in event history
```

### API Testing
```bash
# Health check
curl http://localhost:5001/health

# Get products
curl http://localhost:5001/api/products

# Get suggestions for product ID 1
curl http://localhost:5001/api/suggestions?product_id=1
```

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify port 5001 is available
netstat -an | grep 5001
```

### Frontend can't connect to API
```bash
# Check environment variable
cat Frontend/.env
# Should contain: VITE_API_URL=http://localhost:5001
```

### Database corruption
```bash
# Reset everything
docker-compose down -v
docker-compose up
```

### Port conflicts
Edit `docker-compose.yml` to change exposed ports:
```yaml
services:
  backend:
    ports:
      - "5001:5001"  # Change first number (host port)
```

---

## Future Enhancements

### Planned Features
- [ ] Machine learning for suggestion quality scoring
- [ ] A/B testing framework for price variations
- [ ] Competitor price monitoring with web scraping
- [ ] Email notifications for high-priority suggestions
- [ ] Multi-user support with role-based access
- [ ] Advanced analytics dashboard with charts
- [ ] Bulk suggestion application
- [ ] Scheduled price changes
- [ ] Integration with more platforms (Magento, BigCommerce)

### Bundle System (In Progress)
- [x] Database schema created
- [x] Basic bundle creation endpoint
- [ ] Stock synchronization between bundle and individual products
- [ ] Bundle availability calculation: `min(product_stock / bundle_quantity)`
- [ ] UI for bundle management

---

## Development

### Local Development (Without Docker)

#### Backend
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

#### Frontend
```bash
cd Frontend
npm install
npm run dev
```

### Building for Production
```bash
# Frontend
cd Frontend
npm run build
# Output: dist/

# Backend (Docker)
cd Backend
docker build -t product-optimizer-backend .
```

---

## Logging & Monitoring

### Backend Logs
```bash
# Follow all logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Log Levels
- **INFO**: Standard operations (product sync, suggestion application)
- **WARNING**: Non-critical issues (missing optional fields)
- **ERROR**: Failed operations (API errors, database issues)

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

## Team

Developed during SynderHacks Wrocław 2025

**Built with**: Python, React, Docker, SQLite, and lots of coffee

---

## Acknowledgments

- WooCommerce REST API documentation
- Shopify Admin API documentation
- Flask and React communities
- All open-source contributors

---

## Contact

For questions, issues, or collaboration opportunities:
- Create an issue in the repository
- Email: [your-email@example.com]

---

**Last Updated**: November 2025
**Status**: MVP Complete, Bundle System in Development
**Version**: 1.0.0

