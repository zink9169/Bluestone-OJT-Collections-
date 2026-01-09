
class Product:
    def __init__(self, pid, name, price, stock):
        self.pid = pid
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.pid} | {self.name} | ${self.price} | Stock: {self.stock}"

class User:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

# Polymorphism Concept
# Same system
# Different behavior based on role

# Inheritance
# Admin သည် User တစ်မျိုး ဖြစ်တယ်
# Admin inherits uid, name
# အခုတော့ extra feature မရှိသေးလို့ pass
# နောက်ပိုင်း product manage feature တွေ ထပ်ထည့်လို့ရ
class Admin(User):
    pass


# Inheritance
# Customer → User ကို inheritance လုပ်
# Composition (HAS-A relationship)
# Customer မှာ ShoppingCart တစ်ခုရှိတယ်
# Customer HAS-A Cart
class Customer(User):
    def __init__(self, uid, name):
        super().__init__(uid, name)
        self.cart = ShoppingCart()

# Encapsulation
# Cart logic အားလုံးကို ShoppingCart class ထဲမှာပဲထား
# (add, remove, total, checkout)
class ShoppingCart:
    def __init__(self):
        self.items = {}   # product -> qty

    def add_item(self, product, qty):
        if product.stock >= qty:
            self.items[product] = self.items.get(product, 0) + qty
            product.stock -= qty
            print("Added to cart")
        else:
            print("Not enough stock")

    def remove_item(self, product):
        if product in self.items:
            product.stock += self.items[product]
            del self.items[product]
            print("Removed from cart ")

    def view_cart(self):
        if not self.items:
            print("Cart is empty")
            return
        total = 0
        for p, q in self.items.items():
            print(f"{p.name} x {q} = ${p.price * q}")
            total += p.price * q
        print("Total =", total)

    def checkout(self):
        if not self.items:
            print("Cart empty")
            return
        print("Checkout successful")
        self.items.clear()

#System ထဲရှိ Product objects အားလုံးကိုသိမ်းထားတဲ့ storage
products = []

#Product list ကို display ပြဖို့ helper function
def view_products():
    if not products:
        print("No products available")
    for p in products:
        print(p)

while True:
    print("\nAre you?")
    print("1. Admin")
    print("2. Customer")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        admin = Admin(1, "Admin")

        while True:
            print("\n(Admin Menu)")
            print("1. Add Product")
            print("2. Update Product Stock")
            print("3. View Products")
            print("4. Logout")

            a = input("Choose: ")

            if a == "1":
                pid = int(input("ID: "))
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Stock: "))
                products.append(Product(pid, name, price, stock))
                print("Product added")

            elif a == "2":
                pid = int(input("Product ID: "))
                for p in products:
                    if p.pid == pid:
                        p.stock = int(input("New stock: "))
                        print("Stock updated")

            elif a == "3":
                view_products()

            elif a == "4":
                break

    elif choice == "2":
        customer = Customer(101, "Customer")

        while True:
            print("\n(Customer Menu)")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Logout")

            c = input("Choose: ")

            if c == "1":
                view_products()

            elif c == "2":
                pid = int(input("Product ID: "))
                qty = int(input("Qty: "))
                for p in products:
                    if p.pid == pid:
                        customer.cart.add_item(p, qty)

            elif c == "3":
                pid = int(input("Product ID: "))
                for p in list(customer.cart.items):
                    if p.pid == pid:
                        customer.cart.remove_item(p)

            elif c == "4":
                customer.cart.view_cart()

            elif c == "5":
                customer.cart.checkout()

            elif c == "6":
                break

    elif choice == "3":
        print("Goodbye")
        break
