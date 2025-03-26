class User:
    def __init__(self):
        self.email = ""
        self.password = ""
        self.name = ""
        self.orders = []

    def register(self):
        self.name = input("Enter name: ")
        self.email = input("Enter email: ")
        self.password = input("Enter password: ")
        print("Registration successful!")
        return True

    def login(self, email, password):
        if email == self.email and password == self.password:
            print(f"Welcome, {self.name}!")
            return True
        else:
            print("Invalid credentials.")
            return False

    def view_orders(self):
        if not self.orders:
            print("You don't have any orders yet.")
            return

        print(f"Orders for user {self.name}:")
        for i, order in enumerate(self.orders, 1):
            print(f"Order #{i}:")
            order.display_order_details()

    def place_order(self, order):
        self.orders.append(order)
        print("Order successfully placed!")


class Product:
    def __init__(self, name="", price=0, quantity=0, description=""):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

    def create_product(self):
        self.name = input("Enter product name: ")
        self.price = float(input("Enter product price: "))
        self.quantity = int(input("Enter product quantity: "))
        self.description = input("Enter product description: ")
        print("Product successfully created!")
        return self

    def display_product(self):
        print(f"Product: {self.name}")
        print(f"Price: {self.price}")
        print(f"Available quantity: {self.quantity}")
        print(f"Description: {self.description}")

    def update_product(self):
        print(f"Updating product: {self.name}")
        self.name = input(f"New name (current: {self.name}): ") or self.name
        new_price = input(f"New price (current: {self.price}): ")
        self.price = float(new_price) if new_price else self.price
        new_quantity = input(f"New quantity (current: {self.quantity}): ")
        self.quantity = int(new_quantity) if new_quantity else self.quantity
        self.description = input(f"New description (current: {self.description}): ") or self.description
        print("Product successfully updated!")

    def is_available(self, requested_quantity=1):
        return self.quantity >= requested_quantity


class Order:
    def __init__(self, user):
        self.user = user
        self.products = []
        self.status = "New"

    def add_product(self, product, quantity=1):
        if not self.user:
            print("You need to log in to add a product.")
            return False

        if not product.is_available(quantity):
            print(f"Cannot add product. Available quantity: {product.quantity}")
            return False

        for i, (existing_product, existing_quantity) in enumerate(self.products):
            if existing_product.name == product.name:
                self.products[i] = (existing_product, existing_quantity + quantity)
                print(f"Quantity of {product.name} increased to {existing_quantity + quantity}")
                return True

        self.products.append((product, quantity))
        print(f"Product {product.name} added to order with quantity {quantity}")
        return True

    def remove_product(self, product_name):
        for i, (product, quantity) in enumerate(self.products):
            if product.name == product_name:
                del self.products[i]
                print(f"Product {product_name} removed from order")
                return True

        print(f"Product {product_name} not found in order")
        return False

    def calculate_total(self):
        total = 0
        for product, quantity in self.products:
            total += product.price * quantity
        return total

    def confirm_order(self):
        if not self.products:
            print("Cannot confirm an empty order")
            return False

        print("Order confirmation:")
        self.display_order_details()

        confirm = input("Confirm order? (yes/no): ").lower()
        if confirm == "yes":
            self.status = "Confirmed"
            for product, quantity in self.products:
                product.quantity -= quantity
            return True

        return False

    def display_order_details(self):
        print(f"Order status: {self.status}")
        print("Products in order:")
        for product, quantity in self.products:
            print(f"- {product.name} x{quantity}: {product.price * quantity}")
        print(f"Total amount: {self.calculate_total()}")


class Shop:
    def __init__(self):
        self.users = []
        self.products = []
        self.orders = []

    def register_user(self):
        user = User()
        if user.register():
            self.users.append(user)
            return user
        return None

    def login_user(self, email, password):
        for user in self.users:
            if user.email == email:
                return user if user.login(email, password) else None
        print("User with this email not found.")
        return None

    def add_product(self, product):
        self.products.append(product)

    def find_product(self, name):
        for product in self.products:
            if product.name.lower() == name.lower():
                return product
        return None

    def search_products(self, keyword):
        results = []
        for product in self.products:
            if keyword.lower() in product.name.lower() or keyword.lower() in product.description.lower():
                results.append(product)
        return results

    def create_order(self, user):
        if not user:
            print("You need to log in to create an order.")
            return None

        order = Order(user)
        self.orders.append(order)
        user.orders.append(order)
        return order

    def display_all_products(self):
        if not self.products:
            print("No products available.")
            return

        print("Available products:")
        for i, product in enumerate(self.products, 1):
            print(f"{i}. {product.name} - {product.price} (quantity: {product.quantity})")


def main():
    shop = Shop()

    laptop = Product("HP Laptop", 25000, 10, "Powerful laptop for work")
    shop.add_product(laptop)

    phone = Product("Samsung Smartphone", 12000, 15, "New smartphone with a good camera")
    shop.add_product(phone)

    headphones = Product("Sony Headphones", 3500, 20, "Wireless headphones with noise cancellation")
    shop.add_product(headphones)

    print("=== Register a new user ===")
    user = shop.register_user()

    shop.display_all_products()

    order = shop.create_order(user)
    if order:
        order.add_product(laptop, 1)
        order.add_product(headphones, 2)

        print("\n=== Order details ===")
        order.display_order_details()

        order.confirm_order()

        user.view_orders()


if __name__ == "__main__":
    main()