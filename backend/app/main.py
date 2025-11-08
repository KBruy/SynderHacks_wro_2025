from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import logging
import re
from database import init_db, seed_data, get_db
from crypto import encrypt, decrypt
from integrations.woocommerce import WooCommerceIntegration
from integrations.shopify import ShopifyIntegration
from integrations.mock import MockIntegration
from suggestions_generator import generate_suggestions_for_product

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permissive CORS for demo

# Initialize database on startup
with app.app_context():
    try:
        init_db()
        seed_data()
        logger.info("Database initialized and seeded successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM products')
            product_count = cursor.fetchone()[0]

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'products_count': product_count
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with active promotions"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    p.id, p.sku, p.name, p.price, p.stock, p.status, p.channel, p.created_at,
                    s.id as applied_suggestion_id,
                    s.type as applied_suggestion_type,
                    s.description as applied_suggestion_desc
                FROM products p
                LEFT JOIN suggestions s ON p.id = s.product_id AND s.status = 'applied'
                ORDER BY p.id
            ''')
            rows = cursor.fetchall()

            # Group by product (in case multiple suggestions applied)
            products_dict = {}
            for row in rows:
                row_dict = dict(row)
                product_id = row_dict['id']

                if product_id not in products_dict:
                    products_dict[product_id] = {
                        'id': row_dict['id'],
                        'sku': row_dict['sku'],
                        'name': row_dict['name'],
                        'price': row_dict['price'],
                        'stock': row_dict['stock'],
                        'status': row_dict['status'],
                        'channel': row_dict['channel'],
                        'created_at': row_dict['created_at'],
                        'active_promotions': []
                    }

                # Add applied suggestion if exists
                if row_dict['applied_suggestion_id']:
                    products_dict[product_id]['active_promotions'].append({
                        'id': row_dict['applied_suggestion_id'],
                        'type': row_dict['applied_suggestion_type'],
                        'description': row_dict['applied_suggestion_desc']
                    })

            products = list(products_dict.values())

        logger.info(f"Retrieved {len(products)} products")
        return jsonify(products), 200
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({'error': 'Failed to fetch products'}), 500


@app.route('/api/products/<int:product_id>/details', methods=['GET'])
def get_product_details(product_id):
    """Get detailed product information including history"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()

            # Get product details
            cursor.execute('''
                SELECT id, sku, name, price, stock, status, channel, connection_id, created_at, updated_at
                FROM products
                WHERE id = ?
            ''', (product_id,))
            row = cursor.fetchone()

            if not row:
                return jsonify({'error': 'Product not found'}), 404

            product = dict(row)

            # Get applied suggestions for this product
            cursor.execute('''
                SELECT id, type, description, applied_at
                FROM suggestions
                WHERE product_id = ? AND status = 'applied'
                ORDER BY applied_at DESC
            ''', (product_id,))
            product['applied_suggestions'] = [dict(row) for row in cursor.fetchall()]

            # Get event history for this product
            cursor.execute('''
                SELECT id, event_type, description, created_at
                FROM events
                WHERE product_id = ?
                ORDER BY created_at DESC
                LIMIT 20
            ''', (product_id,))
            product['event_history'] = [dict(row) for row in cursor.fetchall()]

        logger.info(f"Retrieved details for product {product_id}")
        return jsonify(product), 200
    except Exception as e:
        logger.error(f"Error fetching product details: {e}")
        return jsonify({'error': 'Failed to fetch product details'}), 500


@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggestions for a specific product"""
    product_id = request.args.get('product_id', type=int)

    if not product_id:
        return jsonify({'error': 'product_id parameter is required'}), 400

    try:
        with get_db() as conn:
            cursor = conn.cursor()

            # Check if product exists
            cursor.execute('SELECT id FROM products WHERE id = ?', (product_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Product not found'}), 404

            # Get suggestions
            cursor.execute('''
                SELECT id, product_id, type, description, status, created_at, applied_at
                FROM suggestions
                WHERE product_id = ?
                ORDER BY
                    CASE status
                        WHEN 'new' THEN 1
                        WHEN 'applied' THEN 2
                        ELSE 3
                    END,
                    created_at DESC
            ''', (product_id,))
            rows = cursor.fetchall()

            suggestions = [dict(row) for row in rows]

        logger.info(f"Retrieved {len(suggestions)} suggestions for product {product_id}")
        return jsonify(suggestions), 200
    except Exception as e:
        logger.error(f"Error fetching suggestions: {e}")
        return jsonify({'error': 'Failed to fetch suggestions'}), 500


@app.route('/api/suggestions/<int:suggestion_id>/apply', methods=['POST'])
def apply_suggestion(suggestion_id):
    """Apply a suggestion"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()

            # Get suggestion details
            cursor.execute('''
                SELECT s.id, s.product_id, s.type, s.description, s.status, p.name as product_name
                FROM suggestions s
                JOIN products p ON s.product_id = p.id
                WHERE s.id = ?
            ''', (suggestion_id,))
            row = cursor.fetchone()

            if not row:
                return jsonify({'error': 'Suggestion not found'}), 404

            suggestion = dict(row)

            if suggestion['status'] == 'applied':
                return jsonify({
                    'error': 'Suggestion already applied',
                    'suggestion': suggestion
                }), 400

            # Update suggestion status
            now = datetime.now().isoformat(sep=' ', timespec='seconds')
            cursor.execute('''
                UPDATE suggestions
                SET status = 'applied', applied_at = ?
                WHERE id = ?
            ''', (now, suggestion_id))

            # If it's a price suggestion, update the product price
            if suggestion['type'] == 'price':
                new_price = None
                description = suggestion['description']

                # Try to extract new price from description
                # Pattern 1: "Podwyższ cenę do 299.99" or "Podwyższ cenę do 299.99 PLN"
                match = re.search(r'do\s+(\d+\.?\d*)', description)
                if match:
                    new_price = float(match.group(1))
                else:
                    # Pattern 2: "Obniż cenę o 15%" - need current price
                    match = re.search(r'o\s+(\d+)%', description)
                    if match:
                        percent = int(match.group(1))
                        # Get current price
                        cursor.execute('SELECT price FROM products WHERE id = ?', (suggestion['product_id'],))
                        current_price = cursor.fetchone()[0]
                        new_price = round(current_price * (1 - percent / 100.0), 2)

                if new_price:
                    cursor.execute('''
                        UPDATE products
                        SET price = ?, updated_at = ?
                        WHERE id = ?
                    ''', (new_price, now, suggestion['product_id']))
                    logger.info(f"Updated product {suggestion['product_id']} price to {new_price}")

            # Create event in history
            event_description = f"Zastosowano sugestię [{suggestion['type']}] dla produktu '{suggestion['product_name']}': {suggestion['description']}"
            cursor.execute('''
                INSERT INTO events (product_id, suggestion_id, event_type, description, created_at)
                VALUES (?, ?, 'suggestion_applied', ?, ?)
            ''', (suggestion['product_id'], suggestion_id, event_description, now))

            event_id = cursor.lastrowid

        logger.info(f"Applied suggestion {suggestion_id} for product {suggestion['product_id']}")

        return jsonify({
            'success': True,
            'message': 'Sugestia została pomyślnie zastosowana',
            'suggestion_id': suggestion_id,
            'event_id': event_id,
            'applied_at': now
        }), 200
    except Exception as e:
        logger.error(f"Error applying suggestion: {e}")
        return jsonify({'error': 'Failed to apply suggestion'}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """Get recent events (history)"""
    limit = request.args.get('limit', default=20, type=int)

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    e.id,
                    e.product_id,
                    e.suggestion_id,
                    e.event_type,
                    e.description,
                    e.created_at,
                    p.name as product_name,
                    p.sku as product_sku
                FROM events e
                LEFT JOIN products p ON e.product_id = p.id
                ORDER BY e.created_at DESC
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()

            events = [dict(row) for row in rows]

        logger.info(f"Retrieved {len(events)} events")
        return jsonify(events), 200
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({'error': 'Failed to fetch events'}), 500


# ========== Store Connections Management ==========

@app.route('/api/connections', methods=['GET'])
def get_connections():
    """Get all store connections"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, platform, store_url, is_active, last_sync, created_at
                FROM store_connections
                ORDER BY created_at DESC
            ''')
            rows = cursor.fetchall()
            connections = [dict(row) for row in rows]

        return jsonify(connections), 200
    except Exception as e:
        logger.error(f"Error fetching connections: {e}")
        return jsonify({'error': 'Failed to fetch connections'}), 500


