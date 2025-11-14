from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


app = Flask(__name__, static_folder='.', template_folder='.')



def create_sample_data():
    """Create extensive cybersecurity news data for testing"""
    
    # 40 Real cybersecurity news articles with full content
    posts_data = {
        'post_id': list(range(1, 41)),
        'title': [
            'Critical Zero-Day Vulnerability in Apache Log4j Exploited Worldwide',
            'Ransomware Gang Demands $50M from Major Healthcare Network',
            'Microsoft Releases Emergency Patch for Windows Print Spooler',
            'Massive DDoS Attack Takes Down Multiple Banking Websites',
            'AI-Powered Phishing Campaigns Bypass Traditional Email Filters',
            'SQL Injection Flaw Discovered in WordPress Plugin with 2M+ Installs',
            'Chinese APT Group Targets Government Agencies in Supply Chain Attack',
            'Cryptocurrency Exchange Loses $80M in Smart Contract Exploit',
            'New Malware Variant Uses Rootkit to Evade Antivirus Detection',
            'Data Breach at Major Retailer Exposes 5 Million Customer Records',
            'Critical Vulnerability Found in Cisco Network Equipment',
            'North Korean Hackers Launch Campaign Against Aerospace Companies',
            'Vulnerability in Popular VPN Software Allows Man-in-the-Middle Attacks',
            'Ransomware Attack Forces Major Pipeline to Shut Down Operations',
            'Hackers Exploit Zero-Day in Chrome Browser for Targeted Attacks',
            'New Botnet Discovered with Over 100,000 Infected IoT Devices',
            'Financial Institution Hit by Sophisticated Social Engineering Attack',
            'Critical Security Flaw in Linux Kernel Affects Millions of Servers',
            'Malicious npm Package Downloaded 50,000 Times Before Detection',
            'Russian Hackers Target Energy Infrastructure with Custom Malware',
            'Major Cloud Provider Suffers Data Exposure Due to Misconfiguration',
            'Phishing Campaign Impersonates Tax Authority to Steal Credentials',
            'New Android Malware Steals Banking Credentials from 200+ Apps',
            'Critical Vulnerability Patched in VMware vCenter Server',
            'Cybercriminals Use Deepfake Audio to Authorize Fraudulent Transfers',
            'Insider Threat Leads to Massive Data Exfiltration at Tech Company',
            'Hackers Exploit Vulnerability in Remote Desktop Protocol',
            'New Ransomware Strain Targets Industrial Control Systems',
            'Bug Bounty Hunter Discovers Critical Flaw in Social Media Platform',
            'State-Sponsored Actors Deploy Advanced Persistent Threat Framework',
            'Zero-Day Exploit in PDF Readers Used in Targeted Attacks',
            'Cryptojacking Malware Infects Thousands of Corporate Servers',
            'Major Telecom Provider Hit by Sophisticated APT Campaign',
            'New Phishing Kit Mimics Multi-Factor Authentication Pages',
            'Critical Vulnerability Discovered in Popular CMS Platform',
            'Hackers Breach Hospital System, Steal Patient Medical Records',
            'Supply Chain Attack Compromises Software Development Tools',
            'New Spyware Targets Journalists and Human Rights Activists',
            'Critical Flaw in IoT Firmware Affects Millions of Smart Devices',
            'Ransomware Group Leaks Stolen Data After Failed Negotiations'
        ],
        'content': [
            'A critical remote code execution vulnerability (CVE-2021-44228) has been discovered in Apache Log4j, a widely-used Java logging library. Security researchers warn that attackers are actively exploiting this flaw to gain unauthorized access to vulnerable systems worldwide. Organizations are urged to apply patches immediately as the vulnerability is trivial to exploit.',
            'A notorious ransomware group has encrypted critical systems at a major healthcare network, demanding a ransom of $50 million. The attack has disrupted patient care services across multiple hospitals, forcing staff to revert to manual processes. FBI and CISA are investigating the incident.',
            'Microsoft has released an emergency security update addressing multiple critical vulnerabilities in the Windows Print Spooler service. These flaws could allow attackers to execute arbitrary code with SYSTEM privileges. Security experts recommend immediate deployment of the patch.',
            'A coordinated distributed denial-of-service (DDoS) attack has disrupted online banking services for several major financial institutions. The attack peaked at 2.3 Tbps, making it one of the largest recorded DDoS attacks. Customers experienced intermittent service outages for several hours.',
            'Cybercriminals are leveraging artificial intelligence to create highly sophisticated phishing emails that successfully bypass traditional email security filters. These AI-generated messages exhibit perfect grammar, context-aware content, and convincing spoofed sender addresses.',
            'Security researchers have identified a critical SQL injection vulnerability in a popular WordPress plugin installed on over 2 million websites. The flaw allows unauthenticated attackers to extract sensitive database information. A patch has been released and users are urged to update immediately.',
            'A Chinese advanced persistent threat (APT) group has compromised multiple government agencies through a sophisticated supply chain attack. The attackers gained access by compromising a trusted software vendor and injecting malicious code into legitimate software updates.',
            'A major cryptocurrency exchange has suffered a devastating smart contract exploit resulting in the theft of $80 million worth of digital assets. The vulnerability in the exchange\'s DeFi protocol allowed attackers to manipulate token pricing mechanisms.',
            'Cybersecurity researchers have discovered a new malware variant that employs rootkit techniques to operate at the kernel level, making it virtually invisible to traditional antivirus solutions. The malware has been observed in targeted attacks against enterprise networks.',
            'A massive data breach at a major retail chain has exposed personal information of approximately 5 million customers, including names, addresses, email addresses, and encrypted payment card data. The breach occurred through compromised point-of-sale systems.',
            'Cisco has disclosed a critical vulnerability in its network equipment that could allow remote attackers to execute arbitrary code and take complete control of affected devices. The vulnerability affects multiple product lines and emergency patches are being deployed.',
            'North Korean state-sponsored hackers have launched a widespread campaign targeting aerospace and defense companies. The operation aims to steal sensitive intellectual property related to military technology and satellite systems.',
            'A serious vulnerability has been discovered in a widely-used VPN software that could enable man-in-the-middle attacks. The flaw allows attackers to intercept and decrypt VPN traffic, potentially exposing sensitive communications.',
            'A ransomware attack has forced a major fuel pipeline operator to shut down operations, leading to fuel shortages and price increases across multiple states. The attack demonstrates the vulnerability of critical infrastructure to cyber threats.',
            'Google has released an emergency security update for Chrome browser after discovering active exploitation of a zero-day vulnerability. The flaw could allow attackers to execute arbitrary code through specially crafted web pages.',
            'Security researchers have identified a massive botnet consisting of over 100,000 compromised IoT devices including cameras, routers, and smart home devices. The botnet is being used to launch DDoS attacks and distribute malware.',
            'A major financial institution fell victim to a sophisticated social engineering attack where attackers posed as IT support staff to gain employee credentials. The breach resulted in unauthorized access to customer accounts and financial data.',
            'A critical security vulnerability has been patched in the Linux kernel that could allow local privilege escalation. The flaw affects millions of Linux servers worldwide and poses significant security risks.',
            'A malicious package was discovered in the npm repository that had been downloaded over 50,000 times before detection. The package contained code designed to steal environment variables and cryptocurrency wallet credentials from developer machines.',
            'Russian state-sponsored threat actors have deployed custom malware targeting energy sector infrastructure. The malware is designed to provide persistent access and potentially disrupt operations of power generation and distribution systems.',
            'A major cloud service provider has disclosed that customer data was inadvertently exposed due to misconfigured storage buckets. The exposure lasted for several weeks before being discovered during a security audit.',
            'A sophisticated phishing campaign is impersonating government tax authorities to steal login credentials and personal information. The campaign uses convincing fake websites and urgent messaging to pressure victims into providing sensitive data.',
            'A new Android banking trojan has been discovered that can steal credentials from over 200 banking and cryptocurrency applications. The malware uses overlay attacks and keylogging to capture sensitive information.',
            'VMware has released critical security patches for vCenter Server addressing multiple vulnerabilities including remote code execution flaws. Organizations using VMware infrastructure are urged to apply updates immediately.',
            'Cybercriminals have successfully used deepfake audio technology to impersonate a company CEO and authorize fraudulent wire transfers totaling millions of dollars. This represents a new frontier in social engineering attacks.',
            'An insider threat at a major technology company resulted in the exfiltration of terabytes of sensitive data including source code, customer information, and trade secrets. The incident highlights the ongoing challenge of insider risk management.',
            'Attackers are actively exploiting a vulnerability in Microsoft Remote Desktop Protocol (RDP) to gain unauthorized access to corporate networks. Security teams are advised to implement network segmentation and multi-factor authentication.',
            'A new ransomware variant specifically designed to target industrial control systems has been discovered. The malware can disrupt manufacturing operations and poses serious risks to operational technology environments.',
            'A bug bounty researcher has discovered and responsibly disclosed a critical vulnerability in a major social media platform that could have allowed account takeovers affecting millions of users. The platform has since patched the vulnerability.',
            'State-sponsored actors have deployed an advanced persistent threat framework with modular capabilities for reconnaissance, lateral movement, and data exfiltration. The framework demonstrates sophisticated development and operational security practices.'
        ],
        'category': [
            'vulnerability', 'ransomware', 'patch', 'ddos', 'phishing', 'vulnerability',
            'apt', 'breach', 'malware', 'breach', 'vulnerability', 'apt',
            'vulnerability', 'ransomware', 'vulnerability', 'malware', 'phishing',
            'vulnerability', 'malware', 'apt', 'breach', 'phishing', 'malware',
            'patch', 'phishing', 'breach', 'vulnerability', 'ransomware', 'vulnerability', 'apt',
            'vulnerability', 'malware', 'apt', 'phishing', 'vulnerability', 'breach',
            'apt', 'malware', 'vulnerability', 'ransomware'
        ],
        'severity': [
            'critical', 'critical', 'critical', 'high', 'medium', 'critical',
            'high', 'critical', 'high', 'high', 'critical', 'high',
            'critical', 'critical', 'critical', 'high', 'medium', 'critical',
            'high', 'high', 'medium', 'medium', 'high', 'critical',
            'high', 'high', 'high', 'critical', 'critical', 'high',
            'critical', 'high', 'high', 'medium', 'critical', 'high',
            'critical', 'high', 'critical', 'critical'
        ],
        'source': [
            'SecurityWeek', 'BleepingComputer', 'Microsoft Security', 'ThreatPost', 
            'KrebsOnSecurity', 'WPScan', 'Mandiant', 'CoinDesk', 'MalwareBytes',
            'DataBreaches.net', 'Cisco Talos', 'CrowdStrike', 'CERT', 'Reuters',
            'Google Security', 'Akamai', 'FBI Alert', 'Kernel.org', 'npm Security',
            'FireEye', 'AWS Security', 'IRS Alert', 'Zimperium', 'VMware Security',
            'Europol', 'Verizon DBIR', 'CISA', 'Dragos', 'HackerOne', 'MITRE',
            'SecurityWeek', 'CrowdStrike', 'Mandiant', 'KrebsOnSecurity', 'CERT',
            'HealthISAC', 'FireEye', 'Amnesty Tech', 'IoT Security', 'BleepingComputer'
        ],
        'created_at': [datetime.now() - timedelta(hours=i*2) for i in range(40)]
    }
    
    # 50 User interactions (more diverse)
    interactions_data = {
        'user_id': [1]*17 + [2]*17 + [3]*16,
        'post_id': [
            1, 3, 5, 6, 11, 15, 18, 19, 24, 29, 2, 7, 10, 13, 20, 27, 28,  # User 1 (Security Analyst)
            2, 4, 8, 10, 13, 14, 17, 20, 21, 22, 26, 27, 1, 6, 16, 25, 30,  # User 2 (IT Manager)
            1, 5, 9, 12, 15, 18, 19, 23, 29, 3, 6, 11, 16, 24, 28, 30       # User 3 (Developer)
        ],
        'interaction_type': [
            'bookmark', 'upvote', 'upvote', 'bookmark', 'bookmark', 'upvote', 'bookmark', 
            'bookmark', 'upvote', 'upvote', 'upvote', 'upvote', 'share', 'upvote', 
            'bookmark', 'upvote', 'bookmark',
            'bookmark', 'upvote', 'bookmark', 'share', 'upvote', 'bookmark', 'upvote',
            'bookmark', 'upvote', 'upvote', 'downvote', 'upvote', 'upvote', 'upvote',
            'bookmark', 'upvote', 'downvote',
            'bookmark', 'upvote', 'bookmark', 'upvote', 'bookmark', 'bookmark', 'bookmark',
            'upvote', 'bookmark', 'upvote', 'upvote', 'bookmark', 'upvote', 'upvote', 'upvote', 'bookmark'
        ],
        'category': [
            posts_data['category'][i-1] for i in [
                1, 3, 5, 6, 11, 15, 18, 19, 24, 29, 2, 7, 10, 13, 20, 27, 28,
                2, 4, 8, 10, 13, 14, 17, 20, 21, 22, 26, 27, 1, 6, 16, 25, 30,
                1, 5, 9, 12, 15, 18, 19, 23, 29, 3, 6, 11, 16, 24, 28, 30
            ]
        ],
        'timestamp': [datetime.now() - timedelta(hours=i) for i in range(50)]
    }
    
    # ✅ Fix uneven data lengths before creating DataFrame
    max_len = max(len(v) for v in posts_data.values())
    for key, value in posts_data.items():
        if len(value) < max_len:
            diff = max_len - len(value)
            print(f"⚠️ Fixing '{key}': adding {diff} empty entries")
            posts_data[key] += [""] * diff

    # Return DataFrames
    return pd.DataFrame(posts_data), pd.DataFrame(interactions_data)

