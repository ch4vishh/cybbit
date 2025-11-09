# Cybbit - Cybersecurity Discussion Forum

A full-stack web application built with Flask for cybersecurity enthusiasts to discuss vulnerabilities, exploits, and security topics.

## Features

### Authentication System
- **Multi-step Registration**: 3-step process with username validation, email verification (4-digit code), and password creation
- **2FA Email Verification**: Time-limited (10 minutes) verification codes sent via SMTP
- **Flexible Login**: Accepts both username and email with intelligent error handling
- **Session Management**: Secure Flask sessions for user authentication

### Core Functionality
- **Posts**: Create, view, and browse cybersecurity discussions with tags, upvotes/downvotes
- **Comments**: Login-required commenting system with threaded discussions
- **Real-time Timestamps**: Dynamic "X hours ago" formatting
- **Responsive UI**: Dark-themed interface matching cybersecurity aesthetics

## Tech Stack

**Backend**: Python Flask, SQLite3  
**Frontend**: HTML5, CSS3, Jinja2 templating  
**Database**: SQLite with 4 tables (users, posts, comments, verification_codes)  
**Email**: SMTP with MIMEMultipart for HTML emails  
**Security**: Session-based auth, login decorators, SQL injection protection via parameterized queries

## Database Schema
- Users: username (unique), email (unique), password, timestamps
- Posts: author, title, content, JSON tags, vote counts
- Comments: post_id (FK), author, content, timestamps
- Verification_codes: email, code, expiry, used status

## Installation
```bash
pip install flask
python app.py
```

Access at `http://localhost:5000`

## Configuration
Update email credentials in `app.py`:
```python
EMAIL_ADDRESS = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-app-password'
```

## File Structure
```
project/
├── app.py              # Main Flask application
├── forum.db            # SQLite database (auto-generated)
├── templates/
│   ├── posts.html
│   ├── view_post.html
│   ├── create.html
│   ├── login.html
│   └── register.html
└── static/
    └── css/
        └── style.css   # Complete styling
```

Built with security and user experience in mind!