@app.route('/api/connections', methods=['POST'])
def create_connection():
    """Create new store connection"""
    try:
        data = request.json
        required_fields = ['name', 'platform', 'store_url', 'api_key']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Encrypt credentials
        api_key_encrypted = encrypt(data['api_key'])
        api_secret_encrypted = encrypt(data.get('api_secret', '')) if data.get('api_secret') else None

        # Test connection before saving
        platform = data['platform'].lower()
        is_demo = data.get('demo_mode', False)

        try:
            if is_demo or platform == 'demo':
                # Demo mode - no real connection test needed
                integration = MockIntegration(data['store_url'], platform if platform != 'demo' else 'woocommerce')
                platform = platform if platform != 'demo' else 'woocommerce'
            elif platform == 'woocommerce':
                if not data.get('api_secret'):
                    return jsonify({'error': 'WooCommerce requires both api_key and api_secret'}), 400
                integration = WooCommerceIntegration(
                    data['store_url'],
                    data['api_key'],
                    data['api_secret']
                )
            elif platform == 'shopify':
                integration = ShopifyIntegration(
                    data['store_url'],
                    data['api_key']
                )
            else:
                return jsonify({'error': f'Unsupported platform: {platform}'}), 400

            if not integration.test_connection():
                return jsonify({'error': 'Connection test failed. Please check your credentials.'}), 400

        except Exception as e:
            logger.error(f"Connection test error: {e}")
            return jsonify({'error': f'Connection test failed: {str(e)}'}), 400

        # Save connection
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO store_connections
                (name, platform, store_url, api_key_encrypted, api_secret_encrypted, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (data['name'], platform, data['store_url'], api_key_encrypted, api_secret_encrypted))

            connection_id = cursor.lastrowid

            # Log event
            event_time = datetime.now().isoformat(sep=' ', timespec='seconds')
            cursor.execute('''
                INSERT INTO events (event_type, description, created_at)
                VALUES ('connection_created', ?, ?)
            ''', (f"Dodano nowe połączenie: {data['name']} ({platform})", event_time))

        logger.info(f"Created connection {connection_id}: {data['name']}")
        return jsonify({
            'success': True,
            'connection_id': connection_id,
            'message': 'Połączenie zostało pomyślnie utworzone'
        }), 201

    except Exception as e:
        logger.error(f"Error creating connection: {e}")
        return jsonify({'error': 'Failed to create connection'}), 500


