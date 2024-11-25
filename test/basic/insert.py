import os
import sys

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database import Database
from datetime import date

def insert_data():
    db = Database()

    # 插入类别
    for i in range(10):
        db.execute("""
            INSERT INTO Category (category_id, category_name, description)
            VALUES (?, ?, ?)
        """, (f'cat{i}', f'Category {i}', f'Description {i}'))

    # 插入出版社
    for i in range(10):
        db.execute("""
            INSERT INTO Publisher (publisher_id, publisher_name, contact_person, phone_number)
            VALUES (?, ?, ?, ?)
        """, (f'pub{i}', f'Publisher {i}', f'Contact Person {i}', f'Phone Number {i}'))

    # 插入图书
    for i in range(10):
        db.execute("""
            INSERT INTO Book (isbn, title, price, author, category_id, publisher_id, publish_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (f'isbn{i}', f'Title {i}', 10.0 + i, f'Author {i}', f'cat{i}', f'pub{i}', date.today()))

    # 插入客户
    for i in range(10):
        db.execute("""
            INSERT INTO Customer (customer_id, customer_name, password, register_date, login_count, account_balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (f'cus{i}', f'Customer {i}', f'Password {i}', date.today(), i, 100.0 + i))

    # 插入订单
    for i in range(10):
        db.execute("""
            INSERT INTO Orders (order_id, customer_id, order_date, total_amount, payment_status, logistics_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (f'order{i}', f'cus{i}', date.today(), 100.0 + i, '未支付', ['未发货', '已发货未完成'][i % 2]))

    # 插入订单详情
    for i in range(10):
        db.execute("""
            INSERT INTO OrderDetail (order_detail_id, order_id, isbn, unit_price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (f'detail{i}', f'order{i}', f'isbn{i}', 10.0 + i, 1 + i))

if __name__ == "__main__":
    insert_data()