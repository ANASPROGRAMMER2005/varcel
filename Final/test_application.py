#!/usr/bin/env python3
"""
Comprehensive Application Testing Script
Tests all API endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

def test_endpoint(method, endpoint, data=None, description=""):
    """Test a single API endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == 'PUT':
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print(f"✅ {method} {endpoint} - {description}")
            return True, response.json()
        else:
            print(f"❌ {method} {endpoint} - {description} (Status: {response.status_code})")
            return False, None
            
    except Exception as e:
        print(f"❌ {method} {endpoint} - {description} (Error: {e})")
        return False, None

def main():
    """Run comprehensive tests"""
    print("🧪 CampusLink Application Testing")
    print("=" * 50)
    
    # Test basic pages
    print("\n📄 Testing Page Routes:")
    pages = [
        ('/', 'Home page'),
        ('/login', 'Login page'),
        ('/dashboard', 'Dashboard'),
        ('/announcements', 'Announcements'),
        ('/lost-found', 'Lost & Found'),
        ('/timetable', 'Timetable'),
        ('/complaints', 'Complaints'),
        ('/skills', 'Skills'),
        ('/news', 'News'),
        ('/polls', 'Polls')
    ]
    
    for endpoint, description in pages:
        test_endpoint('GET', endpoint, description=description)
    
    # Test API endpoints
    print("\n🔌 Testing API Endpoints:")
    
    # Test Announcements API
    success, data = test_endpoint('GET', '/api/announcements', description="Get announcements")
    
    # Test adding announcement
    announcement_data = {
        'title': 'Test Announcement',
        'content': 'This is a test announcement',
        'category': 'general',
        'author': 'Test Admin'
    }
    test_endpoint('POST', '/api/announcements', announcement_data, "Add announcement")
    
    # Test Lost & Found API
    test_endpoint('GET', '/api/lost-found', description="Get lost & found items")
    
    lost_item_data = {
        'title': 'Test Lost Item',
        'description': 'Test description',
        'category': 'personal',
        'type': 'lost',
        'location': 'Test Location',
        'contact': 'test@example.com'
    }
    test_endpoint('POST', '/api/lost-found', lost_item_data, "Add lost item")
    
    # Test Timetable API
    test_endpoint('GET', '/api/timetable?user_id=default', description="Get timetable")
    
    timetable_data = {
        'user_id': 'default',
        'schedule': [{
            'day': 'Monday',
            'time': '09:00',
            'subject': 'Test Subject',
            'room': 'Room 101',
            'professor': 'Test Professor'
        }]
    }
    test_endpoint('POST', '/api/timetable', timetable_data, "Save timetable")
    
    # Test Complaints API
    test_endpoint('GET', '/api/complaints', description="Get complaints")
    
    complaint_data = {
        'title': 'Test Complaint',
        'description': 'Test complaint description',
        'category': 'maintenance',
        'room_number': '101',
        'student_name': 'Test Student',
        'contact': 'test@example.com'
    }
    test_endpoint('POST', '/api/complaints', complaint_data, "Add complaint")
    
    # Test Skills API
    test_endpoint('GET', '/api/skills', description="Get skills")
    
    skill_data = {
        'title': 'Test Skill',
        'description': 'Test skill description',
        'category': 'programming',
        'instructor': 'Test Instructor',
        'contact': 'test@example.com',
        'duration': '2 hours',
        'price': 'Free'
    }
    test_endpoint('POST', '/api/skills', skill_data, "Add skill")
    
    # Test News API
    test_endpoint('GET', '/api/news', description="Get news")
    
    news_data = {
        'title': 'Test News',
        'content': 'Test news content',
        'category': 'general',
        'author': 'Test Author',
        'url': 'https://example.com'
    }
    test_endpoint('POST', '/api/news', news_data, "Add news")
    
    # Test Polls API
    test_endpoint('GET', '/api/polls', description="Get polls")
    
    poll_data = {
        'question': 'Test Poll Question?',
        'options': ['Option 1', 'Option 2', 'Option 3'],
        'author': 'Test Admin'
    }
    test_endpoint('POST', '/api/polls', poll_data, "Add poll")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("Check the results above for any failed tests.")

if __name__ == "__main__":
    main()