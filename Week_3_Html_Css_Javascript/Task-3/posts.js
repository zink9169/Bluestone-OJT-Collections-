


async function laodPosts() {
  return (await fetch("https://dummyjson.com/posts")).json();
}

document.addEventListener("DOMContentLoaded", async () => {
  let posts = [];

  try {
    posts = await laodPosts();
  } catch {
    console.log("Errors");
    console.log(e);
  }

  console.log(posts);
});
