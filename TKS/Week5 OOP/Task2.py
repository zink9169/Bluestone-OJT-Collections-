class Product:
    def __init__(self, pid, name, price, stock):
        self.id = pid
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def display(self):
        print(f"{self.id}. {self.name} | Price: {self.price:.2f} | Stock: {self.stock}")


# -- User Class --
class User:
    def __init__(self, name):
        self.name = name


# -- Admin Class --
class Admin(User):
    def add_product(self, products):
        pid = len(products) + 1
        name = input("Enter product name: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock (integer): "))

        products.append(Product(pid, name, price, stock))
        print("Product added successfully!")

    def update_stock(self, products):
        for p in products:
            p.display()

        pid = int(input("Enter product id to update: "))
        for p in products:
            if p.id == pid:
                p.stock = int(input("Enter new stock (integer): "))
                print("Stock updated!")
                return
        print("Product not found!")

    def view_products(self, products):
        if not products:
            print("No products available.")
        for p in products:
            p.display()


# -- Shopping Cart --
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, product, qty):
        qty = int(qty)

        if qty <= 0:
            print("Quantity must be greater than 0.")
            return

        if qty > product.stock:
            print("Not enough stock!")
            return

        self.items.append((product, qty))
        product.stock -= qty
        print("Added to cart!")

    def remove_from_cart(self):
        if not self.items:
            print("Cart is empty.")
            return

        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item[0].name} x {item[1]}")

        choice = int(input("Select item to remove: ")) - 1

        if 0 <= choice < len(self.items):
            product, qty = self.items.pop(choice)
            product.stock += qty
            print("Item removed.")
        else:
            print("Invalid choice.")

    def view_cart(self):
        if not self.items:
            print("Cart is empty.")
            return

        total = 0.0
        for product, qty in self.items:
            cost = product.price * qty
            total += cost
            print(f"{product.name} x {qty} = {cost:.2f}")

        print(f"Total: {total:.2f}")

    def checkout(self):
        if not self.items:
            print("Cart is empty.")
            return

        self.view_cart()
        print("Checkout successful!")
        self.items.clear()


# -- Customer Class --
class Customer(User):
    def __init__(self, name):
        super().__init__(name)
        self.cart = ShoppingCart()

    def view_products(self, products):
        for p in products:
            p.display()

    def add_to_cart(self, products):
        for p in products:
            p.display()

        pid = int(input("Enter product id: "))
        qty = int(input("Enter quantity: "))

        for p in products:
            if p.id == pid:
                self.cart.add_to_cart(p, qty)
                return
        print("Product not found!")


# -- Products --
products = [
    Product(1, "Laptop", 800, 5),
    Product(2, "Phone", 500, 10),
    Product(3, "Headphones", 50, 15),
    Product(4, "Keyboard", 30, 20)
]


# -- MAIN --
while True:
    print("\nAre you an Admin or Customer?")
    print("1. Admin")
    print("2. Customer")
    print("3. Exit")

    main_choice = input("Choose: ")

    if main_choice == "1":
        admin = Admin("Admin")

        while True:
            print("\n--- Admin Menu ---")
            print("1. Add Product")
            print("2. Update Product Stock")
            print("3. View Products")
            print("4. Logout")

            choice = input("Choose: ")

            if choice == "1":
                admin.add_product(products)
            elif choice == "2":
                admin.update_stock(products)
            elif choice == "3":
                admin.view_products(products)
            elif choice == "4":
                break
            else:
                print("Invalid option")

    elif main_choice == "2":
        customer = Customer("Customer")

        while True:
            print("\n--- Customer Menu ---")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Logout")

            choice = input("Choose: ")

            if choice == "1":
                customer.view_products(products)
            elif choice == "2":
                customer.add_to_cart(products)
            elif choice == "3":
                customer.cart.remove_from_cart()
            elif choice == "4":
                customer.cart.view_cart()
            elif choice == "5":
                customer.cart.checkout()
            elif choice == "6":
                break
            else:
                print("Invalid option")

    elif main_choice == "3":
        print("Thank you! Exiting...")
        break
    else:
        print("Invalid choice")
