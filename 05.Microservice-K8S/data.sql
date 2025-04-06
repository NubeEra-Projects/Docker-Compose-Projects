-- This is a sample data.sql file for demonstration purposes
-- It will be used to initialize the database with sample data when PostgreSQL is implemented

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sample data for users
INSERT INTO users (id, username, email) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'john_doe', 'john@example.com'),
    ('550e8400-e29b-41d4-a716-446655440001', 'jane_smith', 'jane@example.com'),
    ('550e8400-e29b-41d4-a716-446655440002', 'mike_wilson', 'mike@example.com');

-- Sample data for products
INSERT INTO products (id, name, description, price, stock) VALUES
    ('550e8400-e29b-41d4-a716-446655440003', 'Smartphone', 'Latest model with high-res camera', 799.99, 50),
    ('550e8400-e29b-41d4-a716-446655440004', 'Laptop', 'Powerful laptop for developers', 1299.99, 30),
    ('550e8400-e29b-41d4-a716-446655440005', 'Headphones', 'Noise-cancelling wireless headphones', 199.99, 100),
    ('550e8400-e29b-41d4-a716-446655440006', 'Smartwatch', 'Fitness tracking and notifications', 249.99, 75),
    ('550e8400-e29b-41d4-a716-446655440007', 'Tablet', '10-inch display with stylus support', 499.99, 40);

-- Sample data for orders
INSERT INTO orders (id, user_id, status) VALUES
    ('550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440000', 'delivered'),
    ('550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440001', 'shipped'),
    ('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440002', 'pending'),
    ('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440000', 'pending');

-- Sample data for order items
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES
    ('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440003', 1, 799.99),
    ('550e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440005', 1, 199.99),
    ('550e8400-e29b-41d4-a716-446655440014', '550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440004', 1, 1299.99),
    ('550e8400-e29b-41d4-a716-446655440015', '550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440006', 2, 249.99),
    ('550e8400-e29b-41d4-a716-446655440016', '550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440003', 1, 799.99),
    ('550e8400-e29b-41d4-a716-446655440017', '550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440007', 1, 499.99);
