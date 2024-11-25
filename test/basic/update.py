import os
import sys

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database import Database

def update_data():
    db = Database()

    # 更新类别
    db.execute("UPDATE Category SET category_name = ? WHERE category_id = ?", ('Updated Category 0', 'cat2'))
    db.execute("UPDATE Category SET category_name = ? WHERE category_id = ?", ('Updated Category 1', 'cat3'))

    # 更新出版社
    db.execute("UPDATE Publisher SET publisher_name = ? WHERE publisher_id = ?", ('Updated Publisher 0', 'pub2'))
    db.execute("UPDATE Publisher SET publisher_name = ? WHERE publisher_id = ?", ('Updated Publisher 1', 'pub3'))

    # 更新图书
    db.execute("UPDATE Book SET title = ? WHERE isbn = ?", ('Updated Title 0', 'isbn2'))
    db.execute("UPDATE Book SET title = ? WHERE isbn = ?", ('Updated Title 1', 'isbn3'))

    # 更新客户
    db.execute("UPDATE Customer SET customer_name = ? WHERE customer_id = ?", ('Updated Customer 0', 'cus2'))
    db.execute("UPDATE Customer SET customer_name = ? WHERE customer_id = ?", ('Updated Customer 1', 'cus3'))

    # 更新订单
    db.execute("UPDATE Orders SET payment_status = ? WHERE order_id = ?", ('已支付', 'order2'))
    db.execute("UPDATE Orders SET payment_status = ? WHERE order_id = ?", ('已支付', 'order3'))

    # 更新订单详情
    db.execute("UPDATE OrderDetail SET quantity = ? WHERE order_detail_id = ?", (10, 'detail2'))
    db.execute("UPDATE OrderDetail SET quantity = ? WHERE order_detail_id = ?", (10, 'detail3'))

if __name__ == "__main__":
    update_data()