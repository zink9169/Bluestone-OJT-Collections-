const products = [
  { id: 1, name: "Laptop", price: 10000 },
  { id: 2, name: "Mouse", price: 50 },
  { id: 3, name: "Keyboard", price: 100 },
];

const productSelect = document.getElementById("productSelect");
const quantityInput = document.getElementById("quantityInput");
const quantityError = document.getElementById("quantityError");
const discountInput = document.getElementById("discountInput");
const addBtn = document.getElementById("addBtn");
const tableBody = document.getElementById("tableBody");
const overallTotalCell = document.getElementById("overallTotal");

products.forEach((product) => {
  const option = document.createElement("option");
  option.value = product.id;
  option.textContent = product.name;
  productSelect.appendChild(option);
});

quantityInput.addEventListener("input", () => {
  const value = Number(quantityInput.value);
  quantityError.style.display = value <= 0 ? "inline" : "none";
});

function recalcOverallTotal() {
  let total = 0;
  document.querySelectorAll("#tableBody tr").forEach((row) => {
    total += Number(row.children[4].textContent);
  });
  overallTotalCell.textContent = total.toFixed(2);
}

addBtn.addEventListener("click", () => {
  const productId = Number(productSelect.value);
  const quantity = Number(quantityInput.value);
  const discount = Number(discountInput.value) || 0;

  if (!productId) {
    alert("Please select a product");
    return;
  }

  if (quantity <= 0) {
    quantityError.style.display = "inline";
    return;
  }

  if (discount < 0 || discount > 100 || isNaN(discount)) {
    alert("Discount must be a number between 0 and 100");
    return;
  }

  const product = products.find((p) => p.id === productId);

  let existingRow = Array.from(tableBody.querySelectorAll("tr")).find((row) => {
    return (
      Number(row.getAttribute("data-id")) === productId &&
      Number(row.getAttribute("data-discount")) === discount
    );
  });

  const rowTotal = product.price * quantity * (1 - discount / 100);

  if (existingRow) {
    const qtyCell = existingRow.children[1];
    const totalCell = existingRow.children[4];

    const newQty = Number(qtyCell.textContent) + quantity;
    const newTotal = product.price * newQty * (1 - discount / 100);

    qtyCell.textContent = newQty;
    totalCell.textContent = newTotal.toFixed(2);
  } else {
    const row = document.createElement("tr");
    row.setAttribute("data-id", productId);
    row.setAttribute("data-discount", discount);

    row.innerHTML = `
      <td>${product.name}</td>
      <td>${quantity}</td>
      <td>${product.price}</td>
      <td>${discount}%</td>
      <td>${rowTotal.toFixed(2)}</td>
    `;

    tableBody.appendChild(row);
  }

  recalcOverallTotal();

  productSelect.value = "";
  quantityInput.value = "";
  discountInput.value = "";
  quantityError.style.display = "none";
});
