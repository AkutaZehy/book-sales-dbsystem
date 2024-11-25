class Book:
    def __init__(self, isbn, title, price, author, category_id, publisher_id, publish_date, category=None, publisher=None):
        self.isbn = isbn
        self.title = title
        self.price = price
        self.author = author
        self.category_id = category_id
        self.publisher_id = publisher_id
        self.publish_date = publish_date
        self.category = category
        self.publisher = publisher

    def set_category(self, category):
        self.category = category

    def set_publisher(self, publisher):
        self.publisher = publisher


class Category:
    def __init__(self, category_id, category_name, description):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description


class Publisher:
    def __init__(self, publisher_id, publisher_name, contact_person, phone_number):
        self.publisher_id = publisher_id
        self.publisher_name = publisher_name
        self.contact_person = contact_person
        self.phone_number = phone_number


class Customer:
    def __init__(self, customer_id, customer_name, password, register_date, login_count, account_balance):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.password = password
        self.register_date = register_date
        self.login_count = login_count
        self.account_balance = account_balance


class Order:
    def __init__(self, order_id, customer_id, order_date, total_amount, payment_status, logistics_status, customer=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.payment_status = payment_status
        self.logistics_status = logistics_status
        self.customer = customer

    def set_customer(self, customer):
        self.customer = customer


class OrderDetail:
    def __init__(self, order_detail_id, order_id, isbn, unit_price, quantity, order=None, book=None):
        self.order_detail_id = order_detail_id
        self.order_id = order_id
        self.isbn = isbn
        self.unit_price = unit_price
        self.quantity = quantity
        self.order = order
        self.book = book

    def set_order(self, order):
        self.order = order

    def set_book(self, book):
        self.book = book