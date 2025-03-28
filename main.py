


class User:
    def __init__(self):

        self.email = ""
        self.password = ""
        self.name = ""
        self.orders = []
        self.is_admin = False

    def register(self):

        self.name = input("Enter name: ")
        self.email = input("Enter email: ")
        self.password = input("Enter password: ")

        admin_choice = input("Create as admin? (yes/no): ").lower()
        if admin_choice == 'yes':
            self.is_admin = True
            print("Admin account created!")

        print("Registration successful!")
        return True

    def login(self, email, password):
        if email == self.email and password == self.password:
            print(f"Welcome, {'Admin' if self.is_admin else 'User'}, {self.name}!")
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

    def add_product(self, shop):

        if not self.is_admin:
            print("Only admin can add products!")
            return None

        product = Product().create_product()
        shop.add_product(product)
        return product

    def remove_product(self, shop, product_name):

        if not self.is_admin:
            print("Only admin can remove products!")
            return False

        product = shop.find_product(product_name)
        if product:
            shop.products.remove(product)
            print(f"Product {product_name} removed.")
            return True
        print(f"Product {product_name} not found.")
        return False


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


    current_user = None

    while True:
        print("\n=== Shop Management System ===")
        print("1. Register New User")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")


        if choice == '1':
            print("\n--- User Registration ---")
            new_user = shop.register_user()
            if new_user:
                print(f"Welcome, {new_user.name}!")


        elif choice == '2':
            print("\n--- Login ---")
            email = input("Enter email: ")
            password = input("Enter password: ")
            current_user = shop.login_user(email, password)


            if current_user:
                while True:
                    print("\n=== User Menu ===")
                    print("1. View Products")
                    print("2. Search Products")
                    print("3. Create Order")
                    print("4. View My Orders")

                    if current_user.is_admin:
                        print("5. Add Product")
                        print("6. Remove Product")
                        print("7. Update Product")

                    print("0. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':

                        shop.display_all_products()

                    elif user_choice == '2':
                        keyword = input("Enter search keyword: ")
                        results = shop.search_products(keyword)

                        if results:
                            print("\nSearch Results:")
                            for product in results:
                                product.display_product()
                                print("---")
                        else:
                            print("No products found.")

                    elif user_choice == '3':
                        order = shop.create_order(current_user)

                        while True:
                            shop.display_all_products()
                            product_name = input("Enter product name to add (or 'done' to finish): ")

                            if product_name.lower() == 'done':
                                break

                            product = shop.find_product(product_name)
                            if product:
                                quantity = int(input(f"Enter quantity for {product_name}: "))
                                order.add_product(product, quantity)
                            else:
                                print("Product not found.")

                        if order.products:
                            order.confirm_order()

                    elif user_choice == '4':
                        current_user.view_orders()

                    elif current_user.is_admin:
                        if user_choice == '5':
                            current_user.add_product(shop)

                        elif user_choice == '6':
                            product_name = input("Enter product name to remove: ")
                            current_user.remove_product(shop, product_name)

                        elif user_choice == '7':
                            product_name = input("Enter product name to update: ")
                            product = shop.find_product(product_name)
                            if product:
                                product.update_product()
                            else:
                                print("Product not found.")

                    elif user_choice == '0':
                        current_user = None
                        break

                    else:
                        print("Invalid choice. Please try again.")

        elif choice == '3':

            print("Thank you for using Shop Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
