"""
Models module: Contains data structures used in our microservice application

For the MVP, we'll use in-memory storage with these model classes
Later, these will be converted to SQLAlchemy models
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import uuid

# In-memory data stores
users = {}
products = {}
orders = {}


@dataclass
class User:
    """User model representing customers in our system"""
    id: str  # UUID as string
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, username: str, email: str) -> 'User':
        """Create a new user with a generated UUID"""
        user_id = str(uuid.uuid4())
        user = cls(id=user_id, username=username, email=email)
        users[user_id] = user
        return user
    
    @classmethod
    def get_all(cls) -> List['User']:
        """Get all users"""
        return list(users.values())
    
    @classmethod
    def get_by_id(cls, user_id: str) -> Optional['User']:
        """Get a user by ID"""
        return users.get(user_id)
    
    @classmethod
    def update(cls, user_id: str, username: str = None, email: str = None) -> Optional['User']:
        """Update a user's details"""
        user = cls.get_by_id(user_id)
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            return user
        return None
    
    @classmethod
    def delete(cls, user_id: str) -> bool:
        """Delete a user by ID"""
        if user_id in users:
            del users[user_id]
            return True
        return False


@dataclass
class Product:
    """Product model representing items available for purchase"""
    id: str  # UUID as string
    name: str
    description: str
    price: float
    stock: int
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, name: str, description: str, price: float, stock: int) -> 'Product':
        """Create a new product with a generated UUID"""
        product_id = str(uuid.uuid4())
        product = cls(id=product_id, name=name, description=description, price=price, stock=stock)
        products[product_id] = product
        return product
    
    @classmethod
    def get_all(cls) -> List['Product']:
        """Get all products"""
        return list(products.values())
    
    @classmethod
    def get_by_id(cls, product_id: str) -> Optional['Product']:
        """Get a product by ID"""
        return products.get(product_id)
    
    @classmethod
    def update(cls, product_id: str, **kwargs) -> Optional['Product']:
        """Update a product's details"""
        product = cls.get_by_id(product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            return product
        return None
    
    @classmethod
    def delete(cls, product_id: str) -> bool:
        """Delete a product by ID"""
        if product_id in products:
            del products[product_id]
            return True
        return False


@dataclass
class OrderItem:
    """Order item representing a product in an order"""
    product_id: str
    quantity: int
    unit_price: float
    
    @property
    def total_price(self) -> float:
        """Calculate the total price for this order item"""
        return self.unit_price * self.quantity


@dataclass
class Order:
    """Order model representing a customer purchase"""
    id: str  # UUID as string
    user_id: str
    items: List[OrderItem]
    status: str  # 'pending', 'shipped', 'delivered', 'cancelled'
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def total(self) -> float:
        """Calculate the total price of the order"""
        return sum(item.total_price for item in self.items)
    
    @classmethod
    def create(cls, user_id: str, items: List[Dict]) -> 'Order':
        """Create a new order with a generated UUID"""
        order_id = str(uuid.uuid4())
        
        # Convert item dictionaries to OrderItem objects
        order_items = []
        for item in items:
            product = Product.get_by_id(item['product_id'])
            if not product:
                raise ValueError(f"Product with ID {item['product_id']} not found")
            
            if item['quantity'] > product.stock:
                raise ValueError(f"Insufficient stock for product {product.name}")
            
            # Update product stock
            product.stock -= item['quantity']
            
            order_items.append(OrderItem(
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=product.price
            ))
        
        order = cls(id=order_id, user_id=user_id, items=order_items, status='pending')
        orders[order_id] = order
        return order
    
    @classmethod
    def get_all(cls) -> List['Order']:
        """Get all orders"""
        return list(orders.values())
    
    @classmethod
    def get_by_id(cls, order_id: str) -> Optional['Order']:
        """Get an order by ID"""
        return orders.get(order_id)
    
    @classmethod
    def get_by_user(cls, user_id: str) -> List['Order']:
        """Get all orders for a specific user"""
        return [order for order in orders.values() if order.user_id == user_id]
    
    @classmethod
    def update_status(cls, order_id: str, status: str) -> Optional['Order']:
        """Update an order's status"""
        order = cls.get_by_id(order_id)
        if order:
            order.status = status
            return order
        return None
