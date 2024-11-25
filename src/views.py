from database import Database
from models import *

class Views:
    def __init__(self):
        self.db = Database()

    def get_books(self):
        sql = """
        SELECT b.*, c.category_name, p.publisher_name
        FROM Book b
        LEFT JOIN Category c ON b.category_id = c.category_id
        LEFT JOIN Publisher p ON b.publisher_id = p.publisher_id
        """
        rows = self.db.execute(sql)
        books = []
        categories = {}
        publishers = {}

        for row in rows:
            isbn, title, price, author, category_id, publisher_id, publish_date, category_name, publisher_name = row
            if category_id not in categories:
                categories[category_id] = Category(category_id, category_name, None)
            if publisher_id not in publishers:
                publishers[publisher_id] = Publisher(publisher_id, publisher_name, None, None)
            
            book = Book(isbn, title, price, author, category_id, publisher_id, publish_date)
            book.set_category(categories[category_id])
            book.set_publisher(publishers[publisher_id])
            books.append(book)

        return books

    def get_categories(self):
        sql = "SELECT * FROM Category"
        rows = self.db.execute(sql)
        return [Category(*row) for row in rows]

    def get_publishers(self):
        sql = "SELECT * FROM Publisher"
        rows = self.db.execute(sql)
        return [Publisher(*row) for row in rows]

    def get_customers(self):
        sql = "SELECT * FROM Customer"
        rows = self.db.execute(sql)
        return [Customer(*row) for row in rows]

    def get_orders(self):
        sql = """
        SELECT o.*, c.customer_name
        FROM Orders o
        LEFT JOIN Customer c ON o.customer_id = c.customer_id
        """
        rows = self.db.execute(sql)
        orders = []
        customers = {}

        for row in rows:
            order_id, customer_id, order_date, total_amount, payment_status, logistics_status, customer_name = row
            if customer_id not in customers:
                customers[customer_id] = Customer(customer_id, customer_name, None, None, 0, 0)
            
            order = Order(order_id, customer_id, order_date, total_amount, payment_status, logistics_status)
            order.set_customer(customers[customer_id])
            orders.append(order)

        return orders

    def get_order_details(self):
        sql = """
        SELECT od.*, o.order_id, b.isbn, b.title
        FROM OrderDetail od
        LEFT JOIN Orders o ON od.order_id = o.order_id
        LEFT JOIN Book b ON od.isbn = b.isbn
        """
        rows = self.db.execute(sql)
        order_details = []
        orders = {}
        books = {}

        for row in rows:
            order_detail_id, order_id, isbn, unit_price, quantity, order_id, isbn, title = row
            if order_id not in orders:
                orders[order_id] = Order(order_id, None, None, 0, '', '')
            if isbn not in books:
                books[isbn] = Book(isbn, title, 0, '', '', '', None)
            
            order_detail = OrderDetail(order_detail_id, order_id, isbn, unit_price, quantity)
            order_detail.set_order(orders[order_id])
            order_detail.set_book(books[isbn])
            order_details.append(order_detail)

        return order_details

    def get_customer_orders(self, customer_id):
        sql = """
        SELECT o.order_id, o.customer_id, o.order_date, o.total_amount, o.payment_status, o.logistics_status, b.title, od.quantity, od.unit_price
        FROM Orders o
        JOIN OrderDetail od ON o.order_id = od.order_id
        JOIN Book b ON od.isbn = b.isbn
        WHERE o.customer_id = ?
        """
        rows = self.db.execute(sql, (customer_id,))
        return rows

    def get_warehouse_manager_orders(self):
        sql = """
        SELECT o.order_id, o.customer_id, od.isbn, SUM(od.quantity) AS total_quantity
        FROM Orders o
        JOIN OrderDetail od ON o.order_id = od.order_id
        WHERE o.logistics_status IN ('未发货', '已发货未完成')
        GROUP BY o.order_id, o.customer_id, od.isbn
        """
        rows = self.db.execute(sql)
        return rows