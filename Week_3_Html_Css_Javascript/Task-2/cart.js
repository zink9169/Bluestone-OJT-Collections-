const cartList = document.getElementById("cartList");
const emptyState = document.getElementById("emptyState");

const itemsCountEl = document.getElementById("itemsCount");
const subTotalEl = document.getElementById("subTotal");
const totalEl = document.getElementById("total");
const checkoutBtn = document.getElementById("checkoutBtn");

function getCart() {
  return JSON.parse(localStorage.getItem("cart")) || [];
}
function setCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
}
function money(amount, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(
    amount
  );
}


let PRODUCTS = [];

function findProduct(productId) {
  return PRODUCTS.find((p) => p.id === productId);
}
function findVariant(product, variantId) {
  return (product?.variants || []).find((v) => v.variantId === variantId);
}

function renderCart() {
  const cart = getCart();
  cartList.innerHTML = "";

  if (!cart.length) {
    emptyState.classList.remove("d-none");
    itemsCountEl.textContent = "0";
    subTotalEl.textContent = money(0);
    totalEl.textContent = money(0);
    return;
  }

  emptyState.classList.add("d-none");

  let itemsCount = 0;
  let subtotal = 0;

  cart.forEach((item) => {
    const product = findProduct(item.productId);
    const variant = findVariant(product, item.variantId);

    const name = product?.name || item.productId;
    const price = product?.basePrice ?? 0;
    const currency = product?.currency || "USD";
    const image = variant?.image || "";
    const color = variant?.color || "";

    itemsCount += item.qty;
    subtotal += price * item.qty;

    const row = document.createElement("div");
    row.className = "card border-0 shadow-sm";
    row.innerHTML = `
      <div class="card-body">
        <div class="d-flex gap-3">
          <div class="bg-light rounded p-2" style="width:90px;height:90px;display:grid;place-items:center;">
            <img src="${image}" alt="${name}" style="max-width:100%;max-height:100%;object-fit:contain;">
          </div>

          <div class="flex-grow-1">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <div class="fw-semibold">${name}</div>
                <div class="small text-muted">Variant: ${
                  color || item.variantId
                }</div>
                <div class="small text-muted">Unit: ${money(
                  price,
                  currency
                )}</div>
              </div>

              <button class="btn btn-outline-danger btn-sm remove-btn"
                data-product-id="${item.productId}"
                data-variant-id="${item.variantId}">
                <i class="bi bi-trash"></i>
              </button>
            </div>

            <div class="d-flex align-items-center justify-content-between mt-3">
              <div class="d-inline-flex align-items-center border rounded overflow-hidden">
                <button class="btn btn-light btn-sm px-3 dec-btn"
                  data-product-id="${item.productId}"
                  data-variant-id="${item.variantId}">-</button>

                <span class="px-3 fw-semibold">${item.qty}</span>

                <button class="btn btn-light btn-sm px-3 inc-btn"
                  data-product-id="${item.productId}"
                  data-variant-id="${item.variantId}">+</button>
              </div>

              <div class="fw-semibold">
                ${money(price * item.qty, currency)}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    cartList.appendChild(row);
  });

  itemsCountEl.textContent = String(itemsCount);
  subTotalEl.textContent = money(subtotal);
  totalEl.textContent = money(subtotal);
}

function changeQty(productId, variantId, delta) {
  const cart = getCart();
  const idx = cart.findIndex(
    (x) => x.productId === productId && x.variantId === variantId
  );
  if (idx === -1) return;

  cart[idx].qty += delta;
  if (cart[idx].qty <= 0) cart.splice(idx, 1);

  setCart(cart);
  renderCart();
  if (window.updateCartBadge) window.updateCartBadge();
}

function removeItem(productId, variantId) {
  let cart = getCart();
  cart = cart.filter(
    (x) => !(x.productId === productId && x.variantId === variantId)
  );
  setCart(cart);
  renderCart();

  if (window.updateCartBadge) window.updateCartBadge();
}

cartList.addEventListener("click", (e) => {
  const inc = e.target.closest(".inc-btn");
  if (inc) return changeQty(inc.dataset.productId, inc.dataset.variantId, +1);

  const dec = e.target.closest(".dec-btn");
  if (dec) return changeQty(dec.dataset.productId, dec.dataset.variantId, -1);

  const rm = e.target.closest(".remove-btn");
  if (rm) return removeItem(rm.dataset.productId, rm.dataset.variantId);
});


fetch("./products.json")
  .then((r) => r.json())
  .then((products) => {
    PRODUCTS = products;
    renderCart();
  })
  .catch((err) => {
    console.error(err);
    renderCart();
  });
