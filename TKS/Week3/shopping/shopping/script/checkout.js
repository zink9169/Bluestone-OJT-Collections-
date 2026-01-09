import {
  cart,
  updateTotals,
  updateCartQuantity,
  renderNavBarWithCartQty
} from "../data/cart.js";
import { products } from "../data/products.js";
import { initMobileMenuToggle } from "./util.js";

const cartContainer = document.querySelector(".js-cart-items");
const subtotalEl = document.querySelector(".js-subtotal");
const taxesEl = document.querySelector(".js-taxes");
const totalEl = document.querySelector(".js-total");
const checkoutBtn = document.querySelector(".js-checkout");

function renderNavbar() {
  document.querySelector(".js-navbar").innerHTML = renderNavBarWithCartQty();
}

const fields = [
  { id: "name", message: "Name is required" },
  { id: "email", message: "Valid email is required", type: "email" },
  { id: "phone", message: "Phone is required" },
  { id: "street", message: "Street is required" },
  { id: "city", message: "City is required" },
  { id: "country", message: "Country is required" }
];

function showError(input, message) {
  input.classList.add("border-red-500");
  const error = input.nextElementSibling;
  error.textContent = message;
  error.classList.remove("hidden");
}

function clearError(input) {
  input.classList.remove("border-red-500");
  const error = input.nextElementSibling;
  error.classList.add("hidden");
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

checkoutBtn.addEventListener("click", (e) => {
  e.preventDefault();
  let hasError = false;

  fields.forEach(field => {
    const input = document.getElementById(field.id);
    const value = input.value.trim();

    if (!value) {
      showError(input, field.message);
      hasError = true;
      return;
    }

    if (field.type === "email" && !isValidEmail(value)) {
      showError(input, "Email format is invalid");
      hasError = true;
      return;
    }

    clearError(input);
  });

  if (!hasError) {
    alert("✅ Order confirmed successfully!");
  }
});

fields.forEach(field => {
  const input = document.getElementById(field.id);
  input.addEventListener("input", () => clearError(input));
});

function renderCart() {
  renderNavbar();

  if (cart.length === 0) {
    cartContainer.innerHTML = `
      <p class="text-center text-gray-500 py-6">
        Your cart is empty
      </p>
    `;
    updateTotals(subtotalEl, taxesEl, totalEl);
    return;
  }

  let cartHtml = "";

  cart.forEach(item => {
    const product = products.find(p => p.id === item.id);
    if (!product) return;

    cartHtml += `
      <div class="flex gap-3 items-center">
        <div class="relative">
          <img
            src="${product.images[0]}"
            alt="${product.name}"
            class="w-16 h-16 rounded object-cover"
          />
          <span
            class="absolute -top-2 -right-2 bg-[#714e62] text-white text-xs
                   w-6 h-6 rounded-full flex items-center justify-center font-bold"
          >
            ${item.quantity}
          </span>
        </div>

        <div class="flex-1">
          <p class="font-semibold">${product.name}</p>
          <p class="text-sm text-gray-500">
            $${(product.price / 100).toFixed(2)} each
          </p>
        </div>

        <p class="font-semibold">
          $${((product.price / 100) * item.quantity).toFixed(2)}
        </p>
      </div>
    `;
  });

  cartContainer.innerHTML = cartHtml;
  updateTotals(subtotalEl, taxesEl, totalEl);
}

renderCart();
initMobileMenuToggle();
updateCartQuantity();
