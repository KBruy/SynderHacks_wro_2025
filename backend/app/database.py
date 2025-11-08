import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

DATABASE_PATH = '/data/db.sqlite'

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize database schema"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                channel TEXT NOT NULL,
                connection_id INTEGER,
                external_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (connection_id) REFERENCES store_connections (id)
            )
        ''')

        # Suggestions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                applied_at TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Events table (history)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                suggestion_id INTEGER,
                event_type TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (suggestion_id) REFERENCES suggestions (id)
            )
        ''')

        # Store connections table (encrypted credentials)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS store_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                store_url TEXT NOT NULL,
                api_key_encrypted TEXT NOT NULL,
                api_secret_encrypted TEXT,
                is_active INTEGER DEFAULT 1,
                last_sync TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Sync logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                connection_id INTEGER NOT NULL,
                sync_type TEXT NOT NULL,
                status TEXT NOT NULL,
                products_synced INTEGER DEFAULT 0,
                error_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (connection_id) REFERENCES store_connections (id)
            )
        ''')

        # Competitor tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitor_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                competitor_name TEXT NOT NULL,
                competitor_url TEXT NOT NULL,
                competitor_price REAL NOT NULL,
                checked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Bundles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bundles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                channel TEXT NOT NULL,
                connection_id INTEGER,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (connection_id) REFERENCES store_connections (id)
            )
        ''')

        # Bundle items table (products that make up a bundle)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bundle_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bundle_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (bundle_id) REFERENCES bundles (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
        ''')

def seed_data():
    """Seed database with initial data"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Check if already seeded
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] > 0:
            return

        # Seed products
        products = [
            ('SKU-001', 'Smartwatch Fitness Pro', 299.99, 50, 'active', 'woocommerce'),
            ('SKU-002', 'Wireless Earbuds Elite', 149.99, 120, 'active', 'shopify'),
            ('SKU-003', 'Portable Power Bank 20000mAh', 79.99, 100, 'active', 'woocommerce'),
            ('SKU-004', 'USB-C Charging Cable 2m', 19.99, 8, 'low_stock', 'shopify'),
            ('SKU-005', 'Bluetooth Speaker Waterproof', 89.99, 75, 'active', 'woocommerce'),
            ('SKU-006', 'Phone Stand Adjustable', 24.99, 200, 'active', 'shopify'),
            ('SKU-007', 'Laptop Sleeve 15 inch', 34.99, 60, 'active', 'woocommerce'),
            ('SKU-008', 'Gaming Mouse RGB', 59.99, 15, 'low_stock', 'shopify'),
        ]

        cursor.executemany(
            'INSERT INTO products (sku, name, price, stock, status, channel) VALUES (?, ?, ?, ?, ?, ?)',
            products
        )

        # Seed suggestions
        suggestions = [
            # Product 1 - Smartwatch
            (1, 'price', 'Obniż cenę o 10% - konkurencja oferuje podobny produkt za 269.99', 'new'),
            (1, 'bundle', 'Stwórz bundle ze słuchawkami (SKU-002) z 15% rabatem', 'new'),
            (1, 'promo', 'Promocja "Fitness Challenge" - kup smartwatch, otrzymaj darmowy pasek', 'applied'),

            # Product 2 - Earbuds
            (2, 'price', 'Podwyższ cenę do 169.99 - high demand, niska dostępność u konkurencji', 'new'),
            (2, 'promo', 'Black Friday: 20% rabatu na pierwsze 50 sztuk', 'new'),

            # Product 3 - Power Bank
            (3, 'bundle', 'Bundle z kablem USB-C (SKU-004) za 94.99 zamiast 99.98', 'new'),
            (3, 'promo', 'Darmowa wysyłka przy zakupie 2 sztuk', 'new'),

            # Product 4 - Cable
            (4, 'price', 'Promocyjna cena 14.99 dla klientów kupujących power bank', 'new'),
            (4, 'promo', 'Kup 3, zapłać za 2', 'new'),

            # Product 5 - Speaker
            (5, 'bundle', 'Summer Bundle: głośnik + power bank za 159.99', 'new'),
            (5, 'promo', 'Letnia wyprzedaż: -15%', 'applied'),

            # Product 6 - Phone Stand
            (6, 'price', 'Test A/B: sprawdź 29.99 vs obecna cena', 'new'),

            # Product 7 - Laptop Sleeve
            (7, 'promo', 'Back to School: -20% dla studentów', 'new'),

            # Product 8 - Gaming Mouse
            (8, 'price', 'Podwyżka do 69.99 - limited stock, high demand', 'new'),
            (8, 'bundle', 'Gaming Bundle: mysz + podkładka za 79.99', 'new'),
        ]

        cursor.executemany(
            'INSERT INTO suggestions (product_id, type, description, status) VALUES (?, ?, ?, ?)',
            suggestions
        )

        # Seed initial events
        events = [
            (1, 3, 'suggestion_applied', 'Zastosowano sugestię: Promocja "Fitness Challenge"'),
            (5, 11, 'suggestion_applied', 'Zastosowano sugestię: Letnia wyprzedaż: -15%'),
            (None, None, 'system', 'System zainicjalizowany z danymi startowymi'),
        ]

        cursor.executemany(
            'INSERT INTO events (product_id, suggestion_id, event_type, description) VALUES (?, ?, ?, ?)',
            events
        )
