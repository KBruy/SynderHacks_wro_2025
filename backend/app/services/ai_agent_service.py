"""AI Agent service using OpenAI to generate smart product suggestions."""
import os
import json
from typing import List, Dict, Optional
from database import get_db
from utils.logger import get_logger

# Import OpenAI last to avoid conflicts
from openai import OpenAI

# Import dummyjson after OpenAI
import sys
sys.path.insert(0, '/app')
from app.services import dummyjson_service

logger = get_logger(__name__)

# Initialize OpenAI client
client = None


def _get_openai_client():
    """Lazy initialization of OpenAI client."""
    global client
    if client is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        try:
            logger.info("Initializing OpenAI client...")
            client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"OpenAI client initialization failed: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    return client


def analyze_product_with_ai(product: Dict, market_data: List[Dict]) -> Dict:
    """
    Use OpenAI to analyze a product against market data and generate suggestions.

    Args:
        product: Product dictionary with id, name, price, stock, etc.
        market_data: List of similar products from DummyJSON.

    Returns:
        Dict with analysis results and suggestions.
    """
    try:
        ai_client = _get_openai_client()
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

        # Prepare prompt
        prompt = f"""Jesteś ekspertem od e-commerce i strategii cenowej. Przeanalizuj produkt ze sklepu Shopify i porównaj go z danymi rynkowymi.

PRODUKT ZE SKLEPU:
- Nazwa: {product['name']}
- Cena: {product['price']} PLN
- Stan magazynowy: {product['stock']} sztuk
- Status: {product['status']}

PODOBNE PRODUKTY NA RYNKU (z DummyJSON):
{json.dumps(market_data[:5], indent=2, ensure_ascii=False)}

ZADANIE:
Wygeneruj 3-5 konkretnych, praktycznych sugestii dotyczących:
1. Optymalizacji ceny (price) - czy cena jest konkurencyjna?
2. Promocji (promo) - jakie akcje promocyjne mogą zwiększyć sprzedaż?
3. Bundli (bundle) - z którymi produktami warto stworzyć pakiet?

WAŻNE:
- Sugestie muszą być KONKRETNE i zawierać konkretne wartości/liczby
- Bierz pod uwagę polski rynek i PLN
- Każda sugestia powinna mieć jasne uzasadnienie biznesowe

Odpowiedz TYLKO w formacie JSON:
{{
  "suggestions": [
    {{
      "type": "price|promo|bundle",
      "description": "Konkretna sugestia z konkretnymi wartościami",
      "reasoning": "Krótkie uzasadnienie biznesowe"
    }}
  ],
  "market_position": "Krótka analiza pozycji rynkowej produktu"
}}"""

        # Call OpenAI
        response = ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Jesteś ekspertem e-commerce specjalizującym się w optymalizacji cen i strategiach sprzedaży."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        # Parse response
        result = json.loads(response.choices[0].message.content)
        logger.info(f"AI analysis completed for product {product['id']}: {product['name']}")

        return result

    except Exception as e:
        logger.error(f"AI analysis failed for product {product['id']}: {e}")
        return {
            "suggestions": [],
            "market_position": "Analiza AI niedostępna",
            "error": str(e)
        }


def generate_suggestions_for_product(product_id: int) -> Dict:
    """
    Generate AI-powered suggestions for a specific product.

    This function:
    1. Fetches product from database
    2. Finds similar products from DummyJSON
    3. Uses OpenAI to analyze and generate suggestions
    4. Saves suggestions to database

    Args:
        product_id: ID of the product to analyze.

    Returns:
        Dict with analysis results and created suggestions.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Get product
        cursor.execute('''
            SELECT id, name, price, stock, status, channel
            FROM products WHERE id = ?
        ''', (product_id,))

        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Product {product_id} not found")

        product = dict(row)

        # Find similar products from DummyJSON
        logger.info(f"Searching DummyJSON for products similar to: {product['name']}")
        market_data = dummyjson_service.find_similar_products(product['name'], product['price'])

        if not market_data:
            logger.warning(f"No market data found for product {product_id}")
            return {
                "product_id": product_id,
                "suggestions_created": 0,
                "message": "Brak danych rynkowych do analizy"
            }

        # Analyze with AI
        logger.info(f"Analyzing product {product_id} with AI agent...")
        analysis = analyze_product_with_ai(product, market_data)

        # Save suggestions to database
        suggestions_created = 0
        for suggestion in analysis.get('suggestions', []):
            try:
                cursor.execute('''
                    INSERT INTO suggestions (product_id, type, description, status)
                    VALUES (?, ?, ?, 'new')
                ''', (
                    product_id,
                    suggestion['type'],
                    f"{suggestion['description']} | Uzasadnienie: {suggestion['reasoning']}"
                ))
                suggestions_created += 1
            except Exception as e:
                logger.error(f"Failed to save suggestion: {e}")

        # Log event
        cursor.execute('''
            INSERT INTO events (product_id, event_type, description)
            VALUES (?, 'ai_analysis', ?)
        ''', (
            product_id,
            f"AI Agent wygenerował {suggestions_created} sugestii. {analysis.get('market_position', '')}"
        ))

        logger.info(f"Created {suggestions_created} AI suggestions for product {product_id}")

        return {
            "product_id": product_id,
            "product_name": product['name'],
            "suggestions_created": suggestions_created,
            "market_position": analysis.get('market_position'),
            "market_products_analyzed": len(market_data)
        }


def generate_suggestions_for_all_products() -> Dict:
    """
    Generate AI suggestions for all products in the database.

    Returns:
        Dict with summary of suggestions generated.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Get all products
        cursor.execute('SELECT id, name FROM products')
        products = cursor.fetchall()

    total_suggestions = 0
    products_analyzed = 0
    errors = []

    for product_row in products:
        product_id = product_row[0]
        product_name = product_row[1]

        try:
            result = generate_suggestions_for_product(product_id)
            total_suggestions += result['suggestions_created']
            products_analyzed += 1
            logger.info(f"Generated {result['suggestions_created']} suggestions for: {product_name}")

        except Exception as e:
            error_msg = f"Failed for product {product_id} ({product_name}): {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)

    return {
        "success": True,
        "products_analyzed": products_analyzed,
        "total_suggestions_created": total_suggestions,
        "errors": errors
    }
