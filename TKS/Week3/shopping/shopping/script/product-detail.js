import { products } from "../data/products.js";
import { cart, addToCart, updateCartQuantity, renderNavBarWithCartQty } from "../data/cart.js";
import { initMobileMenuToggle } from "./util.js";

const params = new URLSearchParams(window.location.search);
const productId = Number(params.get("id"));
const product = products.find(p => p.id === productId);
let productInCart = cart.find(p => p.id === productId);

if (!product) {
  alert("Product not found!");
  window.location.href = "index.html";
}

const colorImages = product.images;

const html = `
  ${renderNavBarWithCartQty()}
  <div class="p-6 md:p-20 js-product-detail-container">
    <h2 class="text-gray-600 font-bold mb-4">
      All Products / ${product.name}
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-7xl mx-auto">

      <!-- LEFT -->
      <div class="flex gap-4">
        <div class="flex flex-col gap-2 w-20">
          ${colorImages.map(
  img => `
              <img
                src="${img}"
                class="w-full h-20 object-cover rounded cursor-pointer js-color-thumb"
              />
            `
).join("")}
        </div>

        <div class="flex-1 flex justify-center items-center">
          <img
            src="${product.images[0]}"
            class="js-product-image w-full max-w-[420px] h-[420px] object-cover rounded"
          />
        </div>
      </div>

      <!-- RIGHT -->
      <div class="space-y-6">
        <div>
          <h1 class="text-3xl font-semibold">${product.name}</h1>
          <p class="text-2xl font-bold">
            $${(product.price / 100).toFixed(2)}
          </p>
        </div>

        <div class="flex items-center gap-3">
          <button class="js-minus w-10 h-10 border rounded">−</button>
          <span class="js-qty font-semibold">
            ${productInCart ? productInCart.quantity : 1}
          </span>
          <button class="js-plus w-10 h-10 border rounded">+</button>

          <button class="js-add-cart px-6 py-2 rounded bg-[#714e62] text-white">
            Add to Cart
          </button>
        </div>

        <div class="pt-4 border-t text-sm text-gray-600 space-y-1">
          ${product.terms.map(t => `<p>• ${t}</p>`).join("")}
        </div>
      </div>
    </div>
  </div>
`;

document.querySelector(".js-product-details").innerHTML = html;

updateCartQuantity();

let qty = productInCart ? productInCart.quantity : 1;
const qtyEl = document.querySelector(".js-qty");

document.querySelector(".js-plus").onclick = () => {
  qty++;
  qtyEl.textContent = qty;

};

document.querySelector(".js-minus").onclick = () => {
  if (qty > 1) {
    qty--;
    qtyEl.textContent = qty;

  }
};

document.querySelector(".js-add-cart").onclick = () => {
  addToCart(productId, qty);
};

document.querySelectorAll(".js-color-thumb").forEach(thumb => {
  thumb.addEventListener("click", () => {
    document.querySelector(".js-product-image").src = thumb.src;

    document
      .querySelectorAll(".js-color-thumb")
      .forEach(t => t.classList.remove("ring-2", "ring-indigo-600"));

    thumb.classList.add("ring-2", "ring-indigo-600");
  });
});

initMobileMenuToggle();