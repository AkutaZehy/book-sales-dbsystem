import os
import sys

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database import Database

class HashIndex:
    def __init__(self):
        self.customer_to_orders = {}
        self.order_to_details = {}

    def build_index(self):
        db = Database()

        # 构建customer_id到order_id的映射
        results = db.execute("SELECT customer_id, order_id FROM Orders")
        for customer_id, order_id in results:
            if customer_id not in self.customer_to_orders:
                self.customer_to_orders[customer_id] = []
            self.customer_to_orders[customer_id].append(order_id)

        # 构建order_id到订单详情的映射
        results = db.execute("SELECT order_id, unit_price, quantity FROM OrderDetail")
        for order_id, unit_price, quantity in results:
            if order_id not in self.order_to_details:
                self.order_to_details[order_id] = []
            self.order_to_details[order_id].append((unit_price, quantity))

    def search_orders(self, customer_id):
        return self.customer_to_orders.get(customer_id, [])

    def search_order_details(self, order_ids):
        total_amount = 0
        for order_id in order_ids:
            for unit_price, quantity in self.order_to_details.get(order_id, []):
                total_amount += unit_price * quantity
        return total_amount