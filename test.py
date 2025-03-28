import unittest
from main import User, Product, Order, Shop
import unittest.mock



class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User()

    def test_user_initialization(self):
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.orders, [])
        self.assertFalse(self.user.is_admin)

    def test_user_login_success(self):
        self.user.email = "john@example.com"
        self.user.password = "password123"
        self.user.name = "John"
        self.assertTrue(self.user.login("john@example.com", "password123"))

    def test_user_login_failure(self):
        self.user.email = "john@example.com"
        self.user.password = "password123"
        self.assertFalse(self.user.login("john@example.com", "wrongpassword"))
        self.assertFalse(self.user.login("wrong@example.com", "password123"))

    def test_admin_creation(self):
        self.user.is_admin = True
        self.assertTrue(self.user.is_admin)


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.product = Product("Laptop", 25000, 10, "Test laptop")

    def test_product_initialization(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, 25000)
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.description, "Test laptop")

    def test_product_availability(self):
        self.assertTrue(self.product.is_available(5))
        self.assertTrue(self.product.is_available(10))
        self.assertFalse(self.product.is_available(11))

    def test_product_update(self):
        original_name = self.product.name
        original_price = self.product.price
        original_quantity = self.product.quantity


        with unittest.mock.patch('builtins.input', side_effect=['New Laptop', '30000', '15', 'Updated description']):
            self.product.update_product()

        self.assertNotEqual(self.product.name, original_name)
        self.assertNotEqual(self.product.price, original_price)
        self.assertNotEqual(self.product.quantity, original_quantity)


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.user = User()
        self.user.name = "Test User"
        self.user.email = "test@example.com"

        self.product1 = Product("Laptop", 25000, 10, "Test laptop")
        self.product2 = Product("Mouse", 800, 20, "Computer mouse")

        self.order = Order(self.user)

    def test_add_product(self):
        result = self.order.add_product(self.product1, 2)
        self.assertTrue(result)
        self.assertEqual(len(self.order.products), 1)
        self.assertEqual(self.order.products[0][1], 2)

    def test_add_product_insufficient_quantity(self):
        result = self.order.add_product(self.product1, 11)
        self.assertFalse(result)
        self.assertEqual(len(self.order.products), 0)

    def test_remove_product(self):
        self.order.add_product(self.product1, 2)
        result = self.order.remove_product("Laptop")
        self.assertTrue(result)
        self.assertEqual(len(self.order.products), 0)

    def test_remove_nonexistent_product(self):
        result = self.order.remove_product("Nonexistent")
        self.assertFalse(result)

    def test_calculate_total(self):
        self.order.add_product(self.product1, 2)
        self.order.add_product(self.product2, 3)
        total = self.order.calculate_total()
        self.assertEqual(total, 25000 * 2 + 800 * 3)

    def test_confirm_order(self):
        self.order.add_product(self.product1, 2)
        with unittest.mock.patch('builtins.input', return_value='yes'):
            result = self.order.confirm_order()

        self.assertTrue(result)
        self.assertEqual(self.order.status, "Confirmed")
        self.assertEqual(self.product1.quantity, 8)


class TestShop(unittest.TestCase):

    def setUp(self):
        self.shop = Shop()
        self.product = Product("Laptop", 25000, 10, "Test laptop")
        self.shop.add_product(self.product)

    def test_register_user(self):
        with unittest.mock.patch('builtins.input', side_effect=['John', 'john@example.com', 'password', 'no']):
            user = self.shop.register_user()

        self.assertIsNotNone(user)
        self.assertIn(user, self.shop.users)

    def test_login_user(self):
        user = User()
        user.name = "Test User"
        user.email = "test@example.com"
        user.password = "testpass"
        self.shop.users.append(user)

        logged_user = self.shop.login_user("test@example.com", "testpass")
        self.assertEqual(logged_user, user)

    def test_find_product(self):
        found_product = self.shop.find_product("Laptop")
        self.assertEqual(found_product, self.product)
        self.assertIsNone(self.shop.find_product("Phone"))

    def test_search_products(self):
        results = self.shop.search_products("laptop")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.product)

    def test_create_order(self):
        user = User()
        user.name = "Test User"
        user.email = "test@example.com"

        order = self.shop.create_order(user)

        self.assertIsNotNone(order)
        self.assertIn(order, self.shop.orders)
        self.assertIn(order, user.orders)


if __name__ == "__main__":
    unittest.main()