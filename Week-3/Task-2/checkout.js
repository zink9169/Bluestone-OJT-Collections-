function getCart() {
  return JSON.parse(localStorage.getItem("cart")) || [];
}

function money(amount, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(
    amount
  );
}

const form = document.getElementById("checkoutForm");
const sumItems = document.getElementById("sumItems");
const sumSubtotal = document.getElementById("sumSubtotal");
const sumTotal = document.getElementById("sumTotal");

// load products to compute subtotal correctly
let PRODUCTS = [];

function findProduct(productId) {
  return PRODUCTS.find((p) => p.id === productId);
}

function computeSummary() {
  const cart = getCart();

  const items = cart.reduce((s, it) => s + (it.qty || 0), 0);

  let subtotal = 0;
  cart.forEach((it) => {
    const p = findProduct(it.productId);
    const price = p?.basePrice ?? 0;
    subtotal += price * (it.qty || 0);
  });

  sumItems.textContent = String(items);
  sumSubtotal.textContent = money(subtotal);
  sumTotal.textContent = money(subtotal);
}

function normalizeCardNumber(value) {
  return value.replace(/\D/g, ""); // keep digits only
}

function isFilled(value) {
  return String(value || "").trim().length > 0;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const fd = new FormData(form);
  const data = Object.fromEntries(fd.entries());

  // Basic required validation (demo)
  const requiredFields = [
    "fullName",
    "phone",
    "email",
    "address",
    "city",
    "country",
    "cardNumber",
    "expiry",
    "cvc",
    "cardName",
  ];

  const missing = requiredFields.filter((k) => !isFilled(data[k]));
  if (missing.length) {
    alert("Please fill in all fields.");
    return;
  }

  // Simple extra checks (demo-level)
  const cardDigits = normalizeCardNumber(data.cardNumber);
  if (cardDigits.length < 12) {
    alert("Card number looks too short.");
    return;
  }
  if (!/^\d{2}\/\d{2}$/.test(data.expiry)) {
    alert("Expiry must be in MM/YY format.");
    return;
  }
  if (!/^\d{3,4}$/.test(String(data.cvc).trim())) {
    alert("CVC must be 3 or 4 digits.");
    return;
  }

  const cart = getCart();
  if (!cart.length) {
    alert("Your cart is empty.");
    return;
  }

  alert("Payment successful  Thank you for your order!");

  localStorage.removeItem("cart");
  if (window.updateCartBadge) window.updateCartBadge();

  
  window.location.href = "./home.html";
});

fetch("./products.json")
  .then((r) => r.json())
  .then((products) => {
    PRODUCTS = products;
    computeSummary();
  })
  .catch(() => {

    computeSummary();
  });
