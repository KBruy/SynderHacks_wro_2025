"""Suggestion-related business logic."""
from typing import List, Dict, Optional
import re
from datetime import datetime
from database import get_db
from utils.logger import get_logger

logger = get_logger(__name__)


def get_suggestions_for_product(product_id: int) -> Optional[List[Dict]]:
    """
    Retrieve all suggestions for a specific product.

    Args:
        product_id: ID of the product.

    Returns:
        List of suggestions ordered by status (new first) and creation date,
        or None if product doesn't exist.

    Raises:
        Exception: If database query fails.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Check if product exists
        cursor.execute('SELECT id FROM products WHERE id = ?', (product_id,))
        if not cursor.fetchone():
            logger.warning(f"Product {product_id} not found")
            return None

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
    return suggestions


def apply_suggestion(suggestion_id: int) -> Dict:
    """
    Apply a suggestion and update product if applicable.

    For price suggestions, extracts the new price and updates the product.
    Creates an event in the history.

    Args:
        suggestion_id: ID of the suggestion to apply.

    Returns:
        Dict with success status and details.

    Raises:
        ValueError: If suggestion not found or already applied.
        Exception: If database operation fails.
    """
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
            raise ValueError(f"Suggestion {suggestion_id} not found")

        suggestion = dict(row)

        if suggestion['status'] == 'applied':
            raise ValueError(f"Suggestion {suggestion_id} already applied")

        # Update suggestion status
        now = datetime.now().isoformat(sep=' ', timespec='seconds')
        cursor.execute('''
            UPDATE suggestions
            SET status = 'applied', applied_at = ?
            WHERE id = ?
        ''', (now, suggestion_id))

        # If it's a price suggestion, update the product price
        new_price = _extract_price_from_suggestion(suggestion, cursor)
        if new_price is not None:
            cursor.execute('''
                UPDATE products
                SET price = ?, updated_at = ?
                WHERE id = ?
            ''', (new_price, now, suggestion['product_id']))
            logger.info(f"Updated product {suggestion['product_id']} price to {new_price}")

        # Create event in history
        event_description = (
            f"Zastosowano sugestię [{suggestion['type']}] dla produktu "
            f"'{suggestion['product_name']}': {suggestion['description']}"
        )
        cursor.execute('''
            INSERT INTO events (product_id, suggestion_id, event_type, description, created_at)
            VALUES (?, ?, 'suggestion_applied', ?, ?)
        ''', (suggestion['product_id'], suggestion_id, event_description, now))

        event_id = cursor.lastrowid

    logger.info(f"Applied suggestion {suggestion_id} for product {suggestion['product_id']}")

    return {
        'success': True,
        'message': 'Sugestia została pomyślnie zastosowana',
        'suggestion_id': suggestion_id,
        'event_id': event_id,
        'applied_at': now
    }


def _extract_price_from_suggestion(suggestion: Dict, cursor) -> Optional[float]:
    """
    Extract new price from a price suggestion description.

    Supports patterns:
    - "Podwyższ cenę do 299.99" -> 299.99
    - "Obniż cenę o 15%" -> calculates from current price

    Args:
        suggestion: Suggestion dict with 'type', 'description', 'product_id'.
        cursor: Database cursor for fetching current price if needed.

    Returns:
        New price as float, or None if not a price suggestion or can't extract.
    """
    if suggestion['type'] != 'price':
        return None

    description = suggestion['description']

    # Pattern 1: "Podwyższ cenę do 299.99" or "Podwyższ cenę do 299.99 PLN"
    match = re.search(r'do\s+(\d+\.?\d*)', description)
    if match:
        return float(match.group(1))

    # Pattern 2: "Obniż cenę o 15%" - need current price
    match = re.search(r'o\s+(\d+)%', description)
    if match:
        percent = int(match.group(1))
        # Get current price
        cursor.execute('SELECT price FROM products WHERE id = ?', (suggestion['product_id'],))
        current_price = cursor.fetchone()[0]
        return round(current_price * (1 - percent / 100.0), 2)

    logger.warning(f"Could not extract price from suggestion: {description}")
    return None
