import { products } from "../data/products.js";
import { updateCartQuantity, addToCart, renderNavBarWithCartQty } from "../data/cart.js";
import { initMobileMenuToggle } from "./util.js";

document.querySelector('.js-navbar').innerHTML = renderNavBarWithCartQty();

let productHtml = "";
products.forEach(product => {
  productHtml += `
    <div class="group rounded-sm overflow-hidden relative bg-white cursor-pointer js-product-card" data-id="${product.id}">
      <div class="relative">
        <img src="${product.images[0]}" class="w-full h-60 object-cover" alt="${product.name}">
        
        <!-- Wishlist button -->
        <button class="absolute top-3 right-3 w-9 h-9 rounded-full bg-white shadow js-wishlist-btn opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <i class="bi bi-heart"></i>
        </button>

        <!-- Add to Cart button -->
        <button class="js-add-to-cart-btn absolute bottom-3 left-3 w-10 h-10 rounded-full bg-white shadow opacity-0 group-hover:opacity-100 transition-opacity duration-300" data-button-id="${product.id}">
          <i class="bi bi-cart"></i>
        </button>
      </div>

      <div class="pt-4">
        <h4 class="font-semibold truncate">${product.name}</h4>
        <p class="font-bold">$${(product.price / 100).toFixed(2)}</p>
      </div>
    </div>
  `;
});

document.querySelector(".js-product-grid").innerHTML = productHtml;

// Product card click
document.querySelectorAll(".js-product-card").forEach(card => {
  card.addEventListener("click", e => {
    if (e.target.closest(".js-add-to-cart-btn") || e.target.closest(".js-wishlist-btn")) return;
    window.location.href = `product-detail.html?id=${card.dataset.id}`;
  });
});

// Add to cart button
document.querySelectorAll(".js-add-to-cart-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.stopPropagation();
    const productId = Number(btn.dataset.buttonId);
    addToCart(productId)
  });
});
initMobileMenuToggle();
updateCartQuantity();
