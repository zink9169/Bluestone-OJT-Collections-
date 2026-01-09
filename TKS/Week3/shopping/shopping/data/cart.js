import { products } from "./products.js";


const storedCart = JSON.parse(localStorage.getItem("cart"));
export const cart = Array.isArray(storedCart) ? storedCart : [];

console.log(cart)
export function renderNavBarWithCartQty() {
  return `
  <nav class="bg-white shadow fixed w-full z-50">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between items-center h-16">

        <!-- Logo + Menu -->
        <div class="flex items-center space-x-8">
          <div class="text-xl font-bold text-indigo-600">MyApp</div>
          <ul class="hidden md:flex space-x-6 text-gray-700 font-medium">
            <li><a href="http://127.0.0.1:5500/shopping/home.html" class="hover:text-indigo-600">Home</a></li>
            <li><a href="#" class="hover:text-indigo-600">Shop</a></li>
            <li><a href="#" class="hover:text-indigo-600">Contact Us</a></li>
          </ul>
        </div>

        <!-- Icons -->
        <div class="flex items-center space-x-3 text-gray-700">

          <!-- Cart -->
        <div class="relative">
            <a href="cart.html" class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-100 hover:bg-indigo-100 text-gray-700">
              <i class="bi bi-cart text-lg"></i>
            </a>
            <span
              class="js-cart-quantity absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center rounded-full text-xs font-semibold bg-[#714e62] text-white">
              0
            </span>
          </div>
          <!-- Search -->
          <button
            class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-100 hover:bg-indigo-100 text-gray-700">
            <i class="bi bi-search"></i>
          </button>

          <!-- Phone (Desktop) -->
          <div class="hidden md:flex items-center space-x-2 font-medium">
            <span
              class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-100 hover:bg-indigo-100 text-gray-700">
              <i class="bi bi-telephone"></i>
            </span>
            <a href="tel:+1234567890" class="hover:text-indigo-600">+123 456 7890</a>
          </div>

          <!-- Contact Button (Desktop) -->
          <a href="#contact"
            class="hidden md:inline-flex items-center justify-center px-4 py-2 rounded-md bg-[#714e62] text-white text-sm hover:bg-[#5f4052] transition">
            Contact Us
          </a>

         <!-- Mobile Menu Button -->
          <button id="menu-btn"
            class="md:hidden w-10 h-10 flex items-center justify-center rounded-full bg-gray-100">
            <i class="bi bi-list text-xl"></i>
          </button>
          <!-- Mobile Menu (hidden by default) -->
           
            <div class="js-mobile-menu hidden fixed top-0 w-1/2 bg-white shadow p-4 space-y-2 z-40">
              <a href="home.html" class="block hover:text-indigo-600">Home</a>
              <a href="#" class="block hover:text-indigo-600">Shop</a>
              <a href="#" class="block hover:text-indigo-600">Contact Us</a>
            </div>


        </div>
      </div>
    </div>
  </nav>
  `;
}

export function saveCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
}

export function updateCartQuantity() {
  const totalQuantity = cart.reduce((sum, item) => {
    return sum + item.quantity;
  }, 0);

  const qtyEl = document.querySelector(".js-cart-quantity");
  if (qtyEl) {
    qtyEl.textContent = totalQuantity;
  }
}

export function addToCart(productId, quantity = 1) {
  const existing = cart.find(p => p.id === productId);

  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.push({ id: productId, quantity });
  }

  saveCart(cart)
  updateCartQuantity();
}

export function updateTotals(subtotalEl, taxesEl, totalEl) {
  let subtotal = 0;

  cart.forEach(item => {
    const product = products.find(p => p.id === item.id);
    if (!product) return;
    subtotal += (product.price / 100) * item.quantity;
  });

  const taxes = subtotal * 0.1;
  const total = subtotal + taxes;

  if (subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
  if (taxesEl) taxesEl.textContent = `$${taxes.toFixed(2)}`;
  if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;
}