# Global dataframes
posts_df, interactions_df = create_sample_data()

def calculate_user_preferences(user_id, interactions_df):
    """Calculate user's cybersecurity interest preferences"""
    user_interactions = interactions_df[interactions_df['user_id'] == user_id]
    
    if user_interactions.empty:
        return {}
    
    category_scores = {}
    
    for _, row in user_interactions.iterrows():
        category = row['category']
        interaction = row['interaction_type']
        
        if interaction == 'bookmark':
            score = 8
        elif interaction == 'upvote':
            score = 5
        elif interaction == 'share':
            score = 7
        elif interaction == 'downvote':
            score = -3
        else:
            score = 2
        
        if category in category_scores:
            category_scores[category] += score
        else:
            category_scores[category] = score
    
    return category_scores

def generate_feed(user_id, limit=10):
    """Generate personalized cybersecurity news feed"""
    user_prefs = calculate_user_preferences(user_id, interactions_df)
    
    seen_posts = interactions_df[interactions_df['user_id'] == user_id]['post_id'].unique()
    unseen_posts = posts_df[~posts_df['post_id'].isin(seen_posts)].copy()
    
    if unseen_posts.empty:
        return []
    
    severity_weights = {
        'critical': 20,
        'high': 15,
        'medium': 10,
        'low': 5
    }
    
    def calculate_post_score(row):
        category = row['category']
        severity = row['severity']
        
        pref_score = user_prefs.get(category, 0)
        severity_score = severity_weights.get(severity, 5)
        
        hours_old = (datetime.now() - row['created_at']).total_seconds() / 3600
        recency_score = max(0, 20 - hours_old)
        
        return (severity_score * 2) + (pref_score * 1.5) + recency_score
    
    unseen_posts['score'] = unseen_posts.apply(calculate_post_score, axis=1)
    unseen_posts = unseen_posts.sort_values('score', ascending=False)
    
    feed_posts = unseen_posts.head(limit)
    
    return feed_posts[[
        'post_id', 'title', 'content', 'category', 'severity', 'source', 'score'
    ]].to_dict('records')

