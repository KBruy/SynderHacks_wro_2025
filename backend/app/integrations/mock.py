import random
import logging
from typing import List, Dict
from .base import StoreIntegration

logger = logging.getLogger(__name__)

class MockIntegration(StoreIntegration):
    """Mock integration for testing without real stores"""

    SAMPLE_PRODUCTS = [
        {'name': 'Smartwatch Fitness Pro', 'price': 299.99, 'category': 'Electronics'},
        {'name': 'Wireless Earbuds Elite', 'price': 149.99, 'category': 'Electronics'},
        {'name': 'Portable Power Bank 20000mAh', 'price': 79.99, 'category': 'Electronics'},
        {'name': 'USB-C Charging Cable 2m', 'price': 19.99, 'category': 'Accessories'},
        {'name': 'Bluetooth Speaker Waterproof', 'price': 89.99, 'category': 'Electronics'},
        {'name': 'Phone Stand Adjustable', 'price': 24.99, 'category': 'Accessories'},
        {'name': 'Laptop Sleeve 15 inch', 'price': 34.99, 'category': 'Accessories'},
        {'name': 'Gaming Mouse RGB', 'price': 59.99, 'category': 'Gaming'},
        {'name': 'Mechanical Keyboard', 'price': 129.99, 'category': 'Gaming'},
        {'name': 'Webcam HD 1080p', 'price': 69.99, 'category': 'Electronics'},
        {'name': 'External SSD 1TB', 'price': 149.99, 'category': 'Storage'},
        {'name': 'Phone Case Premium', 'price': 29.99, 'category': 'Accessories'},
        {'name': 'Screen Protector Tempered Glass', 'price': 14.99, 'category': 'Accessories'},
        {'name': 'Wireless Charger Pad', 'price': 39.99, 'category': 'Accessories'},
        {'name': 'Smart Light Bulb RGB', 'price': 24.99, 'category': 'Smart Home'},
        {'name': 'Security Camera WiFi', 'price': 89.99, 'category': 'Smart Home'},
        {'name': 'Smart Plug Mini', 'price': 19.99, 'category': 'Smart Home'},
        {'name': 'Fitness Tracker Band', 'price': 79.99, 'category': 'Fitness'},
        {'name': 'Yoga Mat Premium', 'price': 34.99, 'category': 'Fitness'},
        {'name': 'Resistance Bands Set', 'price': 24.99, 'category': 'Fitness'},
    ]

    def __init__(self, store_url: str, platform: str):
        super().__init__(store_url, 'demo-key')
        self.platform = platform

    def test_connection(self) -> bool:
        """Mock connection test - always succeeds"""
        logger.info(f"Mock connection test for {self.store_url}")
        return True

    def get_products(self, limit: int = 100) -> List[Dict]:
        """Generate mock products"""
        # Randomly select products
        num_products = min(limit, random.randint(8, len(self.SAMPLE_PRODUCTS)))
        selected = random.sample(self.SAMPLE_PRODUCTS, num_products)

        products = []
        for i, product in enumerate(selected, 1):
            # Add some price variation
            price_variation = random.uniform(0.9, 1.1)
            price = round(product['price'] * price_variation, 2)

            # Random stock - some low, most normal
            if random.random() < 0.2:  # 20% chance of low stock
                stock = random.randint(5, 15)
                status = 'low_stock'
            else:
                stock = random.randint(30, 200)
                status = 'active'

            products.append({
                'external_id': f"MOCK-{i}",
                'sku': f"SKU-DEMO-{i:03d}",
                'name': product['name'],
                'price': price,
                'stock': stock,
                'status': status,
                'channel': self.platform
            })

        logger.info(f"Generated {len(products)} mock products")
        return products

    def create_coupon(self, coupon_data: Dict) -> Dict:
        """Mock coupon creation"""
        logger.info(f"Mock coupon created: {coupon_data['code']}")
        return {
            'success': True,
            'coupon_id': f"mock-{random.randint(1000, 9999)}",
            'code': coupon_data['code'],
            'amount': coupon_data['amount']
        }

    def update_product_price(self, product_id: str, new_price: float) -> bool:
        """Mock price update"""
        logger.info(f"Mock price update: {product_id} -> {new_price}")
        return True
