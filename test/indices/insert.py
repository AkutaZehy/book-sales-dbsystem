import os
import random
import sys

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database import Database
from datetime import datetime, timedelta

def insert_data():
    db = Database()

    # 插入订单
    for i in range(10000):  # 10,000条订单
        order_id = f'order{i}'
        customer_id = f'customer{random.randint(0, 999)}'  # 1000个不同的用户
        order_date = datetime.now() - timedelta(days=random.randint(0, 365))  # 订单日期在过去一年内随机分布
        total_amount = 10  # 每个订单固定总数为10
        payment_status = random.choice(['未支付', '已支付'])
        logistics_status = random.choice(['未发货', '已发货未完成', '已完成'])

        db.execute("""
            INSERT INTO Orders (order_id, customer_id, order_date, total_amount, payment_status, logistics_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, customer_id, order_date, total_amount, payment_status, logistics_status))

        # 插入订单详情
        for j in range(10):  # 每个订单10条订单详情
            order_detail_id = f'detail{i}_{j}'
            num = random.randint(0, 100) + 1
            isbn = f'isbn{num}'  # 每个num对应一个isbn
            unit_price = num
            quantity = 1  # 数量固定为1

            db.execute("""
                INSERT INTO OrderDetail (order_detail_id, order_id, isbn, unit_price, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (order_detail_id, order_id, isbn, unit_price, quantity))

if __name__ == "__main__":
    insert_data()