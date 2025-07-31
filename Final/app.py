from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
# Optional Firebase import
try:
    import firebase_admin
    from firebase_admin import credentials, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Firebase not available - running in demo mode")
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
import json
from bson import ObjectId
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app)

# MongoDB Configuration
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['campuslink']
    
    # Collections
    announcements_collection = db['announcements']
    lost_found_collection = db['lost_found']
    timetables_collection = db['timetables']
    complaints_collection = db['complaints']
    users_collection = db['users']
    skills_collection = db['skills']
    news_collection = db['news']
    polls_collection = db['polls']
    
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")

# Firebase Configuration (Optional)
if FIREBASE_AVAILABLE:
    try:
        # Uncomment and configure when you have Firebase credentials
        # cred = credentials.Certificate("path/to/your/firebase-credentials.json")
        # firebase_admin.initialize_app(cred)
        print("Firebase configuration ready (but not initialized)")
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        FIREBASE_AVAILABLE = False

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/announcements')
def announcements():
    return render_template('announcements.html')

@app.route('/lost-found')
def lost_found():
    return render_template('lost_found.html')

@app.route('/timetable')
def timetable():
    return render_template('timetable.html')

@app.route('/complaints')
def complaints():
    return render_template('complaints.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/polls')
def polls():
    return render_template('polls.html')

# API Routes

# Announcements API
@app.route('/api/announcements', methods=['GET', 'POST'])
def api_announcements():
    if request.method == 'GET':
        category = request.args.get('category', '')
        query = {}
        if category:
            query['category'] = category
        
        announcements = list(announcements_collection.find(query).sort('date', -1))
        return jsonify(json.loads(json.dumps(announcements, default=json_serial)))
    
    elif request.method == 'POST':
        data = request.json
        announcement = {
            'title': data['title'],
            'content': data['content'],
            'category': data['category'],
            'date': datetime.now(),
            'author': data.get('author', 'Admin')
        }
        result = announcements_collection.insert_one(announcement)
        return jsonify({'success': True, 'id': str(result.inserted_id)})

# Lost & Found API
@app.route('/api/lost-found', methods=['GET', 'POST'])
def api_lost_found():
    if request.method == 'GET':
        category = request.args.get('category', '')
        type_filter = request.args.get('type', '')  # 'lost' or 'found'
        
        query = {}
        if category:
            query['category'] = category
        if type_filter:
            query['type'] = type_filter
            
        items = list(lost_found_collection.find(query).sort('date', -1))
        return jsonify(json.loads(json.dumps(items, default=json_serial)))
    
    elif request.method == 'POST':
        data = request.json
        item = {
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'type': data['type'],  # 'lost' or 'found'
            'location': data['location'],
            'contact': data['contact'],
            'date': datetime.now(),
            'status': 'active'
        }
        result = lost_found_collection.insert_one(item)
        return jsonify({'success': True, 'id': str(result.inserted_id)})

