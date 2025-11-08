from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# Database setup
DATABASE = 'forum.db'

def get_db():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT NOT NULL,
            upvotes INTEGER DEFAULT 0,
            downvotes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    
    # Check if posts table is empty and add sample posts
    cursor.execute('SELECT COUNT(*) as count FROM posts')
    if cursor.fetchone()['count'] == 0:
        sample_posts = [
            (
                '@CyberGuardian',
                'Critical Vulnerability Found in Major SSL Library',
                'Researchers have discovered a critical vulnerability in OpenSSL that could affect millions of websites worldwide. The flaw, designated as CVE-2024-XXXX, allows attackers to bypass encryption protocols...',
                json.dumps(['#OpenSSL', '#Vulnerability', '#Security']),
                159,
                14
            ),
            (
                '@SecureNet',
                'New Zero-Day Exploit Found in Quantum Encryption',
                'A new zero-day exploit targeting quantum encryption breakthroughs has been identified. Experts are scrambling to patch the vulnerability before it can be widely used by malicious actors...',
                json.dumps(['#ZeroDay', '#Quantum', '#Exploit']),
                102,
                9
            )
        ]
        
        cursor.executemany('''
            INSERT INTO posts (author, title, content, tags, upvotes, downvotes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_posts)
    
    conn.commit()
    conn.close()

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to perform this action.', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def get_all_posts():
    """Fetch all posts from database"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    posts = []
    for row in rows:
        posts.append({
            'id': row['id'],
            'author': row['author'],
            'title': row['title'],
            'content': row['content'],
            'tags': json.loads(row['tags']),
            'upvotes': row['upvotes'],
            'downvotes': row['downvotes'],
            'timestamp': format_timestamp(row['created_at'])
        })
    
    return posts

def get_post_by_id(post_id):
    """Fetch a single post by ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row['id'],
            'author': row['author'],
            'title': row['title'],
            'content': row['content'],
            'tags': json.loads(row['tags']),
            'upvotes': row['upvotes'],
            'downvotes': row['downvotes'],
            'timestamp': format_timestamp(row['created_at'])
        }
    return None

def get_comments_for_post(post_id):
    """Fetch all comments for a specific post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC', (post_id,))
    rows = cursor.fetchall()
    conn.close()
    
    comments = []
    for row in rows:
        comments.append({
            'id': row['id'],
            'author': row['author'],
            'content': row['content'],
            'timestamp': format_timestamp(row['created_at'])
        })
    
    return comments

def add_comment(post_id, author, content):
    """Add a new comment to a post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comments (post_id, author, content)
        VALUES (?, ?, ?)
    ''', (post_id, author, content))
    conn.commit()
    conn.close()

def format_timestamp(timestamp):
    """Format timestamp to relative time"""
    try:
        post_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = now - post_time
        
        if diff.days > 0:
            if diff.days == 1:
                return '1 day ago'
            elif diff.days < 30:
                return f'{diff.days} days ago'
            else:
                return post_time.strftime('%b %d, %Y')
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f'{hours} hour{"s" if hours > 1 else ""} ago'
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
        else:
            return 'Just now'
    except:
        return timestamp

def add_post(author, title, content, tags):
    """Add a new post to database"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO posts (author, title, content, tags, upvotes, downvotes)
        VALUES (?, ?, ?, ?, 0, 0)
    ''', (author, title, content, json.dumps(tags)))
    
    conn.commit()
    conn.close()

def create_user(username, password):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def verify_user(username, password):
    """Verify user credentials"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Initialize database when app starts
with app.app_context():
    init_db()

@app.route('/')
def home():
    return redirect(url_for('posts_page'))

@app.route('/posts')
def posts_page():
    posts = get_all_posts()
    return render_template('posts.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('posts_page'))
    
    comments = get_comments_for_post(post_id)
    return render_template('view_post.html', post=post, comments=comments)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment_to_post(post_id):
    content = request.form.get('content')
    if content and content.strip():
        author = f"@{session['username']}"
        add_comment(post_id, author, content.strip())
        flash('Comment added successfully!', 'success')
    else:
        flash('Comment cannot be empty.', 'error')
    
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/create')
def create_page():
    return render_template('create.html')

@app.route('/create-post', methods=['POST'])
def create_post():
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')
    tags_input = request.form.get('tags', '')
    
    # Process tags
    tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    if not tags:
        tags = ['#General']
    
    # Add @ to author if not present
    if not author.startswith('@'):
        author = f'@{author}'
    
    # Save to database
    add_post(author, title, content, tags)
    
    flash('Post created successfully!', 'success')
    return redirect(url_for('posts_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_user(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('posts_page'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        elif create_user(username, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Username already exists.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('posts_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)