@app.route('/api/connections/<int:connection_id>', methods=['DELETE'])
def delete_connection(connection_id):
    """Delete store connection"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()

            # Get connection name for logging
            cursor.execute('SELECT name FROM store_connections WHERE id = ?', (connection_id,))
            row = cursor.fetchone()
            if not row:
                return jsonify({'error': 'Connection not found'}), 404

            connection_name = row[0]

            # Delete associated products first
            cursor.execute('DELETE FROM products WHERE connection_id = ?', (connection_id,))

            # Delete connection
            cursor.execute('DELETE FROM store_connections WHERE id = ?', (connection_id,))

            # Log event
            event_time = datetime.now().isoformat(sep=' ', timespec='seconds')
            cursor.execute('''
                INSERT INTO events (event_type, description, created_at)
                VALUES ('connection_deleted', ?, ?)
            ''', (f"Usunięto połączenie: {connection_name}", event_time))

        logger.info(f"Deleted connection {connection_id}")
        return jsonify({'success': True, 'message': 'Połączenie zostało usunięte'}), 200

    except Exception as e:
        logger.error(f"Error deleting connection: {e}")
        return jsonify({'error': 'Failed to delete connection'}), 500


@app.route('/api/connections/<int:connection_id>/toggle', methods=['POST'])
def toggle_connection(connection_id):
    """Toggle connection active status"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT is_active, name FROM store_connections WHERE id = ?', (connection_id,))
            row = cursor.fetchone()
            if not row:
                return jsonify({'error': 'Connection not found'}), 404

            is_active, name = row
            new_status = 0 if is_active else 1

            cursor.execute('UPDATE store_connections SET is_active = ? WHERE id = ?', (new_status, connection_id))

            status_text = 'aktywowano' if new_status else 'dezaktywowano'
            cursor.execute('''
                INSERT INTO events (event_type, description)
                VALUES ('connection_toggled', ?)
            ''', (f"{status_text.capitalize()} połączenie: {name}",))

        return jsonify({'success': True, 'is_active': bool(new_status)}), 200

    except Exception as e:
        logger.error(f"Error toggling connection: {e}")
        return jsonify({'error': 'Failed to toggle connection'}), 500


