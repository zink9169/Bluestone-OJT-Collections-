const postGrid = document.querySelector(".js-post-grid");
const postDetail = document.querySelector(".js-post-detail");

async function fetchPosts() {
    const res = await fetch("https://jsonplaceholder.typicode.com/posts");
    const posts = await res.json();
    console.log(posts)

    let postHtml = "";
    posts.forEach(post => {
        postHtml += `
                    <div class="post-card" data-post-id="${post.id}">
                    <h3>${post.title}</h3>
                    <p>${post.body.slice(0, 80)}...</p>
                    </div>
      `;
    });
    postGrid.innerHTML = postHtml;
}

fetchPosts();
postGrid.addEventListener("click", (e) => {
    const card = e.target.closest(".post-card");
    if (!card) return;
    const postId = card.dataset.postId;
    loadPostDetail(postId);
});


async function loadPostDetail(postId) {
    postDetail.innerHTML = "<p>Loading...</p>";
    // Fetch post detail
    const postRes = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${postId}`
    );
    const post = await postRes.json();

    // Fetch comments
    const commentRes = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${postId}/comments`
    );
    const comments = await commentRes.json();
    console.log(comments)

    renderPostDetail(post, comments);
}

function renderPostDetail(post, comments) {
    postGrid.classList.add("hidden");
    postDetail.classList.remove("hidden");
    postDetail.innerHTML = `
      <button class="back-btn" onclick="goBack()">← Back to Posts</button>

      <h3>${post.title}</h3>
      <p>${post.body}</p>

      <p>Comments (${comments.length})</p>
      <div class="comments-container">
        ${comments.map(c => `
          <div class="comment">
            <strong>${c.name}</strong>
            <p>${c.body}</p>
            <small>${c.email}</small>
          </div>
        `).join("")}
      </div>
    `;
}

function goBack() {
    postDetail.classList.add("hidden");
    postGrid.classList.remove("hidden");
}
