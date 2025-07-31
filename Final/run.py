#!/usr/bin/env python3
"""
CampusLink Application Runner
This script starts the CampusLink web application and optionally populates sample data.
"""

import os
import sys
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId

def populate_sample_data():
    """Populate the database with sample data for demonstration"""
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['campuslink']
        
        # Sample announcements
        announcements = [
            {
                "_id": ObjectId(),
                "title": "Mid-Semester Exams Schedule Released",
                "content": "The mid-semester examination schedule has been released. Please check your respective department notice boards for detailed timetables. Exams will commence from March 15th, 2024.",
                "category": "academic",
                "author": "Academic Office",
                "date": datetime.now() - timedelta(days=2),
                "priority": "high"
            },
            {
                "_id": ObjectId(),
                "title": "Annual Tech Fest - TechnoVision 2024",
                "content": "Get ready for the biggest tech event of the year! TechnoVision 2024 will feature hackathons, coding competitions, tech talks, and startup showcases. Registration opens soon.",
                "category": "events",
                "author": "Student Council",
                "date": datetime.now() - timedelta(days=1),
                "priority": "medium"
            },
            {
                "_id": ObjectId(),
                "title": "Library Extended Hours During Exams",
                "content": "The central library will remain open 24/7 during the examination period (March 10-25). Additional study spaces have been arranged in the conference halls.",
                "category": "facilities",
                "author": "Library Administration",
                "date": datetime.now(),
                "priority": "medium"
            }
        ]
        
        # Sample lost & found items
        lost_found_items = [
            {
                "_id": ObjectId(),
                "title": "Black Leather Wallet",
                "description": "Lost near the cafeteria. Contains student ID and some cash. Please contact if found.",
                "category": "personal",
                "type": "lost",
                "location": "Main Cafeteria",
                "contact": "john.doe@college.edu",
                "date": datetime.now() - timedelta(days=3),
                "status": "active"
            },
            {
                "_id": ObjectId(),
                "title": "iPhone 13 - Blue",
                "description": "Found in the computer lab. Has a cracked screen protector. Owner can contact to claim.",
                "category": "electronics",
                "type": "found",
                "location": "Computer Lab - Block A",
                "contact": "security@college.edu",
                "date": datetime.now() - timedelta(days=1),
                "status": "active"
            },
            {
                "_id": ObjectId(),
                "title": "Red Backpack with Books",
                "description": "Found in the library. Contains engineering textbooks and notebooks.",
                "category": "academic",
                "type": "found",
                "location": "Central Library",
                "contact": "library@college.edu",
                "date": datetime.now(),
                "status": "active"
            }
        ]
        
        # Sample complaints
        complaints = [
            {
                "_id": ObjectId(),
                "title": "Water Supply Issue in Hostel Block C",
                "description": "There has been no water supply in rooms 301-320 for the past two days. This is causing significant inconvenience to students.",
                "category": "water",
                "location": "Hostel Block C",
                "student_name": "Alice Johnson",
                "student_id": "CS2021001",
                "contact": "alice.johnson@college.edu",
                "date": datetime.now() - timedelta(days=2),
                "status": "in-progress",
                "priority": "high"
            },
            {
                "_id": ObjectId(),
                "title": "Broken WiFi in Study Hall",
                "description": "The WiFi connection in the main study hall has been unstable for the past week. Students are unable to access online resources.",
                "category": "internet",
                "location": "Main Study Hall",
                "student_name": "Bob Smith",
                "student_id": "EE2021045",
                "contact": "bob.smith@college.edu",
                "date": datetime.now() - timedelta(days=5),
                "status": "resolved",
                "priority": "medium"
            }
        ]
        
        # Sample skills
        skills = [
            {
                "_id": ObjectId(),
                "title": "Python Programming for Beginners",
                "description": "I can teach Python basics, data structures, and simple projects. Perfect for beginners who want to start their coding journey.",
                "category": "programming",
                "instructor": "Sarah Wilson",
                "contact": "sarah.wilson@college.edu",
                "duration": "2 hours",
                "price": "Free",
                "date": datetime.now() - timedelta(days=1),
                "status": "available"
            },
            {
                "_id": ObjectId(),
                "title": "Web Design with HTML/CSS",
                "description": "Learn to create beautiful, responsive websites from scratch. Covers HTML5, CSS3, and basic JavaScript.",
                "category": "design",
                "instructor": "Mike Chen",
                "contact": "mike.chen@college.edu",
                "duration": "3 hours",
                "price": "₹500",
                "date": datetime.now(),
                "status": "available"
            }
        ]
        
        # Sample news
        news_items = [
            {
                "_id": ObjectId(),
                "title": "Google Summer of Code 2024 Applications Open",
                "content": "Google Summer of Code is now accepting applications for 2024. This is a great opportunity for students to contribute to open source projects and gain valuable experience.",
                "category": "internships",
                "author": "Tech News Team",
                "url": "https://summerofcode.withgoogle.com/",
                "date": datetime.now() - timedelta(days=1)
            },
            {
                "_id": ObjectId(),
                "title": "Microsoft Imagine Cup 2024 - Register Now",
                "content": "The world's premier student technology competition is back! Build innovative solutions using Microsoft technologies and compete for prizes worth $100,000.",
                "category": "hackathons",
                "author": "Tech News Team",
                "url": "https://imaginecup.microsoft.com/",
                "date": datetime.now()
            }
        ]
        
        # Sample polls
        polls = [
            {
                "_id": ObjectId(),
                "question": "Should the college implement a hybrid learning model?",
                "options": ["Yes, hybrid is better", "No, prefer offline only", "No, prefer online only", "Need more information"],
                "votes": {"Yes, hybrid is better": 45, "No, prefer offline only": 23, "No, prefer online only": 12, "Need more information": 8},
                "author": "Student Council",
                "date": datetime.now() - timedelta(days=3),
                "status": "active"
            },
            {
                "_id": ObjectId(),
                "question": "What time should the library close on weekdays?",
                "options": ["10 PM", "11 PM", "12 AM", "24/7"],
                "votes": {"10 PM": 15, "11 PM": 32, "12 AM": 28, "24/7": 41},
                "author": "Library Committee",
                "date": datetime.now() - timedelta(days=1),
                "status": "active"
            }
        ]
        
        # Insert sample data
        collections_data = [
            (db['announcements'], announcements),
            (db['lost_found'], lost_found_items),
            (db['complaints'], complaints),
            (db['skills'], skills),
            (db['news'], news_items),
            (db['polls'], polls)
        ]
        
        for collection, data in collections_data:
            # Clear existing data
            collection.delete_many({})
            # Insert new sample data
            if data:
                collection.insert_many(data)
                print(f"✓ Inserted {len(data)} sample records into {collection.name}")
        
        print("\n🎉 Sample data populated successfully!")
        print("You can now explore the application with realistic data.")
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")

def main():
    """Main function to run the application"""
    print("🚀 Starting CampusLink Application...")
    print("=" * 50)
    
    # Check if MongoDB is running
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✓ MongoDB connection successful")
    except Exception as e:
        print("❌ MongoDB connection failed!")
        print("Please make sure MongoDB is installed and running.")
        print("Visit: https://docs.mongodb.com/manual/installation/")
        return
    
    # Ask user if they want to populate sample data
    if len(sys.argv) > 1 and sys.argv[1] == '--sample-data':
        populate_sample_data()
        print()
    
    # Import and run the Flask app
    try:
        from app import app
        print("✓ Flask application loaded")
        print("\n🌐 Application URLs:")
        print("   • Main Site: http://localhost:5000")
        print("   • Dashboard: http://localhost:5000/dashboard")
        print("   • Login: http://localhost:5000/login")
        print("\n📝 Demo Login Credentials:")
        print("   • Student: Any email + any password")
        print("   • Admin: Any email + any password (will be set as admin)")
        print("\n⚡ Starting server...")
        print("=" * 50)
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return

if __name__ == "__main__":
    main()