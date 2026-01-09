const productGrid = document.getElementById("productGrid");
const searchInput = document.getElementById("searchInput");
const priceRange = document.getElementById("priceRange");
const minPriceLabel = document.getElementById("minPriceLabel");
const maxPriceLabel = document.getElementById("maxPriceLabel");
const currentMax = document.getElementById("currentMax");

const sortBtn = document.getElementById("sortBtn");
const sortMenu = document.getElementById("sortMenu");

function money(amount, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(
    amount
  );
}

function getCart() {
  return JSON.parse(localStorage.getItem("cart")) || [];
}
function setCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
}
function addToCart(productId, variantId, qty = 1) {
  const cart = getCart();
  const found = cart.find(
    (x) => x.productId === productId && x.variantId === variantId
  );
  if (found) found.qty += qty;
  else cart.push({ productId, variantId, qty });
  setCart(cart);
  if (window.updateCartBadge) window.updateCartBadge();
}

function getFavorites() {
  return JSON.parse(localStorage.getItem("favorites")) || [];
}
function setFavorites(favs) {
  localStorage.setItem("favorites", JSON.stringify(favs));
}
function isFavorited(productId) {
  return getFavorites().includes(productId);
}

let ALL_PRODUCTS = [];
let sortMode = "featured";

let minPrice = 0;
let maxPrice = 0;

function renderProducts(products) {
  productGrid.innerHTML = "";

  if (!products.length) {
    productGrid.innerHTML = `<div class="col-12 text-muted">No products found.</div>`;
    return;
  }

  products.forEach((p) => {
    const v0 = p.variants?.[0];
    const favActive = isFavorited(p.id);

    const col = document.createElement("div");
    col.className = "col-6 col-md-4 col-lg-4 col-xl-3 product";
    col.dataset.name = p.name.toLowerCase();
    col.dataset.category = (p.category || "").toLowerCase();
    col.dataset.price = String(p.basePrice);

    col.innerHTML = `
      <div class="card border-0 h-100">
        <div class="position-relative bg-light p-3 text-center" style="height: 200px">
          <img
            src="${v0?.image || ""}"
            class="img-fluid h-100 product-img"
            style="object-fit: contain"
            alt="${p.name}"
          />

          <!-- Favorite button (shows on hover if your CSS does that) -->
          <button
            type="button"
            class="btn btn-light position-absolute top-0 end-0 m-2 fav-btn ${
              favActive ? "active" : ""
            }"
            data-product-id="${p.id}"
            aria-label="Favorite"
          >
            <i class="bi ${favActive ? "bi-heart-fill" : "bi-heart"}"></i>
          </button>
        </div>

        <div class="card-body px-0 d-flex flex-column">
          <div class="small">${p.name}</div>
          <div class="fw-semibold mb-2">${money(p.basePrice, p.currency)}</div>

          <!-- Variants -->
          <div class="d-flex gap-2 mb-3">
            ${(p.variants || [])
              .map(
                (v) => `
                  <button
                    type="button"
                    class="variant-dot border rounded-circle p-0"
                    title="${v.color} (stock: ${v.stock})"
                    data-product-id="${p.id}"
                    data-variant-id="${v.variantId}"
                    data-image="${v.image}"
                    style="width:16px;height:16px;background:${v.colorCode};"
                  ></button>
                `
              )
              .join("")}
          </div>

          <!-- Buttons -->
          <div class="mt-auto d-flex gap-2">
            <button
              class="btn btn-outline-dark btn-sm w-50 view-details-btn"
              data-product-id="${p.id}"
            >
              View Details
            </button>

            <button
              class="btn btn-dark btn-sm w-50 add-to-cart-btn"
              data-product-id="${p.id}"
              data-variant-id="${v0?.variantId || ""}"
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    `;

    productGrid.appendChild(col);
  });
}

function applyFiltersAndRender() {
  const query = (searchInput?.value || "").trim().toLowerCase();
  const maxAllowed = Number(priceRange?.value ?? maxPrice);

  let list = [...ALL_PRODUCTS];

  if (query) {
    list = list.filter((p) => {
      const name = (p.name || "").toLowerCase();
      const cat = (p.category || "").toLowerCase();
      return name.includes(query) || cat.includes(query);
    });
  }

  list = list.filter((p) => Number(p.basePrice) <= maxAllowed);

  if (sortMode === "low") {
    list.sort((a, b) => a.basePrice - b.basePrice);
  } else if (sortMode === "high") {
    list.sort((a, b) => b.basePrice - a.basePrice);
  } else {
  }

  if (currentMax) currentMax.textContent = money(maxAllowed);
  renderProducts(list);
}

productGrid.addEventListener("click", (e) => {
  const dot = e.target.closest(".variant-dot");
  if (dot) {
    const card = dot.closest(".card");
    const img = card.querySelector(".product-img");
    const addBtn = card.querySelector(".add-to-cart-btn");

    img.src = dot.dataset.image;
    if (addBtn) addBtn.dataset.variantId = dot.dataset.variantId;
    return;
  }

  const favBtn = e.target.closest(".fav-btn");
  if (favBtn) {
    const productId = favBtn.dataset.productId;
    let favs = getFavorites();
    const icon = favBtn.querySelector("i");

    if (favs.includes(productId)) {
      favs = favs.filter((id) => id !== productId);
      favBtn.classList.remove("active");
      icon.classList.remove("bi-heart-fill");
      icon.classList.add("bi-heart");
    } else {
      favs.push(productId);
      favBtn.classList.add("active");
      icon.classList.remove("bi-heart");
      icon.classList.add("bi-heart-fill");
    }

    setFavorites(favs);
    return;
  }

  const viewBtn = e.target.closest(".view-details-btn");
  if (viewBtn) {
    const productId = viewBtn.dataset.productId;
    window.location.href = `product-detail.html?id=${productId}`;
    return;
  }

  const cartBtn = e.target.closest(".add-to-cart-btn");
  if (cartBtn) {
    addToCart(cartBtn.dataset.productId, cartBtn.dataset.variantId, 1);
    return;
  }
});

if (searchInput) {
  searchInput.addEventListener("input", applyFiltersAndRender);
}

if (priceRange) {
  priceRange.addEventListener("input", applyFiltersAndRender);
}

if (sortMenu && sortBtn) {
  sortMenu.addEventListener("click", (e) => {
    const item = e.target.closest(".sort-item");
    if (!item) return;
    e.preventDefault();

    sortMode = item.dataset.sort;

    sortMenu
      .querySelectorAll(".sort-item")
      .forEach((a) => a.classList.remove("active"));
    item.classList.add("active");

    sortBtn.textContent = `Sort By: ${item.textContent.trim()}`;

    applyFiltersAndRender();
  });
}

fetch("./products.json")
  .then((r) => {
    if (!r.ok) throw new Error("Failed to load products.json");
    return r.json();
  })
  .then((products) => {
    ALL_PRODUCTS = products;

    const prices = products.map((p) => Number(p.basePrice));
    minPrice = Math.min(...prices);
    maxPrice = Math.max(...prices);

    if (priceRange) {
      priceRange.min = String(minPrice);
      priceRange.max = String(maxPrice);
      priceRange.value = String(maxPrice);
    }
    if (minPriceLabel) minPriceLabel.textContent = money(minPrice);
    if (maxPriceLabel) maxPriceLabel.textContent = money(maxPrice);
    if (currentMax) currentMax.textContent = money(maxPrice);

    applyFiltersAndRender();
  })
  .catch((err) => {
    console.error(err);
    productGrid.innerHTML = `<div class="col-12 text-danger">Could not load products.</div>`;
  });