@app.route('/api/connections/<int:connection_id>/sync', methods=['POST'])
def sync_connection(connection_id):
    """Sync products from store connection"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()

            # Get connection details
            cursor.execute('''
                SELECT name, platform, store_url, api_key_encrypted, api_secret_encrypted, is_active
                FROM store_connections WHERE id = ?
            ''', (connection_id,))
            row = cursor.fetchone()

            if not row:
                return jsonify({'error': 'Connection not found'}), 404

            if not row[5]:  # is_active
                return jsonify({'error': 'Connection is not active'}), 400

            name, platform, store_url, api_key_enc, api_secret_enc = row[0], row[1], row[2], row[3], row[4]

            # Decrypt credentials
            api_key = decrypt(api_key_enc)
            api_secret = decrypt(api_secret_enc) if api_secret_enc else None

            # Create integration instance
            # Check if this is a demo connection
            is_demo = api_key == 'demo-key'

            if is_demo:
                integration = MockIntegration(store_url, platform)
            elif platform == 'woocommerce':
                integration = WooCommerceIntegration(store_url, api_key, api_secret)
            elif platform == 'shopify':
                integration = ShopifyIntegration(store_url, api_key)
            else:
                return jsonify({'error': f'Unsupported platform: {platform}'}), 400

            # Fetch products
            products = integration.get_products(limit=100)

            if not products:
                return jsonify({'error': 'No products fetched or sync failed'}), 500

            # Upsert products to database
            products_synced = 0
            new_products_for_suggestions = []

            for product in products:
                try:
                    # Check if product exists by SKU
                    cursor.execute('SELECT id FROM products WHERE sku = ?', (product['sku'],))
                    existing = cursor.fetchone()

                    if existing:
                        # Update existing product
                        cursor.execute('''
                            UPDATE products
                            SET name = ?, price = ?, stock = ?, status = ?, connection_id = ?,
                                external_id = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE sku = ?
                        ''', (product['name'], product['price'], product.get('stock', 0), product['status'],
                              connection_id, product['external_id'], product['sku']))
                        product_id = existing[0]
                    else:
                        # Insert new product
                        cursor.execute('''
                            INSERT INTO products
                            (sku, name, price, stock, status, channel, connection_id, external_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (product['sku'], product['name'], product['price'], product.get('stock', 0),
                              product['status'], product['channel'], connection_id, product['external_id']))
                        product_id = cursor.lastrowid

                        # Mark for suggestion generation (only for new products in demo mode)
                        if is_demo:
                            new_products_for_suggestions.append({
                                'id': product_id,
                                'name': product['name'],
                                'price': product['price']
                            })

                    products_synced += 1
                except Exception as e:
                    logger.error(f"Error syncing product {product.get('sku')}: {e}")
                    continue

            # Generate suggestions for new demo products
            if is_demo and new_products_for_suggestions:
                suggestions_created = 0
                for prod in new_products_for_suggestions:
                    suggestions = generate_suggestions_for_product(prod['id'], prod['name'], prod['price'])
                    for suggestion in suggestions:
                        try:
                            cursor.execute('''
                                INSERT INTO suggestions (product_id, type, description, status)
                                VALUES (?, ?, ?, ?)
                            ''', (suggestion['product_id'], suggestion['type'],
                                  suggestion['description'], suggestion['status']))
                            suggestions_created += 1
                        except Exception as e:
                            logger.error(f"Error creating suggestion: {e}")
                            continue

                logger.info(f"Generated {suggestions_created} suggestions for {len(new_products_for_suggestions)} new products")

            # Update last_sync timestamp
            now = datetime.utcnow().isoformat()
            cursor.execute('UPDATE store_connections SET last_sync = ? WHERE id = ?', (now, connection_id))

            # Log sync
            cursor.execute('''
                INSERT INTO sync_logs (connection_id, sync_type, status, products_synced)
                VALUES (?, 'products', 'success', ?)
            ''', (connection_id, products_synced))

            cursor.execute('''
                INSERT INTO events (event_type, description)
                VALUES ('products_synced', ?)
            ''', (f"Zsynchronizowano {products_synced} produktów z {name}",))

        logger.info(f"Synced {products_synced} products from connection {connection_id}")
        return jsonify({
            'success': True,
            'products_synced': products_synced,
            'message': f'Zsynchronizowano {products_synced} produktów'
        }), 200

    except Exception as e:
        logger.error(f"Error syncing connection: {e}")
        # Log failed sync
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sync_logs (connection_id, sync_type, status, error_message)
                    VALUES (?, 'products', 'failed', ?)
                ''', (connection_id, str(e)))
        except:
            pass

        return jsonify({'error': f'Sync failed: {str(e)}'}), 500


@app.route('/api/connections/demo/quick-setup', methods=['POST'])
def quick_demo_setup():
    """Quickly create demo stores for testing"""
    try:
        demo_stores = [
            {
                'name': 'Demo WooCommerce Store',
                'platform': 'woocommerce',
                'store_url': 'https://demo-woocommerce.example.com',
            },
            {
                'name': 'Demo Shopify Store',
                'platform': 'shopify',
                'store_url': 'demo-shopify.myshopify.com',
            }
        ]

        created_ids = []

        with get_db() as conn:
            cursor = conn.cursor()

            for store in demo_stores:
                # Create demo connection with special demo-key
                api_key_encrypted = encrypt('demo-key')

                cursor.execute('''
                    INSERT INTO store_connections
                    (name, platform, store_url, api_key_encrypted, api_secret_encrypted, is_active)
                    VALUES (?, ?, ?, ?, NULL, 1)
                ''', (store['name'], store['platform'], store['store_url'], api_key_encrypted))

                created_ids.append(cursor.lastrowid)

            # Log event
            cursor.execute('''
                INSERT INTO events (event_type, description)
                VALUES ('demo_setup', 'Utworzono demo sklepy do testów')
            ''')

        logger.info(f"Created {len(created_ids)} demo stores")
        return jsonify({
            'success': True,
            'message': f'Utworzono {len(created_ids)} demo sklepy',
            'connection_ids': created_ids
        }), 201

    except Exception as e:
        logger.error(f"Error creating demo stores: {e}")
        return jsonify({'error': 'Failed to create demo stores'}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
