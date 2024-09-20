from flask import Flask, jsonify, request, abort, redirect, url_for
from uuid import uuid4
from threading import Thread
from crews import StockAnalysisCrew
from log_manager import append_event, outputs, outputs_lock, Event
from datetime import datetime
import json
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = 'your_secret_key'  # Set a secret key for session management

login_manager = LoginManager()
login_manager.init_app(app)

# In-memory "database" for storing users
users = {}

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

# Add a test user (In real apps, use a proper database)
users['admin'] = User(id='1', username='admin', password=generate_password_hash('admin', method='scrypt'))

# Load user callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.get_id() == user_id:
            return user
    return None

# Simple login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        abort(400, description="Missing username or password.")

    user = users.get(username)
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Logged in successfully!"}), 200
    else:
        abort(401, description="Invalid credentials.")

# Simple logout route
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200


def kickoff_crew(input_id, company_stock):
    print("Kicking off crew with input_id: ", input_id)
    results = None 
    try:
        crew = StockAnalysisCrew(input_id)
        crew.setup_crew(company_stock)
        results = crew.kickoff()
        print("Crew completed successfully")
    except Exception as e:
        print("Error when kicking off crew: ", e)
        append_event(input_id, f"Error when kicking off crew: {e}")
        with outputs_lock:
            outputs[input_id].status = "Error"
            outputs[input_id].error = str(e)

    with outputs_lock:
        outputs[input_id].status = "Completed"
        outputs[input_id].results = results
        outputs[input_id].events.append(Event(
            timestamp=datetime.now(),
            message="Crew has finished running."
        ))


@app.route('/api/multiagent', methods=['POST'])
def run_crew():
    data = request.get_json()
    company_stock = data['company_stock']
    input_id = str(uuid4())
    print("Received request to run crew with input_id: ", input_id)

    with outputs_lock:
        outputs[input_id] = Event(
            input_id=input_id,
            timestamp=datetime.now(),
            message="Crew has been set up, starting crew now."
        )

    thread = Thread(target=kickoff_crew, args=(input_id, company_stock))
    thread.start()

    return jsonify({"input_id": input_id}), 200

@app.route('/api/multiagent/<input_id>', methods=['GET'])
def get_status(input_id):
    with outputs_lock:
        if input_id not in outputs:
            return jsonify({"error": "Input ID not found"}), 404
        

    try:
        result =json.loads(outputs.results)
    except json.JSONDecodeError:
        result = outputs.results

    return jsonify({
        'input_id': input_id,
        "status": outputs[input_id].status,
        "results": result,
        "events": [event.to_dict() for event in outputs[input_id].events]
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=3001)