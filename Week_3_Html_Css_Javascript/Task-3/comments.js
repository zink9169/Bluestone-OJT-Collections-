async function laodComments() {
  return (await fetch("https://dummyjson.com/comments")).json();
}

document.addEventListener("DOMContentLoaded", async () => {
  let comments = [];

  try {
    posts = await laodComments();
  } catch {
    console.log("Errors");
    console.log(e);
  }

  console.log(comments);
});
