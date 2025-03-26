import unittest
from unittest.mock import patch
import io

from main import User, Product, Order, Shop


class TestUser(unittest.TestCase):
    def test_user_initialization(self):
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.orders, [])

    def test_user_login_success(self):
        user = User()
        user.email = "john@example.com"
        user.password = "password123"
        self.assertTrue(user.login("john@example.com", "password123"))

    def test_user_login_failure(self):
        user = User()
        user.email = "john@example.com"
        user.password = "password123"
        self.assertFalse(user.login("john@example.com", "wrongpassword"))


class TestProduct(unittest.TestCase):
    def test_product_initialization(self):
        product = Product("Laptop", 25000, 10)
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.quantity, 10)

    def test_product_availability(self):
        product = Product("Laptop", 25000, 5)
        self.assertTrue(product.is_available(3))
        self.assertFalse(product.is_available(6))

    def test_reduce_stock(self):
        product = Product("Laptop", 25000, 5)
        product.quantity -= 3
        self.assertEqual(product.quantity, 2)


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.order = Order(self.user)
        self.product1 = Product("Laptop", 25000, 10)
        self.product2 = Product("Mouse", 800, 20)

    def test_add_product(self):
        self.order.add_product(self.product1, 2)
        self.assertEqual(len(self.order.products), 1)

    def test_remove_product(self):
        self.order.add_product(self.product1, 2)
        self.order.add_product(self.product2, 1)
        self.order.remove_product("Laptop")
        self.assertEqual(len(self.order.products), 1)

    def test_calculate_total(self):
        self.order.add_product(self.product1, 2)
        self.order.add_product(self.product2, 3)
        self.assertEqual(self.order.calculate_total(), 52400)

    def test_confirm_order(self):
        self.order.add_product(self.product1, 1)
        self.order.confirm_order()
        self.assertEqual(self.order.status, "Confirmed")


class TestShop(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.product = Product("Laptop", 25000, 10)
        self.shop.add_product(self.product)
        self.user = User()
        self.shop.users.append(self.user)

    def test_find_product(self):
        self.assertEqual(self.shop.find_product("Laptop"), self.product)
        self.assertIsNone(self.shop.find_product("Phone"))

    def test_create_order(self):
        order = self.shop.create_order(self.user)
        self.assertIn(order, self.shop.orders)

    def test_add_product_to_shop(self):
        new_product = Product("Phone", 15000, 5)
        self.shop.add_product(new_product)
        self.assertEqual(len(self.shop.products), 2)

    def test_login_user(self):
        self.user.email = "test@example.com"
        self.user.password = "test123"
        self.assertEqual(self.shop.login_user("test@example.com", "test123"), self.user)
        self.assertIsNone(self.shop.login_user("wrong@example.com", "test123"))


if __name__ == "__main__":
    unittest.main()