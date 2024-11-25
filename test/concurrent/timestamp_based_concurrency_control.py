import os
import random
import sys
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database_concurrent import Database

class TimestampBasedConcurrencyControl:
    def __init__(self, db):
        self.db = db
        self.timestamps = {}
        self.locks = {}

    def start_transaction(self, tid):
        self.timestamps[tid] = time.time()

    def read(self, tid, table, key):
        lock = self.locks.setdefault(table, threading.Lock())
        logging.debug(f"Transaction {tid} trying to acquire lock on {table} at {time.time()}")
        with lock:
            logging.debug(f"Transaction {tid} acquired lock on {table} at {time.time()}")
            sql = f"SELECT * FROM {table} WHERE order_id = ?"
            result = self.db.execute(sql, (key,))
            return result

    def write(self, tid, table, key, value):
        lock = self.locks.setdefault(table, threading.Lock())
        logging.debug(f"Transaction {tid} trying to acquire lock on {table} at {time.time()}")
        with lock:
            logging.debug(f"Transaction {tid} acquired lock on {table} at {time.time()}")
            sql = f"SELECT * FROM {table} WHERE order_id = ?"
            result = self.db.execute(sql, (key,))
            if result and self.timestamps[tid] < self.timestamps.get(result[0][0], float('-inf')):
                raise Exception(f"Transaction {tid} cannot write data written by a newer transaction")
            value['tid'] = tid
            if table == 'Orders':
                sql = f"REPLACE INTO {table} (order_id, customer_id, order_date, total_amount, payment_status, logistics_status) VALUES (?, ?, ?, ?, ?, ?)"
                self.db.execute(sql, (value['order_id'], value['customer_id'], value['order_date'], value['total_amount'], value['payment_status'], value['logistics_status']))
            elif table == 'OrderDetail':
                sql = f"REPLACE INTO {table} (order_detail_id, order_id, isbn, unit_price, quantity) VALUES (?, ?, ?, ?, ?)"
                self.db.execute(sql, (value['order_detail_id'], value['order_id'], value['isbn'], value['unit_price'], value['quantity']))

def test_timestamp_based_concurrency_control(db):
    tbcc = TimestampBasedConcurrencyControl(db)

    def transaction_1(tid):
        try:
            tbcc.start_transaction(tid)
            logging.debug(f"Transaction {tid} starting at {time.time()}")
            tbcc.read(tid, 'Orders', 'order1')
            tbcc.read(tid, 'OrderDetail', 'detail1')
            time.sleep(0.5)
            tbcc.write(tid, 'Orders', 'order1', {'order_id': 'order1', 'customer_id': 'customer0', 'order_date': '2023-01-01', 'total_amount': 200.00, 'payment_status': '未支付', 'logistics_status': '未发货'})
            tbcc.write(tid, 'OrderDetail', 'detail1', {'order_detail_id': 'detail1', 'order_id': 'order1', 'isbn': '1234567890123', 'unit_price': 100.00, 'quantity': 2})
            logging.debug(f"Transaction {tid} completed successfully at {time.time()}")
        except Exception as e:
            logging.error(f"Transaction {tid} failed: {e}")

    def transaction_2(tid):
        try:
            tbcc.start_transaction(tid)
            logging.debug(f"Transaction {tid} starting at {time.time()}")
            tbcc.read(tid, 'Orders', 'order1')
            tbcc.read(tid, 'OrderDetail', 'detail1')
            time.sleep(0.5)
            tbcc.write(tid, 'Orders', 'order1', {'order_id': 'order1', 'customer_id': 'customer0', 'order_date': '2023-01-02', 'total_amount': 300.00, 'payment_status': '已支付', 'logistics_status': '已发货未完成'})
            tbcc.write(tid, 'OrderDetail', 'detail1', {'order_detail_id': 'detail1', 'order_id': 'order1', 'isbn': '1234567890123', 'unit_price': 100.00, 'quantity': 3})
            logging.debug(f"Transaction {tid} completed successfully at {time.time()}")
        except Exception as e:
            logging.error(f"Transaction {tid} failed: {e}")

    def transaction_3(tid):
        try:
            tbcc.start_transaction(tid)
            logging.debug(f"Transaction {tid} starting at {time.time()}")
            result_orders = tbcc.read(tid, 'Orders', 'order1')
            result_order_detail = tbcc.read(tid, 'OrderDetail', 'detail1')
            logging.debug(f"Transaction {tid} read Orders: {result_orders}")
            logging.debug(f"Transaction {tid} read OrderDetail: {result_order_detail}")
            logging.debug(f"Transaction {tid} completed successfully at {time.time()}")
        except Exception as e:
            logging.error(f"Transaction {tid} failed: {e}")

    threads = []
    for i in range(10):
        interval = 0.1
        target = [transaction_1, transaction_2, transaction_3][i % 3]
        t = threading.Thread(target=target, args=(i,), name=f"Thread-{i}")
        threads.append(t)
        time.sleep(interval)
        t.start()

    for t in threads:
        t.join()

    # 回显结果
    result = db.execute("SELECT * FROM Orders WHERE order_id = 'order1'")
    logging.debug(f"Final state of Orders table: {result}")
    result = db.execute("SELECT * FROM OrderDetail WHERE order_detail_id = 'detail1'")
    logging.debug(f"Final state of OrderDetail table: {result}")

if __name__ == "__main__":
    db = Database()
    test_timestamp_based_concurrency_control(db)