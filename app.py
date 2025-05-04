from flask import Flask, render_template, request, jsonify
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_login import login_required
from models import db, User
from auth import auth
# Load your existing agent setup
from agent_setup import agent_executor  # Your existing agent code

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth)

# Create tables
with app.app_context():
    db.create_all()
# Mock user session storage
user_sessions = {}

@app.route('/')
@login_required
def home():
    return render_template('index.html')

async def async_chat_handler(user_id, message):
    """Handle async operations separately"""
    # Initialize session if new user
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'chat_history': [],
            'bookings': []
        }
    
    try:
        # Run the agent
        result = await agent_executor.ainvoke({
            "input": message,
            "chat_history": user_sessions[user_id]['chat_history']
        })
        
        # Store conversation
        user_sessions[user_id]['chat_history'].extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": result['output']}
        ])
        
        # Detect and store bookings
        if "booking confirmed" in result['output'].lower():
            booking_id = f"IRCTC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            user_sessions[user_id]['bookings'].append({
                "id": booking_id,
                "details": result['output'],
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "response": result['output'],
            "bookings": user_sessions[user_id]['bookings']
        }
    
    except Exception as e:
        return {"error": str(e)}

@app.route('/chat', methods=['POST'])
async def chat():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    message = data.get('message', '')
    return jsonify(await async_chat_handler(user_id, message))

if __name__ == '__main__':
    app.run(debug=True)