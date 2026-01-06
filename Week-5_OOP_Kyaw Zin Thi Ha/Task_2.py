from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional



@dataclass
class Product:
    product_id: int
    name: str
    price: float
    stock: int

    def restock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Restock quantity must be > 0.")
        self.stock += qty

    def reduce_stock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Quantity must be > 0.")
        if qty > self.stock:
            raise ValueError("Not enough stock.")
        self.stock -= qty


class ProductCatalog:


    def __init__(self) -> None:
        self._products: Dict[int, Product] = {}
        self._next_id: int = 1

    def add_product(self, name: str, price: float, stock: int) -> Product:
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price <= 0:
            raise ValueError("Price must be > 0.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        p = Product(product_id=self._next_id, name=name.strip(), price=price, stock=stock)
        self._products[p.product_id] = p
        self._next_id += 1
        return p

    def get(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def all_products(self) -> Dict[int, Product]:
        return dict(self._products)

    def update_stock(self, product_id: int, new_stock: int) -> None:
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        p = self.get(product_id)
        if not p:
            raise ValueError("Product not found.")
        p.stock = new_stock




class User:
    def __init__(self, username: str) -> None:
        self.username = username

    @property
    def role(self) -> str:
        return "User"


class Admin(User):
    @property
    def role(self) -> str:
        return "Admin"


class Customer(User):
    def __init__(self, username: str) -> None:
        super().__init__(username)
        self.cart = ShoppingCart()

    @property
    def role(self) -> str:
        return "Customer"




class ShoppingCart:
    def __init__(self) -> None:
        
        self._items: Dict[int, int] = {}

    def add_item(self, product: Product, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Quantity must be > 0.")
        if qty > product.stock:
            raise ValueError("Not enough stock available.")
        self._items[product.product_id] = self._items.get(product.product_id, 0) + qty

    def remove_item(self, product_id: int, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Quantity must be > 0.")
        if product_id not in self._items:
            raise ValueError("Item not in cart.")

        current = self._items[product_id]
        if qty >= current:
            del self._items[product_id]
        else:
            self._items[product_id] = current - qty

    def clear(self) -> None:
        self._items.clear()

    def items(self) -> Dict[int, int]:
        return dict(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0



class ECommerceApp:
    def __init__(self) -> None:
        self.catalog = ProductCatalog()
        self.catalog.add_product("Laptop", 1200.0, 5)
        self.catalog.add_product("Headphones", 75.0, 20)
        self.catalog.add_product("Mouse", 25.0, 30)

    def run(self) -> None:
        while True:
            print("\nAre you an Admin or Customer?")
            print("1. Admin")
            print("2. Customer")
            print("3. Exit")

            choice = self._read_int("Choose: ")
            if choice == 1:
                self._admin_flow()
            elif choice == 2:
                self._customer_flow()
            elif choice == 3:
                print("Goodbye.")
                return
            else:
                print("Invalid option.")



    def _admin_flow(self) -> None:
        admin = Admin(username="admin")

        while True:
            print(f"\n(Admin Menu) - Logged in as: {admin.username}")
            print("1. Add Product")
            print("2. Update Product Stock")
            print("3. View Products")
            print("4. Logout")

            choice = self._read_int("Choose: ")
            try:
                if choice == 1:
                    self._admin_add_product()
                elif choice == 2:
                    self._admin_update_stock()
                elif choice == 3:
                    self._view_products()
                elif choice == 4:
                    print("Logged out.")
                    return
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def _admin_add_product(self) -> None:
        name = input("Product name: ").strip()
        price = self._read_float("Price: ")
        stock = self._read_int("Stock: ")

        p = self.catalog.add_product(name=name, price=price, stock=stock)
        print(f"Added product: [{p.product_id}] {p.name} - ${p.price:.2f} (Stock: {p.stock})")

    def _admin_update_stock(self) -> None:
        self._view_products()
        pid = self._read_int("Product ID to update: ")
        new_stock = self._read_int("New stock: ")
        self.catalog.update_stock(product_id=pid, new_stock=new_stock)
        print("Stock updated successfully.")

    

    def _customer_flow(self) -> None:
        username = input("Enter customer username: ").strip() or "customer"
        customer = Customer(username=username)

        while True:
            print(f"\n(Customer Menu) - Logged in as: {customer.username}")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Logout")

            choice = self._read_int("Choose: ")
            try:
                if choice == 1:
                    self._view_products()
                elif choice == 2:
                    self._customer_add_to_cart(customer)
                elif choice == 3:
                    self._customer_remove_from_cart(customer)
                elif choice == 4:
                    self._view_cart(customer)
                elif choice == 5:
                    self._checkout(customer)
                elif choice == 6:
                    print("Logged out.")
                    return
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def _customer_add_to_cart(self, customer: Customer) -> None:
        self._view_products()
        pid = self._read_int("Product ID to add: ")
        qty = self._read_int("Quantity: ")

        product = self._require_product(pid)
        customer.cart.add_item(product, qty)
        print("Added to cart.")

    def _customer_remove_from_cart(self, customer: Customer) -> None:
        self._view_cart(customer)
        if customer.cart.is_empty():
            return

        pid = self._read_int("Product ID to remove: ")
        qty = self._read_int("Quantity to remove: ")
        customer.cart.remove_item(pid, qty)
        print("Removed from cart.")

    def _view_cart(self, customer: Customer) -> None:
        items = customer.cart.items()
        if not items:
            print("\nCart is empty.")
            return

        print("\nYour Cart")
        print("-" * 50)
        total = 0.0
        for pid, qty in items.items():
            product = self._require_product(pid)
            line = product.price * qty
            total += line
            print(f"[{pid}] {product.name} | ${product.price:.2f} x {qty} = ${line:.2f}")
        print("-" * 50)
        print(f"Total: ${total:.2f}")

    def _checkout(self, customer: Customer) -> None:
        items = customer.cart.items()
        if not items:
            print("Cart is empty. Nothing to checkout.")
            return

        
        for pid, qty in items.items():
            product = self._require_product(pid)
            if qty > product.stock:
                raise ValueError(f"Not enough stock for '{product.name}'. Available: {product.stock}, In cart: {qty}")

        
        total = 0.0
        for pid, qty in items.items():
            product = self._require_product(pid)
            product.reduce_stock(qty)
            total += product.price * qty

        customer.cart.clear()
        print(f"Checkout successful. Amount paid: ${total:.2f}")

    

    def _view_products(self) -> None:
        products = self.catalog.all_products()
        if not products:
            print("\nNo products available.")
            return

        print("\nAvailable Products")
        print("-" * 60)
        print(f"{'ID':<5}{'Name':<25}{'Price':<12}{'Stock':<8}")
        print("-" * 60)
        for p in products.values():
            print(f"{p.product_id:<5}{p.name:<25}${p.price:<11.2f}{p.stock:<8}")
        print("-" * 60)

    def _require_product(self, product_id: int) -> Product:
        p = self.catalog.get(product_id)
        if not p:
            raise ValueError("Product not found.")
        return p

    @staticmethod
    def _read_int(prompt: str) -> int:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            raise ValueError("Please enter a valid integer.")

    @staticmethod
    def _read_float(prompt: str) -> float:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            raise ValueError("Please enter a valid number.")


if __name__ == "__main__":
    ECommerceApp().run()
