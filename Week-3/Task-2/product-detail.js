const params = new URLSearchParams(window.location.search);
const productId = params.get("id");

const mainImage = document.getElementById("mainImage");
const thumbList = document.getElementById("thumbList");
const productName = document.getElementById("productName");
const productPrice = document.getElementById("productPrice");

const breadcrumbName = document.getElementById("breadcrumbName");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

const favBtn = document.getElementById("favBtn");
const favIcon = favBtn ? favBtn.querySelector("i") : null;

const minusBtn = document.getElementById("minusBtn");
const plusBtn = document.getElementById("plusBtn");
const qtyEl = document.getElementById("qty");
const addToCartBtn = document.getElementById("addToCartBtn");

let qty = 1;
let currentVariantId = null;

let variants = [];
let currentIndex = 0;

function getFavorites() {
  return JSON.parse(localStorage.getItem("favorites")) || [];
}
function setFavorites(favs) {
  localStorage.setItem("favorites", JSON.stringify(favs));
}
function isFavorited(id) {
  return getFavorites().includes(id);
}
function updateFavUI() {
  if (!favBtn || !favIcon || !productId) return;

  if (isFavorited(productId)) {
    favBtn.classList.add("active");
    favIcon.classList.remove("bi-heart");
    favIcon.classList.add("bi-heart-fill");
  } else {
    favBtn.classList.remove("active");
    favIcon.classList.remove("bi-heart-fill");
    favIcon.classList.add("bi-heart");
  }
}

if (favBtn) {
  favBtn.addEventListener("click", () => {
    if (!productId) return;
    let favs = getFavorites();

    if (favs.includes(productId)) {
      favs = favs.filter((x) => x !== productId);
    } else {
      favs.push(productId);
    }

    setFavorites(favs);
    updateFavUI();
  });
}

function money(amount, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(
    amount
  );
}

function setMainVariantByIndex(idx) {
  if (!variants.length) return;

  currentIndex = (idx + variants.length) % variants.length;
  const v = variants[currentIndex];

  currentVariantId = v.variantId;
  if (mainImage) mainImage.src = v.image;

  const buttons = thumbList ? thumbList.querySelectorAll(".thumb-btn") : [];
  buttons.forEach((b, i) => b.classList.toggle("active", i === currentIndex));
}

function renderProduct(p) {
  if (productName) productName.textContent = p.name;
  if (productPrice) productPrice.textContent = money(p.basePrice, p.currency);
  if (breadcrumbName) breadcrumbName.textContent = p.name; // breadcrumb like screenshot

  variants = p.variants || [];

  if (variants.length) {
    currentIndex = 0;
    currentVariantId = variants[0].variantId;
    if (mainImage) {
      mainImage.src = variants[0].image;
      mainImage.alt = p.name;
    }
  }

  if (thumbList) {
    thumbList.innerHTML = "";
    variants.forEach((v, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "thumb-btn";

      btn.style.width = "60px";
      btn.style.height = "60px";
      btn.style.borderRadius = "10px";
      btn.style.border = "1px solid #e5e5e5";
      btn.style.background = "#fff";
      btn.style.padding = "6px";

      btn.innerHTML = `<img src="${v.image}" alt="${v.color}" style="width:100%;height:100%;object-fit:contain;">`;

      btn.addEventListener("click", () => setMainVariantByIndex(idx));

      thumbList.appendChild(btn);
    });

    setMainVariantByIndex(0);
  }

  if (prevBtn)
    prevBtn.addEventListener("click", () =>
      setMainVariantByIndex(currentIndex - 1)
    );
  if (nextBtn)
    nextBtn.addEventListener("click", () =>
      setMainVariantByIndex(currentIndex + 1)
    );

  updateFavUI();
}

if (minusBtn) {
  minusBtn.addEventListener("click", () => {
    qty = Math.max(1, qty - 1);
    if (qtyEl) qtyEl.textContent = qty;
  });
}
if (plusBtn) {
  plusBtn.addEventListener("click", () => {
    qty += 1;
    if (qtyEl) qtyEl.textContent = qty;
  });
}

if (addToCartBtn) {
  addToCartBtn.addEventListener("click", () => {
    addToCart(productId, currentVariantId, qty);

    window.location.href = "./cart.html";
  });

  if (window.updateCartBadge) window.updateCartBadge();
}

fetch("./products.json")
  .then((r) => {
    if (!r.ok) throw new Error("Failed to load products.json");
    return r.json();
  })
  .then((products) => {
    const p = products.find((x) => x.id === productId);
    if (!p) {
      if (productName) productName.textContent = "Product not found";
      return;
    }
    renderProduct(p);
  })
  .catch((err) => {
    console.error(err);
    if (productName) productName.textContent = "Error loading product";
  });

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
}
