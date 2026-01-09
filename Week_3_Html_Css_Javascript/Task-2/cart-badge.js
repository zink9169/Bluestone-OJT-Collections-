function getCart() {
  return JSON.parse(localStorage.getItem("cart")) || [];
}

function cartItemCount() {

  return getCart().reduce((sum, item) => sum + (item.qty || 0), 0);
}

function updateCartBadge() {
  const badge = document.getElementById("cartBadge");
  if (!badge) return;

  const count = cartItemCount();

  if (count > 0) {
    badge.textContent = count;
    badge.classList.remove("d-none");
  } else {
    badge.classList.add("d-none");
  }
}

document.addEventListener("DOMContentLoaded", updateCartBadge);


window.addEventListener("storage", (e) => {
  if (e.key === "cart") updateCartBadge();
});


window.updateCartBadge = updateCartBadge;
