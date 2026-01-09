
let products = [];
let cart = JSON.parse(localStorage.getItem("cart")) || [];
console.log(cart)
// products → products.json ထဲက product အားလုံးကို သိမ်းမယ့် array
// cart → localStorage ထဲမှာရှိပြီးသား cart data ကို ပြန်ဖတ်တယ်
// localStorage ထဲ cart မရှိရင် [] (အလွတ် array) သုံးမယ်
// console.log(cart) → browser console မှာ cart ကို စစ်ကြည့်ဖို့




fetch("products.json")
  .then(res => res.json())
  .then(data => {
    products = data;
    displayProducts(products);
  });
// products.json ဖိုင်က data ကို fetch လုပ်တယ်
// JSON ပြောင်းပြီး products array ထဲသိမ်းတယ်
// displayProducts() ကိုခေါ်ပြီး UI ပေါ်မှာ ပြတယ်


function displayProducts(items) {

  const productList = document.getElementById("productList");
  if (!productList) return;

  productList.innerHTML = "";

  items.forEach(p => {
    productList.innerHTML += `
      <div class="col-md-4 mb-4">
        <div class="card p-3 text-center">

          <div class="img-container position-relative">
            <img src="${p.image}" class="img-fluid" alt="">
            <button class="btn btn-info btn-sm view-desc-btn"
              data-bs-toggle="modal" data-bs-target="#descModal"
              onclick="showDescription('${p.name}', '${p.description}')">
              View Description
            </button>
          </div>

          <h6 class="mt-2">${p.name}</h6>
          <p class="price">$ ${p.price}</p>

          <div class="d-flex align-items-center justify-content-center mb-2">
            <button class="btn btn-outline-secondary btn-sm me-2"
              onclick="changeQtyInput(${p.id}, -1)">−</button>

            <input type="number" id="qty-${p.id}"
              class="form-control text-center"
              value="1" min="1" style="width:60px;">

            <button class="btn btn-outline-secondary btn-sm ms-2"
              onclick="changeQtyInput(${p.id}, 1)">+</button>
          </div>

          <button class="btn btn-dark btn-sm"
            onclick="addToCart(${p.id})">
            Add to Cart
          </button>

        </div>
      </div>
    `;
  });
}

/*QTY INPUT CONTROL*/
function changeQtyInput(id, delta) {
  const input = document.getElementById(`qty-${id}`);
  input.value = Math.max(1, parseInt(input.value) + delta);
}

/*ADD TO CART (CORRECT)*/
function addToCart(id) {
  const product = products.find(p => p.id === id);
  const qty = parseInt(document.getElementById(`qty-${id}`).value);

  const existIndex = cart.findIndex(item => item.id === id);

  if (existIndex >= 0) {
    cart[existIndex].qty += qty;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      price: product.price,
      qty: qty,
      image: product.image
    });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  alert("Added to cart ✅");
}

/*SEARCH*/
const searchInput = document.getElementById("search");
if (searchInput) {
  searchInput.addEventListener("input", e => {
    const value = e.target.value.toLowerCase();
    const filtered = products.filter(p =>
      p.name.toLowerCase().includes(value)
    );
    displayProducts(filtered);
  });
}

/*PRICE FILTER*/
const priceRange = document.getElementById("priceRange");
if (priceRange) {
  priceRange.addEventListener("input", e => {
    document.getElementById("priceValue").innerText = e.target.value;
    const filtered = products.filter(p => p.price <= e.target.value);
    displayProducts(filtered);
  });
}

/*MODAL DESCRIPTION*/
function showDescription(name, description) {
  document.getElementById("modalTitle").innerText = name;
  document.getElementById("modalBody").innerText = description;
}

