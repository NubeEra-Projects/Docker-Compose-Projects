"""
Routes for our microservice application
"""
from flask import request, jsonify, render_template
from app import app
from models import User, Product, Order
import logging

# ---------------------------
# Frontend Routes
# ---------------------------
@app.route('/')
def index():
    """Render the main documentation page"""
    return render_template('index.html')

# ---------------------------
# User Service API
# ---------------------------
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        return jsonify({
            'success': True,
            'users': [vars(user) for user in User.get_all()]
        }), 200
    except Exception as e:
        logging.error(f"Error getting users: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = User.get_by_id(user_id)
        if user:
            return jsonify({
                'success': True,
                'user': vars(user)
            }), 200
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    except Exception as e:
        logging.error(f"Error getting user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        user = User.create(username=data['username'], email=data['email'])
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': vars(user)
        }), 201
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user's details"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        user = User.update(user_id, username=data.get('username'), email=data.get('email'))
        if user:
            return jsonify({
                'success': True,
                'message': 'User updated successfully',
                'user': vars(user)
            }), 200
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        success = User.delete(user_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'User deleted successfully'
            }), 200
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ---------------------------
# Product Service API
# ---------------------------
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        return jsonify({
            'success': True,
            'products': [vars(product) for product in Product.get_all()]
        }), 200
    except Exception as e:
        logging.error(f"Error getting products: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product = Product.get_by_id(product_id)
        if product:
            return jsonify({
                'success': True,
                'product': vars(product)
            }), 200
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404
    except Exception as e:
        logging.error(f"Error getting product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'description', 'price', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        product = Product.create(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            stock=int(data['stock'])
        )
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'product': vars(product)
        }), 201
    except Exception as e:
        logging.error(f"Error creating product: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product's details"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'price' in data:
            update_data['price'] = float(data['price'])
        if 'stock' in data:
            update_data['stock'] = int(data['stock'])
        
        product = Product.update(product_id, **update_data)
        if product:
            return jsonify({
                'success': True,
                'message': 'Product updated successfully',
                'product': vars(product)
            }), 200
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404
    except Exception as e:
        logging.error(f"Error updating product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        success = Product.delete(product_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Product deleted successfully'
            }), 200
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404
    except Exception as e:
        logging.error(f"Error deleting product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ---------------------------
# Order Service API
# ---------------------------
@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        user_id = request.args.get('user_id')
        if user_id:
            orders = Order.get_by_user(user_id)
        else:
            orders = Order.get_all()
            
        # Convert orders to dict for JSON serialization
        order_list = []
        for order in orders:
            order_dict = vars(order).copy()
            order_dict['items'] = [vars(item) for item in order.items]
            order_dict['total'] = order.total
            order_list.append(order_dict)
            
        return jsonify({
            'success': True,
            'orders': order_list
        }), 200
    except Exception as e:
        logging.error(f"Error getting orders: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    try:
        order = Order.get_by_id(order_id)
        if order:
            order_dict = vars(order).copy()
            order_dict['items'] = [vars(item) for item in order.items]
            order_dict['total'] = order.total
            
            return jsonify({
                'success': True,
                'order': order_dict
            }), 200
        return jsonify({
            'success': False,
            'error': 'Order not found'
        }), 404
    except Exception as e:
        logging.error(f"Error getting order {order_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['user_id', 'items']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate user exists
        user = User.get_by_id(data['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'error': f"User with ID {data['user_id']} not found"
            }), 404
        
        # Validate items format
        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return jsonify({
                'success': False,
                'error': 'Items must be a non-empty list'
            }), 400
        
        for item in data['items']:
            if 'product_id' not in item or 'quantity' not in item:
                return jsonify({
                    'success': False,
                    'error': 'Each item must have product_id and quantity'
                }), 400
        
        try:
            order = Order.create(user_id=data['user_id'], items=data['items'])
            
            # Prepare response
            order_dict = vars(order).copy()
            order_dict['items'] = [vars(item) for item in order.items]
            order_dict['total'] = order.total
            
            return jsonify({
                'success': True,
                'message': 'Order created successfully',
                'order': order_dict
            }), 201
        except ValueError as ve:
            return jsonify({
                'success': False,
                'error': str(ve)
            }), 400
    except Exception as e:
        logging.error(f"Error creating order: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update an order's status"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        # Validate status value
        valid_statuses = ['pending', 'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f"Status must be one of: {', '.join(valid_statuses)}"
            }), 400
        
        order = Order.update_status(order_id, data['status'])
        if order:
            order_dict = vars(order).copy()
            order_dict['items'] = [vars(item) for item in order.items]
            order_dict['total'] = order.total
            
            return jsonify({
                'success': True,
                'message': 'Order status updated successfully',
                'order': order_dict
            }), 200
        return jsonify({
            'success': False,
            'error': 'Order not found'
        }), 404
    except Exception as e:
        logging.error(f"Error updating order status for {order_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
