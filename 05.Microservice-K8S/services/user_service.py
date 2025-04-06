import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserService:
    """
    User Service - Simulates a microservice for user management
    
    In a real microservice architecture, this would be a separate service
    with its own database and API endpoints.
    """
    
    def __init__(self):
        # In-memory storage for demonstration
        self.users = {}
        self.next_id = 1
    
    def get_all_users(self):
        """Get all users"""
        logger.debug(f"Getting all users. Count: {len(self.users)}")
        return list(self.users.values())
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        logger.debug(f"Getting user by ID: {user_id}")
        return self.users.get(user_id)
    
    def get_user_by_username(self, username):
        """Get user by username"""
        logger.debug(f"Getting user by username: {username}")
        for user in self.users.values():
            if user.get('username') == username:
                return user
        return None
    
    def create_user(self, user_data):
        """Create a new user"""
        if 'id' not in user_data:
            user_data['id'] = self.next_id
            self.next_id += 1
        
        user_id = user_data['id']
        
        # Check if username already exists
        if 'username' in user_data:
            existing_user = self.get_user_by_username(user_data['username'])
            if existing_user and existing_user['id'] != user_id:
                logger.error(f"Username {user_data['username']} already exists")
                return None
        
        logger.debug(f"Creating user with ID: {user_id}")
        user_data['created_at'] = datetime.now().isoformat()
        self.users[user_id] = user_data
        return user_data
    
    def update_user(self, user_id, user_data):
        """Update an existing user"""
        logger.debug(f"Updating user with ID: {user_id}")
        if user_id not in self.users:
            logger.error(f"User with ID {user_id} not found")
            return None
        
        # Check if username already exists
        if 'username' in user_data:
            existing_user = self.get_user_by_username(user_data['username'])
            if existing_user and existing_user['id'] != user_id:
                logger.error(f"Username {user_data['username']} already exists")
                return None
        
        # Update user
        current_user = self.users[user_id]
        for key, value in user_data.items():
            if key != 'id':  # Prevent changing the ID
                current_user[key] = value
        
        current_user['updated_at'] = datetime.now().isoformat()
        self.users[user_id] = current_user
        return current_user
    
    def delete_user(self, user_id):
        """Delete a user"""
        logger.debug(f"Deleting user with ID: {user_id}")
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
