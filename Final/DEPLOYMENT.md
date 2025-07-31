# CampusLink Deployment Guide

## Quick Start (Windows)

1. **Double-click `start.bat`** - This will automatically:
   - Check Python installation
   - Install required packages
   - Ask if you want sample data
   - Start the application

2. **Open your browser** and go to:
   - **Main Site**: http://localhost:5000
   - **Dashboard**: http://localhost:5000/dashboard

## Manual Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)

### Installation Steps

1. **Clone/Download the project**
   ```bash
   cd CampusLink
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-cors pymongo
   ```

3. **Start MongoDB**
   - **Windows**: Start MongoDB service
   - **macOS/Linux**: `sudo systemctl start mongod`

4. **Run the application**
   ```bash
   # With sample data
   python run.py --sample-data
   
   # Without sample data
   python run.py
   ```

## Configuration

### MongoDB Configuration
- **Local MongoDB**: Default connection to `mongodb://localhost:27017/`
- **MongoDB Atlas**: Update connection string in `app.py`

### Firebase Configuration (Optional)
1. Create a Firebase project
2. Download service account credentials
3. Update the path in `app.py`:
   ```python
   cred = credentials.Certificate("path/to/your/firebase-credentials.json")
   firebase_admin.initialize_app(cred)
   ```

## Demo Credentials

The application runs in demo mode by default:
- **Any email + any password** = Student access
- **Admin features** are available through the interface

## Features Available

### ✅ Core Features
1. **Campus Announcements** - View and manage campus updates
2. **Lost & Found** - Report and search for lost items
3. **Timetable Scheduler** - Manage class schedules
4. **Hostel Complaints** - File and track complaints
5. **User Authentication** - Role-based access control

### ✅ Additional Features
6. **Skill Exchange** - Peer learning marketplace
7. **Tech News & Opportunities** - Hackathons, internships, tech news
8. **Polls & Feedback** - Campus polls and feedback collection

## API Endpoints

### Announcements
- `GET /api/announcements` - Get all announcements
- `POST /api/announcements` - Create announcement (admin)

### Lost & Found
- `GET /api/lost-found` - Get all items
- `POST /api/lost-found` - Report new item

### Timetable
- `GET /api/timetable?user_id=<id>` - Get user timetable
- `POST /api/timetable` - Add/update timetable entry

### Complaints
- `GET /api/complaints` - Get all complaints
- `POST /api/complaints` - File new complaint
- `PUT /api/complaints` - Update complaint status (admin)

### Skills
- `GET /api/skills` - Get all skills
- `POST /api/skills` - Offer new skill

### News
- `GET /api/news` - Get all news
- `POST /api/news` - Add news (admin)

### Polls
- `GET /api/polls` - Get all polls
- `POST /api/polls` - Create poll (admin)
- `PUT /api/polls` - Vote on poll

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check connection string
   - Verify network connectivity

2. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill existing processes using port 5000

3. **Module Not Found Error**
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

4. **Static Files Not Loading**
   - Check file paths in templates
   - Ensure static folder structure is correct

### Performance Tips

1. **Database Indexing**
   ```javascript
   // In MongoDB shell
   db.announcements.createIndex({"date": -1})
   db.lost_found.createIndex({"category": 1, "status": 1})
   db.complaints.createIndex({"status": 1, "date": -1})
   ```

2. **Caching**
   - Enable Flask caching for static content
   - Use CDN for production deployment

## Production Deployment

### Using Gunicorn (Linux/macOS)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export MONGODB_URI=your-mongodb-connection-string
```

## Security Considerations

1. **Change default secret key** in production
2. **Use HTTPS** for production deployment
3. **Implement rate limiting** for API endpoints
4. **Validate and sanitize** all user inputs
5. **Use environment variables** for sensitive data

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the README.md file
3. Check application logs for error details

---

**CampusLink** - Making campus life easier, one feature at a time! 🎓✨