import {
  cart,
  renderNavBarWithCartQty,
  saveCart,
  updateCartQuantity,
  updateTotals
} from "../data/cart.js";
import { products } from "../data/products.js";
import { initMobileMenuToggle } from "./util.js";

const cartContainer = document.querySelector(".js-cart-items");
const subtotalEl = document.querySelector(".js-subtotal");
const taxesEl = document.querySelector(".js-taxes");
const totalEl = document.querySelector(".js-total");

function renderCart() {
  document.querySelector(".js-navbar").innerHTML = renderNavBarWithCartQty();

  if (cart.length === 0) {
    cartContainer.innerHTML = `
            <div class="text-center py-20 text-gray-500">
                <h2 class="text-2xl font-semibold mb-2">Your cart is empty</h2>
                <p>Add some products to your cart to see them here.</p>
            </div>
        `;
    subtotalEl.textContent = "$0.00";
    taxesEl.textContent = "$0.00";
    totalEl.textContent = "$0.00";
    updateCartQuantity();
    return;
  }

  let cartHtml = "";

  cart.forEach((cartItem, index) => {
    const product = products.find(p => p.id === cartItem.id);
    if (!product) return;

    cartHtml += `
      <div class="flex justify-between items-center js-cart-item" data-index="${index}">
        
        <!-- Product Info -->
        <div class="flex items-center gap-4">
          <img src="${product.images[0]}" alt="${product.name}" class="h-20 w-20 rounded object-cover">
          <div class="flex flex-col">
            <p class="font-semibold text-lg">${product.name}</p>
            <div><button class="js-remove border-r border-gray-300 pr-4" data-product-id="${product.id}">Remove</button>
            <button class="pl-4" > Save for Later</button></div>

          </div>
        </div>

        <!-- Price & Quantity -->
        <div class="flex flex-col items-end">
          <div class="font-semibold mb-2 text-gray-700">$${(product.price / 100).toFixed(2)}</div>
          <div class="flex items-center gap-2">
            <button class="px-3 py-1 shadow rounded js-decrease hover:bg-gray-300" data-product-id="${product.id}">-</button>
            <span class="text-lg">${cartItem.quantity}</span>
            <button class="px-3 py-1 shadow rounded js-increase hover:bg-gray-300" data-product-id="${product.id}">+</button>
          </div>
        </div>
      </div>
    `;
  });

  cartContainer.innerHTML = cartHtml;
  updateTotals(subtotalEl, taxesEl, totalEl);
  setupCartActions();
}

function setupCartActions() {
  // INCREASE QUANTITY
  document.querySelectorAll(".js-increase").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = Number(btn.dataset.productId);

      const cartItem = cart.find(item => item.id === productId);
      if (!cartItem) return;

      cartItem.quantity += 1;

      saveCart(cartItem)
      renderCart();
      updateCartQuantity();
    });
  });

  // DECREASE QUANTITY
  document.querySelectorAll(".js-decrease").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = Number(btn.dataset.productId);
      const cartItem = cart.find(item => item.id === productId);
      if (!cartItem) return;

      if (cartItem.quantity > 1) {
        cartItem.quantity -= 1;
      } else {
        cart.splice(cart.indexOf(cartItem), 1);
      }

      saveCart(cart)
      renderCart();
      updateCartQuantity();
    });
  });

  // REMOVE ITEM
  document.querySelectorAll(".js-remove").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = Number(btn.dataset.productId);
      const index = cart.findIndex(item => item.id === productId);
      if (index === -1) return;
      cart.splice(index, 1);

      saveCart(cart)
      renderCart();
      updateCartQuantity();
    });
  });
}

renderCart();
initMobileMenuToggle();
updateCartQuantity();
