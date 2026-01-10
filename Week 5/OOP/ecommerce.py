class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"ID: {self.product_id} | {self.name} | Price: ${self.price} | Stock: {self.stock}"


class User:
    def __init__(self, username):
        self.username = username


class Admin(User):
    def add_product(self, inventory):
        p_id = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        price = float(input("Enter Price: "))
        while True:
            user_input = input("Enter Stock Quantity: ")

            try:
                stock = int(user_input)
                if stock < 0:
                    print("Error: Stock cannot be negative. Try again.")
                else:
                    print("Stock quantity accepted:", stock)
                    break
            except ValueError:
                print("Error: Please enter a whole number (no decimals). Try again.")

        inventory.append(Product(p_id, name, price, stock))
        print("Product added successfully!")

    def update_stock(self, inventory):
        p_id = input("Enter Product ID to update: ")
        for p in inventory:
            if p.product_id == p_id:
                new_stock = int(input(f"Current stock is {p.stock}. Enter new stock: "))
                p.stock = new_stock
                print("Stock updated!")
                return
        print("Product not found.")


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        if product.stock >= quantity:
            self.items.append({"product": product, "quantity": quantity})
            product.stock -= quantity
            print(f"Added {quantity} {product.name}(s) to cart.")
        else:
            print("Insufficient stock!")

    def remove_item(self, product_id):
        for item in self.items:
            if item["product"].product_id == product_id:
                item["product"].stock += item["quantity"]
                self.items.remove(item)
                print("Item removed from cart.")
                return
        print("Item not in cart.")

    def view_cart(self):
        if not self.items:
            print("Cart is empty.")
        else:
            total = 0
            for item in self.items:
                p = item["product"]
                subtotal = p.price * item["quantity"]
                total += subtotal
                print(f"{p.name} x {item['quantity']} - ${subtotal}")
            print(f"Total: ${total}")


class Customer(User):
    def __init__(self, username):
        super().__init__(username)
        self.cart = ShoppingCart()


inventory = [Product("1", "Laptop", 999.99, 5), Product("2", "Mouse", 25.00, 10)]


def main():
    while True:
        print("\n--- Welcome to the Store ---")
        print("1. Admin\n2. Customer\n3. Exit")
        choice = input("Select Role: ")

        if choice == '1':
            admin = Admin("Admin_User")
            while True:
                print("\n(Admin Menu)\n1. Add Product\n2. Update Stock\n3. View Products\n4. Logout")
                a_choice = input("Action: ")
                if a_choice == '1':
                    admin.add_product(inventory)
                elif a_choice == '2':
                    admin.update_stock(inventory)
                elif a_choice == '3':
                    for p in inventory: print(p)
                elif a_choice == '4':
                    break

        elif choice == '2':
            customer = Customer("Guest")
            while True:
                print(
                    "\n(Customer Menu)\n1. View Products\n2. Add to Cart\n3. Remove from Cart\n4. View Cart\n5. Checkout\n6. Logout")
                c_choice = input("Action: ")
                if c_choice == '1':
                    for p in inventory: print(p)
                elif c_choice == '2':
                    p_id = input("Enter Product ID: ")
                    qty = int(input("Quantity: "))
                    prod = next((p for p in inventory if p.product_id == p_id), None)
                    if prod: customer.cart.add_item(prod, qty)
                elif c_choice == '3':
                    p_id = input("Enter Product ID to remove: ")
                    customer.cart.remove_item(p_id)
                elif c_choice == '4':
                    customer.cart.view_cart()
                elif c_choice == '5':
                    customer.cart.view_cart()
                    print("Thank you for your purchase!")
                    customer.cart.items = []  # Clear cart
                elif c_choice == '6':
                    break

        elif choice == '3':
            break


if __name__ == "__main__":
    main()