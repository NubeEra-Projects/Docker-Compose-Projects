import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ProductService:
    """
    Product Service - Simulates a microservice for product management
    
    In a real microservice architecture, this would be a separate service
    with its own database and API endpoints.
    """
    
    def __init__(self):
        # In-memory storage for demonstration
        self.products = {}
        self.next_id = 1
    
    def get_all_products(self):
        """Get all products"""
        logger.debug(f"Getting all products. Count: {len(self.products)}")
        return list(self.products.values())
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        logger.debug(f"Getting product by ID: {product_id}")
        return self.products.get(product_id)
    
    def get_products_by_category(self, category):
        """Get products by category"""
        logger.debug(f"Getting products by category: {category}")
        return [p for p in self.products.values() if p.get('category') == category]
    
    def create_product(self, product_data):
        """Create a new product"""
        if 'id' not in product_data:
            product_data['id'] = self.next_id
            self.next_id += 1
        
        product_id = product_data['id']
        logger.debug(f"Creating product with ID: {product_id}")
        
        product_data['created_at'] = datetime.now().isoformat()
        self.products[product_id] = product_data
        return product_data
    
    def update_product(self, product_id, product_data):
        """Update an existing product"""
        logger.debug(f"Updating product with ID: {product_id}")
        if product_id not in self.products:
            logger.error(f"Product with ID {product_id} not found")
            return None
        
        # Update product
        current_product = self.products[product_id]
        for key, value in product_data.items():
            if key != 'id':  # Prevent changing the ID
                current_product[key] = value
        
        current_product['updated_at'] = datetime.now().isoformat()
        self.products[product_id] = current_product
        return current_product
    
    def delete_product(self, product_id):
        """Delete a product"""
        logger.debug(f"Deleting product with ID: {product_id}")
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    def search_products(self, query):
        """Search products by name or description"""
        logger.debug(f"Searching products with query: {query}")
        query = query.lower()
        return [
            p for p in self.products.values() 
            if query in p.get('name', '').lower() or query in p.get('description', '').lower()
        ]
    
    def check_inventory(self, product_id, quantity):
        """Check if a product has sufficient inventory"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        
        return product.get('inventory', 0) >= quantity