/*CART PAGE*/
function renderCart() {
  const container = document.getElementById("cartItems");
  if (!container) return;

  container.innerHTML = "";

  if (cart.length === 0) {
    container.innerHTML = "<p>Your cart is empty 🛒</p>";
    updateSummary();
    return;
  }

  cart.forEach((item, index) => {
    container.innerHTML += `
      <div class="d-flex align-items-center mb-4 border-bottom pb-3">
        <img src="${item.image}" width="80" class="me-3">

        <div class="flex-grow-1">
          <h6>${item.name}</h6>
          <small>$${item.price}</small>
        </div>

        <div class="d-flex align-items-center">
          <button class="btn btn-outline-secondary btn-sm"
            onclick="changeCartQty(${index}, -1)">−</button>

          <span class="mx-3">${item.qty}</span>

          <button class="btn btn-outline-secondary btn-sm"
            onclick="changeCartQty(${index}, 1)">+</button>
        </div>

        <div class="ms-4 fw-bold">
          $${item.price * item.qty}
        </div>

        <button class="btn btn-link text-danger ms-3"
          onclick="removeItem(${index})">Remove</button>
      </div>
    `;
  });

  updateSummary();
}

function changeCartQty(index, delta) {
  cart[index].qty = Math.max(1, cart[index].qty + delta);
  localStorage.setItem("cart", JSON.stringify(cart));
  renderCart();
}

function removeItem(index) {
  cart.splice(index, 1);
  localStorage.setItem("cart", JSON.stringify(cart));
  renderCart();
}

function updateSummary() {
  console.log(cart);

  const subtotal = cart.reduce(
    (sum, item) => sum + Number(item.price) * Number(item.qty),
    0
  );

  console.log(subtotal);

  const tax = subtotal * 0.15;
  const total = subtotal + tax;

  document.getElementById("subtotal").innerText = `$${subtotal.toFixed(2)}`;
  document.getElementById("tax").innerText = `$${tax.toFixed(2)}`;
  document.getElementById("total").innerText = `$${total.toFixed(2)}`;
}


/*INIT CART PAGE*/
if (document.getElementById("cartItems")) {
  renderCart();
}
/*CHECKOUT REDIRECT*/
function goToCheckout() {
  if (cart.length === 0) {
    alert("Your cart is empty!");
    return;
  }
  window.location.href = "checkout.html";
}

  /*CHECKOUT PAGE FUNCTIONS*/
  function renderCheckoutItems() {
    const container = document.getElementById("checkoutOrderItems");
    if (!container) return;
    
    container.innerHTML = "";
    
    let subtotal = 0;
    
    cart.forEach(item => {
      const itemTotal = item.price * item.qty;
      subtotal += itemTotal;
      
      container.innerHTML += `
        <div class="order-item">
          <div class="d-flex justify-content-between">
            <span>${item.qty} × ${item.name}</span>
            <span>$${itemTotal.toFixed(2)}</span>
          </div>
        </div>
      `;
    });
    
    const deliveryFee = 10.00;
    const tax = subtotal * 0.15;
    const total = subtotal + tax + deliveryFee;
    
    document.getElementById("checkoutSubtotal").textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById("checkoutTax").textContent = `$${tax.toFixed(2)}`;
    document.getElementById("checkoutTotal").textContent = `$${total.toFixed(2)}`;
    
    // Update page title with item count
    document.title = `Checkout (${cart.length} items) - Your Store`;
  }
  
  function processCheckout() {
    // Basic form validation
    const form = document.getElementById("checkoutForm");
    const requiredFields = form.querySelectorAll('[required]');
    let valid = true;
    
    requiredFields.forEach(field => {
      if (!field.value.trim()) {
        valid = false;
        field.classList.add('is-invalid');
      } else {
        field.classList.remove('is-invalid');
      }
    });
    
    if (!valid) {
      alert("Please fill in all required fields (*)");
      return;
    }
    
    if (cart.length === 0) {
      alert("Your cart is empty!");
      return;
    }
    
    // Here you would typically send data to a server
    // For now, we'll just show a success message
    alert("Order confirmed! Thank you for your purchase.");
    
    // Clear cart
    cart = [];
    localStorage.setItem("cart", JSON.stringify(cart));
    
    // Redirect to home or confirmation page
    setTimeout(() => {
      window.location.href = "home.html";
    }, 1000);
  }
  
  // Initialize checkout page
  if (document.getElementById("checkoutOrderItems")) {
    if (cart.length === 0) {
      // If cart is empty, redirect back to cart page
      setTimeout(() => {
        alert("Your cart is empty!");
        window.location.href = "cart.html";
      }, 500);
    } else {
      renderCheckoutItems();
    }
  }
