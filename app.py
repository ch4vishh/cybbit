from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for posts (will reset when server restarts)
posts = [
    {
        'id': 1,
        'author': '@CyberGuardian',
        'title': 'Critical Vulnerability Found in Major SSL Library',
        'content': 'Researchers have discovered a critical vulnerability in OpenSSL that could affect millions of websites worldwide. The flaw, designated as CVE-2024-XXXX, allows attackers to bypass encryption protocols...',
        'tags': ['#OpenSSL', '#Vulnerability', '#Security'],
        'upvotes': 159,
        'downvotes': 14,
        'timestamp': '2 hours ago'
    },
    {
        'id': 2,
        'author': '@SecureNet',
        'title': 'New Zero-Day Exploit Found in Quantum Encryption',
        'content': 'A new zero-day exploit targeting quantum encryption breakthroughs has been identified. Experts are scrambling to patch the vulnerability before it can be widely used by malicious actors...',
        'tags': ['#ZeroDay', '#Quantum', '#Exploit'],
        'upvotes': 102,
        'downvotes': 9,
        'timestamp': '5 hours ago'
    }
]

@app.route('/')
def home():
    return redirect(url_for('posts_page'))

@app.route('/posts')
def posts_page():
    return render_template('posts.html', posts=posts)

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
    
    # Create new post
    new_post = {
        'id': len(posts) + 1,
        'author': author if author.startswith('@') else f'@{author}',
        'title': title,
        'content': content,
        'tags': tags,
        'upvotes': 0,
        'downvotes': 0,
        'timestamp': 'Just now'
    }
    
    posts.insert(0, new_post)
    
    return redirect(url_for('posts_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)