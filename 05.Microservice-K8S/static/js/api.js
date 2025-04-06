/**
 * API interaction utilities for the Microservice Demo Application
 * This module provides helper functions for making API requests.
 */

/**
 * Base API class that handles common API operations
 */
class ApiService {
    /**
     * Make a GET request to the specified endpoint
     * 
     * @param {string} endpoint - The API endpoint to request
     * @returns {Promise} - Promise that resolves with the response data
     */
    static async get(endpoint) {
        try {
            const response = await fetch(endpoint, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            return this._handleResponse(response);
        } catch (error) {
            return this._handleError(error);
        }
    }
    
    /**
     * Make a POST request to the specified endpoint
     * 
     * @param {string} endpoint - The API endpoint to request
     * @param {object} data - The data to send in the request body
     * @returns {Promise} - Promise that resolves with the response data
     */
    static async post(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            return this._handleResponse(response);
        } catch (error) {
            return this._handleError(error);
        }
    }
    
    /**
     * Make a PUT request to the specified endpoint
     * 
     * @param {string} endpoint - The API endpoint to request
     * @param {object} data - The data to send in the request body
     * @returns {Promise} - Promise that resolves with the response data
     */
    static async put(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            return this._handleResponse(response);
        } catch (error) {
            return this._handleError(error);
        }
    }
    
    /**
     * Make a DELETE request to the specified endpoint
     * 
     * @param {string} endpoint - The API endpoint to request
     * @returns {Promise} - Promise that resolves with the response data
     */
    static async delete(endpoint) {
        try {
            const response = await fetch(endpoint, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            return this._handleResponse(response);
        } catch (error) {
            return this._handleError(error);
        }
    }
    
    /**
     * Handle API response
     * 
     * @param {Response} response - Fetch API response object
     * @returns {Promise} - Promise that resolves with the parsed response data
     * @private
     */
    static async _handleResponse(response) {
        const data = await response.json();
        
        if (!response.ok) {
            return {
                success: false,
                status: response.status,
                error: data.error || 'Unknown error occurred',
                data: null
            };
        }
        
        return {
            success: true,
            status: response.status,
            data: data
        };
    }
    
    /**
     * Handle API error
     * 
     * @param {Error} error - Error object
     * @returns {object} - Error response object
     * @private
     */
    static _handleError(error) {
        console.error('API error:', error);
        
        return {
            success: false,
            status: 0,
            error: error.message || 'Network error occurred',
            data: null
        };
    }
}

/**
 * User service for user-related API operations
 */
class UserService extends ApiService {
    static async getAllUsers() {
        return await this.get('/api/users');
    }
    
    static async getUser(userId) {
        return await this.get(`/api/users/${userId}`);
    }
    
    static async createUser(userData) {
        return await this.post('/api/users', userData);
    }
    
    static async updateUser(userId, userData) {
        return await this.put(`/api/users/${userId}`, userData);
    }
    
    static async deleteUser(userId) {
        return await this.delete(`/api/users/${userId}`);
    }
}

/**
 * Product service for product-related API operations
 */
class ProductService extends ApiService {
    static async getAllProducts() {
        return await this.get('/api/products');
    }
    
    static async getProduct(productId) {
        return await this.get(`/api/products/${productId}`);
    }
    
    static async createProduct(productData) {
        return await this.post('/api/products', productData);
    }
    
    static async updateProduct(productId, productData) {
        return await this.put(`/api/products/${productId}`, productData);
    }
    
    static async deleteProduct(productId) {
        return await this.delete(`/api/products/${productId}`);
    }
}

/**
 * Order service for order-related API operations
 */
class OrderService extends ApiService {
    static async getAllOrders(userId = null) {
        const endpoint = userId ? `/api/orders?user_id=${userId}` : '/api/orders';
        return await this.get(endpoint);
    }
    
    static async getOrder(orderId) {
        return await this.get(`/api/orders/${orderId}`);
    }
    
    static async createOrder(orderData) {
        return await this.post('/api/orders', orderData);
    }
    
    static async updateOrderStatus(orderId, status) {
        return await this.put(`/api/orders/${orderId}/status`, { status });
    }
}
