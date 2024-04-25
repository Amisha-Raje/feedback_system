from pymongo import MongoClient
from hashlib import sha256

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']  # Replace 'mydatabase' with your database name
users_collection = db['users']  # Collection for storing user data
feedback_collection = db['feedback']  # Collection for storing feedback data

# Function to register a new user
def register_user(username, password):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        return False, "Username already exists"
    
    # Hash the password before storing it in the database
    hashed_password = sha256(password.encode()).hexdigest()
    
    # Insert the user data into the database
    users_collection.insert_one({"username": username, "password": hashed_password})
    return True, "User registered successfully"

# Function to authenticate a user
def authenticate_user(username, password):
    # Retrieve the user data from the database
    user_data = users_collection.find_one({"username": username})
    
    # If user data is found
    if user_data:
        # Hash the input password and compare it with the stored hashed password
        if user_data['password'] == sha256(password.encode()).hexdigest():
            return True, "Authentication successful"
        else:
            return False, "Incorrect password"
    else:
        return False, "User not found"

# Function to submit feedback
def submit_feedback(username, feedback_text):
    feedback_collection.insert_one({"username": username, "feedback": feedback_text})
    return True, "Feedback submitted successfully"

# Example usage
# Register a new user
register_status, message = register_user("john_doe", "password123")
print(message)

# Authenticate the user
auth_status, message = authenticate_user("john_doe", "#########")
print(message)

# Submit feedback
feedback_status, message = submit_feedback("john_doe", "This is a test feedback.")
print(message)
