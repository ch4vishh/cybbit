let currentUser = 1;
let currentCategory = 'all';

// Load feed when page loads
window.onload = function() {
    loadFeed(1);
    loadPreferences(1);
};

async function loadFeed(userId) {
    currentUser = userId;
    
    // Update active button
    document.querySelectorAll('.user-select button').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === userId - 1);
    });

    // Reset category filter
    currentCategory = 'all';
    document.querySelectorAll('.category-buttons button').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === 0);
    });

    // Update header
    const userNames = ['Security Analyst', 'IT Manager', 'Developer'];
    document.getElementById('feedTitle').textContent = `📰 ${userNames[userId-1]} Feed`;
    document.getElementById('feedSubtitle').textContent = 'Personalized cybersecurity news based on your interests';

    // Show loading
    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading your personalized feed...</p>
        </div>
    `;

    try {
        const response = await fetch(`http://127.0.0.1:5000/feed/${userId}?limit=15`);
        const data = await response.json();

        displayFeed(data.feed);
        loadPreferences(userId);
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error loading feed.<br>Make sure Flask app is running on port 5000!<br><br>Run: python app.py</div>';
    }
}

async function loadPreferences(userId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/user/${userId}/preferences`);
        const data = await response.json();

        const prefsHtml = Object.entries(data.interests).length > 0
            ? Object.entries(data.interests)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 6)
                .map(([category, score]) => `
                    <div class="preference-item">
                        <span>${getCategoryIcon(category)} ${capitalize(category)}</span>
                        <span style="color: ${score > 0 ? '#4ade80' : '#f87171'}; font-weight: 600;">${score > 0 ? '+' : ''}${score}</span>
                    </div>
                `).join('')
            : '<div style="color: #94a3b8; padding: 1rem 0; text-align: center;">No preferences yet.<br>Interact with posts to build your profile!</div>';

        document.getElementById('preferencesContent').innerHTML = prefsHtml;
    } catch (error) {
        document.getElementById('preferencesContent').innerHTML = 
            '<div style="color: #f87171;">Error loading preferences</div>';
    }
}

function displayFeed(alerts) {
    if (alerts.length === 0) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">📭 No more alerts to show!<br><br>You\'ve seen all available content.<br>Check back later for updates.</div>';
        return;
    }

    const feedHtml = alerts.map(alert => `
        <div class="alert-card ${alert.severity}">
            <div class="alert-header">
                <h3 class="alert-title" onclick="openArticle(${alert.post_id})">${alert.title}</h3>
                <span class="severity-badge ${alert.severity}">${alert.severity}</span>
            </div>
            
            <div class="alert-meta">
                <span class="category-tag">${getCategoryIcon(alert.category)} ${capitalize(alert.category)}</span>
                <span class="source-tag">📰 ${alert.source}</span>
            </div>
            
            <p class="alert-content">${alert.content.substring(0, 200)}... <span style="color: #60a5fa; cursor: pointer;" onclick="openArticle(${alert.post_id})">Read more</span></p>
            
            <div class="alert-footer">
                <span class="relevance-score">🎯 Relevance: ${alert.score.toFixed(1)}</span>
                <div class="alert-actions">
                    <button class="action-btn" onclick="interact(${alert.post_id}, 'bookmark', '${alert.category}', this)">
                        🔖 Bookmark
                    </button>
                    <button class="action-btn" onclick="interact(${alert.post_id}, 'upvote', '${alert.category}', this)">
                        👍 Useful
                    </button>
                    <button class="action-btn" onclick="interact(${alert.post_id}, 'share', '${alert.category}', this)">
                        📤 Share
                    </button>
                </div>
            </div>
        </div>
    `).join('');

    document.getElementById('feed').innerHTML = feedHtml;
}
           


async function interact(postId, type, category, button) {
    try {
        const response = await fetch('http://127.0.0.1:5000/interaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUser,
                post_id: postId,
                interaction_type: type,
                category: category
            })
        });

        if (response.ok) {
            // Visual feedback
            const icons = { bookmark: '✅ Saved', upvote: '✅ Marked', share: '✅ Shared' };
            button.classList.add('bookmarked');
            button.innerHTML = icons[type];
            button.disabled = true;
            
            // Reload feed after 1 second
            setTimeout(() => {
                if (currentCategory === 'all') {
                    loadFeed(currentUser);
                } else {
                    filterCategory(currentCategory);
                }
            }, 1000);
        }
    } catch (error) {
        alert('⚠️ Error recording interaction.\nMake sure Flask is running!');
    }
}

async function showCriticalAlerts() {
    document.getElementById('feedTitle').textContent = '🚨 Critical Security Alerts';
    document.getElementById('feedSubtitle').textContent = 'Immediate action required - High priority threats';
    
    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading critical alerts...</p>
        </div>
    `;

    try {
        const response = await fetch('http://127.0.0.1:5000/alerts/critical');
        const data = await response.json();

        if (data.critical_alerts.length === 0) {
            document.getElementById('feed').innerHTML = 
                '<div class="no-posts">✅ No critical alerts at this time!<br><br>All systems secure.</div>';
            return;
        }

        const alertsHtml = data.critical_alerts.map(alert => `
            <div class="alert-card critical">
                <div class="alert-header">
                    <h3 class="alert-title">🚨 ${alert.title}</h3>
                    <span class="severity-badge critical">CRITICAL</span>
                </div>
                
                <div class="alert-meta">
                    <span class="category-tag">${getCategoryIcon(alert.category)} ${capitalize(alert.category)}</span>
                    <span class="source-tag">📰 ${alert.source}</span>
                </div>
                
                <p class="alert-content">${alert.content}</p>
                
                <div class="alert-footer">
                    <div class="alert-actions">
                        <button class="action-btn" onclick="interact(${alert.post_id}, 'bookmark', '${alert.category}', this)">
                            🔖 Bookmark
                        </button>
                        <button class="action-btn" onclick="interact(${alert.post_id}, 'upvote', '${alert.category}', this)">
                            👍 Useful
                        </button>
                        <button class="action-btn" onclick="interact(${alert.post_id}, 'share', '${alert.category}', this)">
                            📤 Share
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('feed').innerHTML = alertsHtml;
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error loading critical alerts</div>';
    }
}

async function filterCategory(category) {
    currentCategory = category;
    
    // Update active button
    document.querySelectorAll('.category-buttons button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    if (category === 'all') {
        loadFeed(currentUser);
        return;
    }

    document.getElementById('feedTitle').textContent = `${getCategoryIcon(category)} ${capitalize(category)} News`;
    document.getElementById('feedSubtitle').textContent = `Filtered cybersecurity alerts in ${category} category`;

    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Filtering by ${category}...</p>
        </div>
    `;

    try {
        const response = await fetch(`http://127.0.0.1:5000/category/${category}`);
        const data = await response.json();

        if (data.posts.length === 0) {
            document.getElementById('feed').innerHTML = 
                `<div class="no-posts">📭 No ${category} alerts found<br><br>Check back later for updates</div>`;
            return;
        }

        const postsHtml = data.posts.map(post => `
            <div class="alert-card ${post.severity}">
                <div class="alert-header">
                    <h3 class="alert-title">${post.title}</h3>
                    <span class="severity-badge ${post.severity}">${post.severity}</span>
                </div>
                
                <div class="alert-meta">
                    <span class="category-tag">${getCategoryIcon(category)} ${capitalize(category)}</span>
                    <span class="source-tag">📰 ${post.source}</span>
                </div>
                
                <p class="alert-content">${post.content}</p>
                
                <div class="alert-footer">
                    <div class="alert-actions">
                        <button class="action-btn" onclick="interact(${post.post_id}, 'bookmark', '${category}', this)">
                            🔖 Bookmark
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'upvote', '${category}', this)">
                            👍 Useful
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'share', '${category}', this)">
                            📤 Share
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('feed').innerHTML = postsHtml;
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error filtering category</div>';
    }
}

async function showStats() {
    const modal = document.getElementById('statsModal');
    modal.style.display = 'block';

    try {
        const response = await fetch('http://127.0.0.1:5000/stats');
        const data = await response.json();

        const statsHtml = `
            <div class="stat-item">
                <h3>📰 Total Alerts</h3>
                <p style="font-size: 2rem; color: #60a5fa; font-weight: bold;">${data.total_alerts}</p>
            </div>
            <div class="stat-item">
                <h3>👥 Active Users</h3>
                <p style="font-size: 2rem; color: #60a5fa; font-weight: bold;">${data.active_users}</p>
            </div>
            <div class="stat-item">
                <h3>⚡ Total Interactions</h3>
                <p style="font-size: 2rem; color: #60a5fa; font-weight: bold;">${data.total_interactions}</p>
            </div>
            <div class="stat-item">
                <h3>📊 Severity Distribution</h3>
                ${Object.entries(data.severity_distribution).map(([sev, count]) => 
                    `<p>${capitalize(sev)}: <strong>${count}</strong></p>`
                ).join('')}
            </div>
            <div class="stat-item">
                <h3>🏷️ Category Distribution</h3>
                ${Object.entries(data.category_distribution).map(([cat, count]) => 
                    `<p>${getCategoryIcon(cat)} ${capitalize(cat)}: <strong>${count}</strong></p>`
                ).join('')}
            </div>
        `;

        document.getElementById('statsContent').innerHTML = statsHtml;
    } catch (error) {
        document.getElementById('statsContent').innerHTML = 
            '<div style="color: #f87171;">Error loading statistics</div>';
    }
}

function closeStats() {
    document.getElementById('statsModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('statsModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

function getCategoryIcon(category) {
    const icons = {
        'vulnerability': '🔓',
        'ransomware': '🔒',
        'patch': '🔧',
        'ddos': '⚡',
        'phishing': '🎣',
        'apt': '🎯',
        'breach': '💔',
        'malware': '🦠'
    };
    return icons[category] || '📌';
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Article Detail View
async function openArticle(postId) {
    const modal = document.getElementById('articleModal');
    modal.style.display = 'block';
    
    document.getElementById('articleContent').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading article...</p>
        </div>
    `;

    try {
        const response = await fetch(`http://127.0.0.1:5000/article/${postId}`);
        const data = await response.json();
        const article = data.article;

        const articleHtml = `
            <div class="article-detail">
                <h1>${article.title}</h1>
                
                <div class="article-meta-detail">
                    <span class="severity-badge ${article.severity}">${article.severity}</span>
                    <span class="category-tag">${getCategoryIcon(article.category)} ${capitalize(article.category)}</span>
                    <span class="source-tag">📰 ${article.source}</span>
                    <span class="source-tag">📅 ${new Date(article.created_at).toLocaleDateString()}</span>
                </div>
                
                <div class="article-body">
                    ${article.content}
                </div>
                
                <div class="alert-footer" style="margin-top: 2rem;">
                    <div class="alert-actions">
                        <button class="action-btn" onclick="interact(${article.post_id}, 'bookmark', '${article.category}', this)">
                            🔖 Bookmark
                        </button>
                        <button class="action-btn" onclick="interact(${article.post_id}, 'upvote', '${article.category}', this)">
                            👍 Mark Useful
                        </button>
                        <button class="action-btn" onclick="interact(${article.post_id}, 'share', '${article.category}', this)">
                            📤 Share
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('articleContent').innerHTML = articleHtml;
    } catch (error) {
        document.getElementById('articleContent').innerHTML = 
            '<div class="no-posts">⚠️ Error loading article</div>';
    }
}

function closeArticle() {
    document.getElementById('articleModal').style.display = 'none';
}

// NEW FEATURES - Popular, Trending, Most Useful

async function showPopular() {
    document.getElementById('feedTitle').textContent = '🔥 Popular Posts';
    document.getElementById('feedSubtitle').textContent = 'Most interacted posts across all users';
    
    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading popular posts...</p>
        </div>
    `;

    try {
        const response = await fetch('http://127.0.0.1:5000/popular?limit=15');
        const data = await response.json();

        if (data.popular_posts.length === 0) {
            document.getElementById('feed').innerHTML = 
                '<div class="no-posts">📭 No popular posts yet</div>';
            return;
        }

        const postsHtml = data.popular_posts.map(post => `
            <div class="alert-card ${post.severity}">
                <div class="alert-header">
                    <h3 class="alert-title">${post.title}</h3>
                    <span class="severity-badge ${post.severity}">${post.severity}</span>
                </div>
                
                <div class="alert-meta">
                    <span class="category-tag">${getCategoryIcon(post.category)} ${capitalize(post.category)}</span>
                    <span class="source-tag">📰 ${post.source}</span>
                    <span class="source-tag">🔥 ${post.interaction_count} interactions</span>
                </div>
                
                <p class="alert-content">${post.content}</p>
                
                <div class="alert-footer">
                    <span class="relevance-score">🔥 Popularity: ${post.interaction_count}</span>
                    <div class="alert-actions">
                        <button class="action-btn" onclick="interact(${post.post_id}, 'bookmark', '${post.category}', this)">
                            🔖 Bookmark
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'upvote', '${post.category}', this)">
                            👍 Useful
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('feed').innerHTML = postsHtml;
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error loading popular posts</div>';
    }
}

async function showTrending() {
    document.getElementById('feedTitle').textContent = '📈 Trending Now';
    document.getElementById('feedSubtitle').textContent = 'Hot topics in the last 24 hours';
    
    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading trending posts...</p>
        </div>
    `;

    try {
        const response = await fetch('http://127.0.0.1:5000/trending?limit=15');
        const data = await response.json();

        if (data.trending_posts.length === 0) {
            document.getElementById('feed').innerHTML = 
                '<div class="no-posts">📭 No trending posts in last 24 hours</div>';
            return;
        }

        const postsHtml = data.trending_posts.map(post => `
            <div class="alert-card ${post.severity}">
                <div class="alert-header">
                    <h3 class="alert-title">📈 ${post.title}</h3>
                    <span class="severity-badge ${post.severity}">${post.severity}</span>
                </div>
                
                <div class="alert-meta">
                    <span class="category-tag">${getCategoryIcon(post.category)} ${capitalize(post.category)}</span>
                    <span class="source-tag">📰 ${post.source}</span>
                    <span class="source-tag">📈 Trending Score: ${post.trend_score}</span>
                </div>
                
                <p class="alert-content">${post.content}</p>
                
                <div class="alert-footer">
                    <span class="relevance-score">📈 Trend: ${post.trend_score}</span>
                    <div class="alert-actions">
                        <button class="action-btn" onclick="interact(${post.post_id}, 'bookmark', '${post.category}', this)">
                            🔖 Bookmark
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'upvote', '${post.category}', this)">
                            👍 Useful
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('feed').innerHTML = postsHtml;
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error loading trending posts</div>';
    }
}

async function showMostUseful() {
    document.getElementById('feedTitle').textContent = '⭐ Most Useful Posts';
    document.getElementById('feedSubtitle').textContent = 'Highest rated by the community';
    
    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading most useful posts...</p>
        </div>
    `;

    try {
        const response = await fetch('http://127.0.0.1:5000/most-useful?limit=15');
        const data = await response.json();

        if (data.useful_posts.length === 0) {
            document.getElementById('feed').innerHTML = 
                '<div class="no-posts">📭 No rated posts yet</div>';
            return;
        }

        const postsHtml = data.useful_posts.map(post => `
            <div class="alert-card ${post.severity}">
                <div class="alert-header">
                    <h3 class="alert-title">⭐ ${post.title}</h3>
                    <span class="severity-badge ${post.severity}">${post.severity}</span>
                </div>
                
                <div class="alert-meta">
                    <span class="category-tag">${getCategoryIcon(post.category)} ${capitalize(post.category)}</span>
                    <span class="source-tag">📰 ${post.source}</span>
                    <span class="source-tag">⭐ ${post.useful_score} votes</span>
                </div>
                
                <p class="alert-content">${post.content}</p>
                
                <div class="alert-footer">
                    <span class="relevance-score">⭐ Rating: ${post.useful_score}</span>
                    <div class="alert-actions">
                        <button class="action-btn" onclick="interact(${post.post_id}, 'bookmark', '${post.category}', this)">
                            🔖 Bookmark
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'upvote', '${post.category}', this)">
                            👍 Useful
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('feed').innerHTML = postsHtml;
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error loading useful posts</div>';
    }
}

async function showMyBookmarks() {
    document.getElementById('feedTitle').textContent = '🔖 My Bookmarks';
    document.getElementById('feedSubtitle').textContent = 'Your saved posts for later reading';
    
    document.getElementById('feed').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading your bookmarks...</p>
        </div>
    `;

    try {
        const response = await fetch(`http://127.0.0.1:5000/user/${currentUser}/bookmarks`);
        const data = await response.json();

        if (data.bookmarks.length === 0) {
            document.getElementById('feed').innerHTML = 
                '<div class="no-posts">📭 No bookmarks yet<br><br>Start bookmarking posts you want to read later!</div>';
            return;
        }

        const postsHtml = data.bookmarks.map(post => `
            <div class="alert-card ${post.severity}">
                <div class="alert-header">
                    <h3 class="alert-title">🔖 ${post.title}</h3>
                    <span class="severity-badge ${post.severity}">${post.severity}</span>
                </div>
                
                <div class="alert-meta">
                    <span class="category-tag">${getCategoryIcon(post.category)} ${capitalize(post.category)}</span>
                    <span class="source-tag">📰 ${post.source}</span>
                </div>
                
                <p class="alert-content">${post.content}</p>
                
                <div class="alert-footer">
                    <div class="alert-actions">
                        <button class="action-btn bookmarked">
                            ✅ Bookmarked
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'upvote', '${post.category}', this)">
                            👍 Useful
                        </button>
                        <button class="action-btn" onclick="interact(${post.post_id}, 'share', '${post.category}', this)">
                            📤 Share
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('feed').innerHTML = postsHtml;
    } catch (error) {
        document.getElementById('feed').innerHTML = 
            '<div class="no-posts">⚠️ Error loading bookmarks</div>';
    }
}