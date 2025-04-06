import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class OrderService:
    """
    Order Service - Simulates a microservice for order management
    
    In a real microservice architecture, this would be a separate service
    with its own database and API endpoints.
    """
    
    def __init__(self):
        # In-memory storage for demonstration
        self.orders = {}
        self.next_id = 1
    
    def get_all_orders(self):
        """Get all orders"""
        logger.debug(f"Getting all orders. Count: {len(self.orders)}")
        return list(self.orders.values())
    
    def get_order_by_id(self, order_id):
        """Get order by ID"""
        logger.debug(f"Getting order by ID: {order_id}")
        return self.orders.get(order_id)
    
    def get_orders_by_user_id(self, user_id):
        """Get orders by user ID"""
        logger.debug(f"Getting orders for user ID: {user_id}")
        return [o for o in self.orders.values() if o.get('user_id') == user_id]
    
    def create_order(self, order_data):
        """Create a new order"""
        if 'id' not in order_data:
            order_data['id'] = self.next_id
            self.next_id += 1
        
        order_id = order_data['id']
        logger.debug(f"Creating order with ID: {order_id}")
        
        # Set default values if not provided
        if 'status' not in order_data:
            order_data['status'] = 'pending'
        
        if 'created_at' not in order_data:
            order_data['created_at'] = datetime.now().isoformat()
        
        # Generate a unique order reference
        order_data['reference'] = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        self.orders[order_id] = order_data
        return order_data
    
    def update_order(self, order_id, order_data):
        """Update an existing order"""
        logger.debug(f"Updating order with ID: {order_id}")
        if order_id not in self.orders:
            logger.error(f"Order with ID {order_id} not found")
            return None
        
        # Update order
        current_order = self.orders[order_id]
        for key, value in order_data.items():
            if key not in ['id', 'reference', 'created_at']:  # Prevent changing certain fields
                current_order[key] = value
        
        current_order['updated_at'] = datetime.now().isoformat()
        self.orders[order_id] = current_order
        return current_order
    
    def delete_order(self, order_id):
        """Delete an order"""
        logger.debug(f"Deleting order with ID: {order_id}")
        if order_id in self.orders:
            del self.orders[order_id]
            return True
        return False
    
    def calculate_order_total(self, items, product_service):
        """Calculate total price for an order"""
        total = 0
        for item in items:
            product = product_service.get_product_by_id(item['product_id'])
            if product:
                total += product['price'] * item['quantity']
        return total
