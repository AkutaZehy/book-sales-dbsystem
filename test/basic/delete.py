import os
import sys

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database import Database

def delete_data():
    db = Database()

    # 删除类别
    db.execute("DELETE FROM Category WHERE category_id = ?", ('cat0',))
    db.execute("DELETE FROM Category WHERE category_id = ?", ('cat1',))

    # 删除出版社
    db.execute("DELETE FROM Publisher WHERE publisher_id = ?", ('pub0',))
    db.execute("DELETE FROM Publisher WHERE publisher_id = ?", ('pub1',))

    # 删除图书
    db.execute("DELETE FROM Book WHERE isbn = ?", ('isbn0',))
    db.execute("DELETE FROM Book WHERE isbn = ?", ('isbn1',))

    # 删除客户
    db.execute("DELETE FROM Customer WHERE customer_id = ?", ('cus0',))
    db.execute("DELETE FROM Customer WHERE customer_id = ?", ('cus1',))

    # 删除订单
    db.execute("DELETE FROM Orders WHERE order_id = ?", ('order0',))
    db.execute("DELETE FROM Orders WHERE order_id = ?", ('order1',))

    # 删除订单详情
    db.execute("DELETE FROM OrderDetail WHERE order_detail_id = ?", ('detail0',))
    db.execute("DELETE FROM OrderDetail WHERE order_detail_id = ?", ('detail1',))

if __name__ == "__main__":
    delete_data()