# Timetable API
@app.route('/api/timetable', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_timetable():
    if request.method == 'GET':
        user_id = request.args.get('user_id', 'default')
        timetable = timetables_collection.find_one({'user_id': user_id})
        if timetable:
            return jsonify(json.loads(json.dumps(timetable, default=json_serial)))
        return jsonify({'schedule': []})
    
    elif request.method == 'POST':
        data = request.json
        user_id = data.get('user_id', 'default')
        
        # If schedule data is provided, replace the entire schedule
        if 'schedule' in data:
            timetable_doc = {
                'user_id': user_id,
                'schedule': data['schedule'],
                'updated_at': datetime.now()
            }
            timetables_collection.replace_one(
                {'user_id': user_id},
                timetable_doc,
                upsert=True
            )
        else:
            # Add single schedule item (legacy support)
            schedule_item = {
                'day': data['day'],
                'time': data['time'],
                'subject': data['subject'],
                'room': data['room'],
                'professor': data.get('professor', ''),
                'duration': data.get('duration', '60'),
                'notes': data.get('notes', ''),
                'created_at': datetime.now()
            }
            
            timetables_collection.update_one(
                {'user_id': user_id},
                {'$push': {'schedule': schedule_item}},
                upsert=True
            )
        
        return jsonify({'success': True})

# Complaints API
@app.route('/api/complaints', methods=['GET', 'POST', 'PUT'])
def api_complaints():
    if request.method == 'GET':
        complaints = list(complaints_collection.find().sort('date', -1))
        return jsonify(json.loads(json.dumps(complaints, default=json_serial)))
    
    elif request.method == 'POST':
        data = request.json
        complaint = {
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'room_number': data.get('room_number', ''),
            'priority': data.get('priority', 'medium'),
            'status': 'pending',
            'date': datetime.now(),
            'student_name': data.get('student_name', ''),
            'contact': data.get('contact', '')
        }
        result = complaints_collection.insert_one(complaint)
        return jsonify({'success': True, 'id': str(result.inserted_id)})
    
    elif request.method == 'PUT':
        data = request.json
        complaint_id = data['id']
        new_status = data['status']
        
        complaints_collection.update_one(
            {'_id': ObjectId(complaint_id)},
            {'$set': {'status': new_status, 'updated_at': datetime.now()}}
        )
        return jsonify({'success': True})

# Skills API
@app.route('/api/skills', methods=['GET', 'POST'])
def api_skills():
    if request.method == 'GET':
        skills = list(skills_collection.find().sort('date', -1))
        return jsonify(json.loads(json.dumps(skills, default=json_serial)))
    
    elif request.method == 'POST':
        data = request.json
        skill = {
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'instructor': data['instructor'],
            'contact': data['contact'],
            'duration': data.get('duration', '1 hour'),
            'price': data.get('price', 'Free'),
            'date': datetime.now(),
            'status': 'available'
        }
        result = skills_collection.insert_one(skill)
        return jsonify({'success': True, 'id': str(result.inserted_id)})

# News API
@app.route('/api/news', methods=['GET', 'POST'])
def api_news():
    if request.method == 'GET':
        news = list(news_collection.find().sort('date', -1))
        return jsonify(json.loads(json.dumps(news, default=json_serial)))
    
    elif request.method == 'POST':
        data = request.json
        news_item = {
            'title': data['title'],
            'content': data['content'],
            'category': data['category'],
            'url': data.get('url', ''),
            'date': datetime.now(),
            'author': data.get('author', 'Admin')
        }
        result = news_collection.insert_one(news_item)
        return jsonify({'success': True, 'id': str(result.inserted_id)})

# Polls API
@app.route('/api/polls', methods=['GET', 'POST', 'PUT'])
def api_polls():
    if request.method == 'GET':
        polls = list(polls_collection.find().sort('date', -1))
        return jsonify(json.loads(json.dumps(polls, default=json_serial)))
    
    elif request.method == 'POST':
        data = request.json
        poll = {
            'question': data['question'],
            'options': data['options'],
            'votes': {option: 0 for option in data['options']},
            'voters': [],
            'date': datetime.now(),
            'status': 'active',
            'author': data.get('author', 'Admin')
        }
        result = polls_collection.insert_one(poll)
        return jsonify({'success': True, 'id': str(result.inserted_id)})
    
    elif request.method == 'PUT':
        data = request.json
        poll_id = data['poll_id']
        selected_option = data['option']
        voter_id = data.get('voter_id', 'anonymous')
        
        # Check if user already voted
        poll = polls_collection.find_one({'_id': ObjectId(poll_id)})
        if voter_id not in poll.get('voters', []):
            polls_collection.update_one(
                {'_id': ObjectId(poll_id)},
                {
                    '$inc': {f'votes.{selected_option}': 1},
                    '$push': {'voters': voter_id}
                }
            )
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Already voted'})

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)