# API Endpoints
@app.route('/feed/<int:user_id>', methods=['GET'])
def get_user_feed(user_id):
    """Get personalized feed"""
    limit = request.args.get('limit', 10, type=int)
    feed = generate_feed(user_id, limit)
    
    return jsonify({
        'user_id': user_id,
        'feed': feed,
        'count': len(feed)
    })

@app.route('/user/<int:user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """View user preferences"""
    prefs = calculate_user_preferences(user_id, interactions_df)
    
    return jsonify({
        'user_id': user_id,
        'interests': prefs,
        'top_interest': max(prefs, key=prefs.get) if prefs else None
    })

@app.route('/interaction', methods=['POST'])
def add_interaction():
    """Record user interaction"""
    global interactions_df
    
    data = request.get_json()
    
    new_interaction = pd.DataFrame([{
        'user_id': data['user_id'],
        'post_id': data['post_id'],
        'interaction_type': data['interaction_type'],
        'category': data['category'],
        'timestamp': datetime.now()
    }])
    
    interactions_df = pd.concat([interactions_df, new_interaction], ignore_index=True)
    
    return jsonify({
        'message': 'Interaction recorded',
        'data': data
    })

@app.route('/alerts/critical', methods=['GET'])
def get_critical_alerts():
    """Get critical alerts"""
    critical_posts = posts_df[posts_df['severity'] == 'critical']
    
    return jsonify({
        'critical_alerts': critical_posts[[
            'post_id', 'title', 'content', 'category', 'source', 'severity'
        ]].to_dict('records'),
        'count': len(critical_posts)
    })

@app.route('/category/<category_name>', methods=['GET'])
def get_by_category(category_name):
    """Get posts by category"""
    category_posts = posts_df[posts_df['category'] == category_name]
    
    return jsonify({
        'category': category_name,
        'posts': category_posts[[
            'post_id', 'title', 'content', 'severity', 'source', 'category'
        ]].to_dict('records'),
        'count': len(category_posts)
    })

@app.route('/popular', methods=['GET'])
def get_popular_posts():
    """Get most popular posts (most interactions across all users)"""
    limit = request.args.get('limit', 10, type=int)
    
    # Count interactions per post
    interaction_counts = interactions_df.groupby('post_id').size().reset_index(name='interaction_count')
    
    # Merge with posts data
    popular_posts = posts_df.merge(interaction_counts, on='post_id', how='left')
    popular_posts['interaction_count'] = popular_posts['interaction_count'].fillna(0)
    
    # Sort by interaction count
    popular_posts = popular_posts.sort_values('interaction_count', ascending=False).head(limit)
    
    return jsonify({
        'popular_posts': popular_posts[[
            'post_id', 'title', 'content', 'category', 'severity', 'source', 'interaction_count'
        ]].to_dict('records'),
        'count': len(popular_posts)
    })

@app.route('/trending', methods=['GET'])
def get_trending_posts():
    """Get trending posts (most interactions in last 24 hours)"""
    limit = request.args.get('limit', 10, type=int)
    
    # Get recent interactions (last 24 hours)
    recent_cutoff = datetime.now() - timedelta(hours=24)
    recent_interactions = interactions_df[interactions_df['timestamp'] > recent_cutoff]
    
    if recent_interactions.empty:
        return jsonify({
            'trending_posts': [],
            'count': 0,
            'message': 'No trending posts in last 24 hours'
        })
    
    # Count recent interactions per post
    trending_counts = recent_interactions.groupby('post_id').size().reset_index(name='trend_score')
    
    # Merge with posts data
    trending_posts = posts_df.merge(trending_counts, on='post_id', how='inner')
    trending_posts = trending_posts.sort_values('trend_score', ascending=False).head(limit)
    
    return jsonify({
        'trending_posts': trending_posts[[
            'post_id', 'title', 'content', 'category', 'severity', 'source', 'trend_score'
        ]].to_dict('records'),
        'count': len(trending_posts)
    })

@app.route('/most-useful', methods=['GET'])
def get_most_useful():
    """Get most useful posts (highest upvote ratio)"""
    limit = request.args.get('limit', 10, type=int)
    
    # Calculate upvote/bookmark scores
    useful_interactions = interactions_df[
        interactions_df['interaction_type'].isin(['upvote', 'bookmark', 'share'])
    ]
    
    if useful_interactions.empty:
        return jsonify({
            'useful_posts': [],
            'count': 0
        })
    
    # Group by post and count useful interactions
    useful_counts = useful_interactions.groupby('post_id').size().reset_index(name='useful_score')
    
    # Merge with posts
    useful_posts = posts_df.merge(useful_counts, on='post_id', how='inner')
    useful_posts = useful_posts.sort_values('useful_score', ascending=False).head(limit)
    
    return jsonify({
        'useful_posts': useful_posts[[
            'post_id', 'title', 'content', 'category', 'severity', 'source', 'useful_score'
        ]].to_dict('records'),
        'count': len(useful_posts)
    })

@app.route('/most-bookmarked', methods=['GET'])
def get_most_bookmarked():
    """Get most bookmarked posts"""
    limit = request.args.get('limit', 10, type=int)
    
    # Get only bookmarks
    bookmarks = interactions_df[interactions_df['interaction_type'] == 'bookmark']
    
    if bookmarks.empty:
        return jsonify({
            'bookmarked_posts': [],
            'count': 0
        })
    
    # Count bookmarks per post
    bookmark_counts = bookmarks.groupby('post_id').size().reset_index(name='bookmark_count')
    
    # Merge with posts
    bookmarked_posts = posts_df.merge(bookmark_counts, on='post_id', how='inner')
    bookmarked_posts = bookmarked_posts.sort_values('bookmark_count', ascending=False).head(limit)
    
    return jsonify({
        'bookmarked_posts': bookmarked_posts[[
            'post_id', 'title', 'content', 'category', 'severity', 'source', 'bookmark_count'
        ]].to_dict('records'),
        'count': len(bookmarked_posts)
    })

@app.route('/article/<int:post_id>', methods=['GET'])
def get_article(post_id):
    """Get full article details"""
    article = posts_df[posts_df['post_id'] == post_id]
    
    if article.empty:
        return jsonify({'error': 'Article not found'}), 404
    
    article_data = article.iloc[0].to_dict()
    article_data['created_at'] = article_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        'article': article_data
    })

