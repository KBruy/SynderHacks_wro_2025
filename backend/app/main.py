"""Flask application - routing and request handling only."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import traceback
from pydantic import ValidationError

from database import init_db, seed_data, get_db
from utils.logger import setup_logger
from utils.validators import CreateConnectionRequest, GetSuggestionsRequest, GetEventsRequest
from services import (
    get_all_products,
    get_product_details,
    get_suggestions_for_product,
    apply_suggestion,
    get_recent_events,
    get_all_connections,
    create_connection,
    delete_connection,
    toggle_connection,
    quick_demo_setup,
    sync_connection,
)

# Configure logging
logger = setup_logger(__name__)

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


# ========== Global Error Handlers ==========

@app.errorhandler(Exception)
def handle_exception(e: Exception):
    """
    Global exception handler for all unhandled exceptions.

    Logs the full traceback and returns a JSON error response.

    Args:
        e: The exception that was raised.

    Returns:
        JSON error response with 500 status code.
    """
    logger.error(f"Unhandled exception: {e}")
    logger.error(traceback.format_exc())
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    """
    Handle Pydantic validation errors.

    Args:
        e: Pydantic ValidationError.

    Returns:
        JSON error response with 400 status code.
    """
    logger.warning(f"Validation error: {e}")
    return jsonify({
        'error': 'Validation failed',
        'details': e.errors()
    }), 400


# ========== Health Check ==========

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON response with system health status.
    """
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


# ========== Product Endpoints ==========

@app.route('/api/products', methods=['GET'])
def api_get_products():
    """
    Get all products in standardized ProductRecord format.

    Returns:
        JSON list of products.
    """
    products = get_all_products()
    return jsonify(products), 200


@app.route('/api/products/<int:product_id>/details', methods=['GET'])
def api_get_product_details(product_id: int):
    """
    Get detailed product information including history.

    Args:
        product_id: Product ID from URL path.

    Returns:
        JSON product details or 404 if not found.
    """
    product = get_product_details(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify(product), 200


# ========== Suggestion Endpoints ==========

@app.route('/api/suggestions', methods=['GET'])
def api_get_suggestions():
    """
    Get suggestions for a specific product.

    Query params:
        product_id: Required product ID.

    Returns:
        JSON list of suggestions or 400/404 on error.
    """
    # Validate query params
    product_id = request.args.get('product_id', type=int)

    if not product_id:
        return jsonify({'error': 'product_id parameter is required'}), 400

    try:
        # Validate using pydantic
        validated = GetSuggestionsRequest(product_id=product_id)
    except ValidationError as e:
        return handle_validation_error(e)

    suggestions = get_suggestions_for_product(validated.product_id)

    if suggestions is None:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify(suggestions), 200


@app.route('/api/suggestions/<int:suggestion_id>/apply', methods=['POST'])
def api_apply_suggestion(suggestion_id: int):
    """
    Apply a suggestion.

    Args:
        suggestion_id: Suggestion ID from URL path.

    Returns:
        JSON success response or 400/404 on error.
    """
    try:
        result = apply_suggestion(suggestion_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# ========== Event Endpoints ==========

@app.route('/api/events', methods=['GET'])
def api_get_events():
    """
    Get recent events (history).

    Query params:
        limit: Optional, default 20.

    Returns:
        JSON list of events.
    """
    limit = request.args.get('limit', default=20, type=int)

    try:
        validated = GetEventsRequest(limit=limit)
    except ValidationError as e:
        return handle_validation_error(e)

    events = get_recent_events(validated.limit)
    return jsonify(events), 200


# ========== Store Connection Endpoints ==========

@app.route('/api/connections', methods=['GET'])
def api_get_connections():
    """
    Get all store connections.

    Returns:
        JSON list of connections.
    """
    connections = get_all_connections()
    return jsonify(connections), 200


@app.route('/api/connections', methods=['POST'])
def api_create_connection():
    """
    Create new store connection.

    Request body:
        name: Connection name (required).
        platform: Platform type - 'shopify' or 'woocommerce' (required).
        store_url: Store URL (required).
        api_key: API key (required).
        api_secret: API secret (optional, required for WooCommerce).

    Returns:
        JSON success response with connection_id or 400 on error.
    """
    try:
        # Validate request body
        data = request.json
        validated = CreateConnectionRequest(**data)

        result = create_connection(validated.dict())
        return jsonify(result), 201
    except ValidationError as e:
        return handle_validation_error(e)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/connections/<int:connection_id>', methods=['DELETE'])
def api_delete_connection(connection_id: int):
    """
    Delete store connection.

    Args:
        connection_id: Connection ID from URL path.

    Returns:
        JSON success response or 404 on error.
    """
    try:
        delete_connection(connection_id)
        return jsonify({
            'success': True,
            'message': 'Połączenie zostało usunięte'
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/connections/<int:connection_id>/toggle', methods=['POST'])
def api_toggle_connection(connection_id: int):
    """
    Toggle connection active status.

    Args:
        connection_id: Connection ID from URL path.

    Returns:
        JSON success response with new status or 404 on error.
    """
    try:
        new_status = toggle_connection(connection_id)
        return jsonify({
            'success': True,
            'is_active': new_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/connections/<int:connection_id>/sync', methods=['POST'])
def api_sync_connection(connection_id: int):
    """
    Sync products from store connection.

    Args:
        connection_id: Connection ID from URL path.

    Returns:
        JSON success response with products_synced count or 400/500 on error.
    """
    try:
        result = sync_connection(connection_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Sync failed for connection {connection_id}: {e}")
        return jsonify({'error': f'Sync failed: {str(e)}'}), 500


@app.route('/api/connections/demo/quick-setup', methods=['POST'])
def api_quick_demo_setup():
    """
    Quickly create demo stores for testing.

    DEPRECATED: Demo mode is no longer supported.

    Returns:
        JSON error response with 400 status code.
    """
    try:
        created_ids = quick_demo_setup()
        return jsonify({
            'success': True,
            'message': f'Utworzono {len(created_ids)} demo sklepy',
            'connection_ids': created_ids
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# ========== Main Entry Point ==========

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
