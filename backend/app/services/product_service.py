"""Product-related business logic."""
from typing import List, Dict, Optional
from database import get_db
from models import db_row_to_product
from utils.logger import get_logger

logger = get_logger(__name__)


def get_all_products() -> List[Dict]:
    """
    Retrieve all products with their applied suggestions.

    Returns:
        List of products in standardized ProductRecord format.

    Raises:
        Exception: If database query fails.
    """
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
                    'row': row_dict,
                    'promotions': []
                }

            # Add applied suggestion if exists
            if row_dict['applied_suggestion_id']:
                products_dict[product_id]['promotions'].append({
                    'id': row_dict['applied_suggestion_id'],
                    'type': row_dict['applied_suggestion_type'],
                    'description': row_dict['applied_suggestion_desc']
                })

        # Convert to ProductRecord using our standard function
        products = []
        for product_data in products_dict.values():
            product = db_row_to_product(product_data['row'], product_data['promotions'])
            products.append(product.dict())

    logger.info(f"Retrieved {len(products)} products")
    return products


def get_product_details(product_id: int) -> Optional[Dict]:
    """
    Get detailed product information including applied suggestions and event history.

    Args:
        product_id: ID of the product to retrieve.

    Returns:
        Product details dict including applied_suggestions and event_history,
        or None if product not found.

    Raises:
        Exception: If database query fails.
    """
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
            logger.warning(f"Product {product_id} not found")
            return None

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
    return product