@app.route('/user/<int:user_id>/bookmarks', methods=['GET'])
def get_user_bookmarks(user_id):
    """Get specific user's bookmarked posts"""
    # Get user's bookmarked post IDs
    user_bookmarks = interactions_df[
        (interactions_df['user_id'] == user_id) & 
        (interactions_df['interaction_type'] == 'bookmark')
    ]['post_id'].unique()
    
    # Get those posts
    bookmarked_posts = posts_df[posts_df['post_id'].isin(user_bookmarks)]
    
    return jsonify({
        'user_id': user_id,
        'bookmarks': bookmarked_posts[[
            'post_id', 'title', 'content', 'category', 'severity', 'source'
        ]].to_dict('records'),
        'count': len(bookmarked_posts)
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Platform statistics"""
    # Most interacted posts
    top_posts = interactions_df.groupby('post_id').size().reset_index(name='count')
    top_posts = top_posts.sort_values('count', ascending=False).head(5)
    top_post_ids = top_posts['post_id'].tolist()
    
    return jsonify({
        'total_alerts': len(posts_df),
        'total_interactions': len(interactions_df),
        'active_users': interactions_df['user_id'].nunique(),
        'severity_distribution': posts_df['severity'].value_counts().to_dict(),
        'category_distribution': posts_df['category'].value_counts().to_dict(),
        'interaction_types': interactions_df['interaction_type'].value_counts().to_dict(),
        'top_post_ids': top_post_ids,
        'most_active_category': interactions_df['category'].value_counts().to_dict()
    })

@app.route('/')
def home():
    return """
    <h1>CyberPulse Feed API</h1>
    <h2>40 Real Cybersecurity News Articles</h2>
    <p><strong>Personalized Feeds:</strong></p>
    <ul>
        <li><a href='/feed/1'>/feed/1</a> - Security Analyst feed</li>
        <li><a href='/feed/2'>/feed/2</a> - IT Manager feed</li>
        <li><a href='/feed/3'>/feed/3</a> - Developer feed</li>
    </ul>
    <p><strong>Discovery Feeds:</strong></p>
    <ul>
        <li><a href='/popular'>/popular</a> - Most popular posts (all users)</li>
        <li><a href='/trending'>/trending</a> - Trending in last 24 hours</li>
        <li><a href='/most-useful'>/most-useful</a> - Highest upvoted posts</li>
        <li><a href='/most-bookmarked'>/most-bookmarked</a> - Most bookmarked</li>
    </ul>
    <p><strong>Filters:</strong></p>
    <ul>
        <li><a href='/alerts/critical'>/alerts/critical</a> - Critical alerts only</li>
        <li><a href='/category/vulnerability'>/category/vulnerability</a> - By category</li>
    </ul>
    <p><strong>User Data:</strong></p>
    <ul>
        <li><a href='/user/1/preferences'>/user/1/preferences</a> - User interests</li>
        <li><a href='/user/1/bookmarks'>/user/1/bookmarks</a> - User's saved posts</li>
    </ul>
    <p><strong>Analytics:</strong></p>
    <ul>
        <li><a href='/stats'>/stats</a> - Platform statistics</li>
    </ul>
    """

from flask import render_template, send_from_directory

@app.route('/feed')
def show_feed_page():
    """Show the HTML feed UI"""
    return render_template('feed.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve JS and CSS files directly from current folder"""
    return send_from_directory('.', filename)


if __name__ == '__main__':
    print("🛡️ CyberPulse Feed API starting...")
    print(f"📊 Loaded {len(posts_df)} news articles")
    print(f"👥 {len(interactions_df)} user interactions")
    print("\n🔗 Available endpoints:")
    print("   Personalized:")
    print("   - GET  /feed/<user_id>")
    print("   - GET  /user/<user_id>/preferences")
    print("   - GET  /user/<user_id>/bookmarks")
    print("\n   Discovery:")
    print("   - GET  /popular (most interactions)")
    print("   - GET  /trending (last 24h)")
    print("   - GET  /most-useful (highest upvotes)")
    print("   - GET  /most-bookmarked")
    print("\n   Filters:")
    print("   - GET  /alerts/critical")
    print("   - GET  /category/<category_name>")
    print("\n   Actions:")
    print("   - POST /interaction")
    print("   - GET  /stats")
    app.run(debug=True, port=5000)


