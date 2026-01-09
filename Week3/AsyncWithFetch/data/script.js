
// posts-list → Post list ပြမယ့်နေရာ
// detail-content → Post detail + comments ပြမယ့်နေရာ
        const postsListElement = document.getElementById('posts-list');
        const detailContentElement = document.getElementById('detail-content');


        // posts → API ကနေ ရလာတဲ့ post list ကို သိမ်း
        // activePostId → လက်ရှိ click လုပ်ထားတဲ့ post id
        let posts = [];
        let activePostId = null;
        


        // Fetch all posts on page load
        // async function → API ကို await နဲ့ ခေါ်နိုင်
        async function fetchPosts() { 
            try {
                // Loading ပြ
                showLoading(postsListElement, 'Loading blog posts...');
                // JSONPlaceholder API က post list ကိုယူ
                const response = await fetch('https://jsonplaceholder.typicode.com/posts');
                // API error ဖြစ်ရင် catch သို့ သွား
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                //JSON ပြောင်း + display
                posts = await response.json();
                displayPosts();
            } catch (error) {
                showError(postsListElement, `Failed to load posts: ${error.message}`);
            }
        }
        

       // displayPosts() – Post list ကို UI မှာပြ
        function displayPosts() {
            if (!posts || posts.length === 0) {
                postsListElement.innerHTML = '<div class="empty-state"><p>No posts available.</p></div>';
                return;
            }
            postsListElement.innerHTML = '';
            //Post တစ်ခုချင်း loop
            posts.forEach(post => {
                //Card element ဖန်တီး
                const postElement = document.createElement('div');
                //လက်ရှိရွေးထားတဲ့ post ကို highlight လုပ်
                postElement.className = `post-card ${activePostId === post.id ? 'active' : ''}`;
                postElement.innerHTML = `
                    <div class="post-title">${post.title}</div>
                    <div class="post-body">${post.body}</div>
                    <div class="post-meta">
                        <span class="post-id">Post #${post.id}</span>
                        <span>User ID: ${post.userId}</span>
                    </div>
                `;
                
                // အရင် active class အားလုံး ဖယ်
                // Click လုပ်တဲ့ card ကို active ပေး
                // fetchPostDetails(post.id) ခေါ်
                postElement.addEventListener('click', () => { 
                    document.querySelectorAll('.post-card').forEach(card => {
                        card.classList.remove('active');
                    });
                    postElement.classList.add('active');
                    fetchPostDetails(post.id);
                });
                postsListElement.appendChild(postElement);
            });
        }
        
       //fetchPostDetails(postId) – Post detail + comments ယူ
        async function fetchPostDetails(postId) {
           // Active post id update
            activePostId = postId;
            try {
                //Loading ပြ
                showLoading(detailContentElement, 'Loading post details and comments...');
                // Post detail နဲ့ comments ကို တစ်ပြိုင်နက်တည်း fetch လုပ်/ Performance ကောင်း
                const [postResponse, commentsResponse] = await Promise.all([
                    fetch(`https://jsonplaceholder.typicode.com/posts/${postId}`),
                    fetch(`https://jsonplaceholder.typicode.com/posts/${postId}/comments`)
                ]);
                if (!postResponse.ok || !commentsResponse.ok) {
                    throw new Error('Failed to fetch post details or comments');
                }
                //JSON ပြောင်း
                const post = await postResponse.json();
                const comments = await commentsResponse.json();
                displayPostDetails(post, comments);
            } catch (error) {
                showError(detailContentElement, `Failed to load post details: ${error.message}`);
            }
        } 
        // UI ပြ
        function displayPostDetails(post, comments) {
            detailContentElement.innerHTML = `
                <div class="post-detail">
                
                // Post detail + comments ကို HTML နဲ့ ပြ
                    <h3 class="detail-title">${post.title}</h3>
                    <p class="detail-body">${post.body}</p>
                    <div class="detail-meta">
                        <span>Post ID: ${post.id}</span>
                        <span>User ID: ${post.userId}</span>
                    </div>
                </div>
                
                //Comment section
                <div class="comments-section">
                    <h3 class="section-title"><i class="fas fa-comments"></i> Comments (${comments.length})</h3>
                    ${comments.length > 0 ? 
                        `<div class="comments-list">

                       // Comment တစ်ခုချင်းကို card အနေနဲ့ပြ
                            ${comments.map(comment => `
                                <div class="comment-card">
                                    <div class="comment-name">
                                        <i class="fas fa-user"></i> ${comment.name}
                                    </div>
                                    <div class="comment-email">
                                        <i class="fas fa-envelope"></i> ${comment.email}
                                    </div>
                                    <p class="comment-body">${comment.body}</p>
                                </div>
                            `).join('')}
                        </div>` 
                        : 
                        `<div class="empty-state">
                            <i class="fas fa-comment-slash"></i>
                            <p>No comments for this post yet.</p>
                        </div>`
                    }
                </div>
            `;
        }
        
        // Loading spinner + message ပြဖို့ reusable function
        function showLoading(element, message = 'Loading...') {
            element.innerHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    <p>${message}</p>
                </div>
            `;
        }
        
        // Error message ကို UI မှာ ပြဖို့
        function showError(element, message) {
            element.innerHTML = `
                <div class="error">
                    <p><i class="fas fa-exclamation-triangle"></i> ${message}</p>
                </div>
            `;
        }
        
        // Page load ပြီးတာနဲ့ / fetchPosts() ကို အလိုအလျောက် run
        document.addEventListener('DOMContentLoaded', fetchPosts);
