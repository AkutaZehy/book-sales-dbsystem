import sqlite3
import os
import logging
import time

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# 数据库路径
db_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/db/my_database.db3'

class Database:
    def __init__(self, db_path=db_dir):
        self.db_path = db_path

    def connect(self):
        # print("Connecting to the database...time:", time.time())
        return sqlite3.connect(self.db_path)

    def execute(self, sql, params=()):
        conn = self.connect()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()
            # print("Connection closed...time:", time.time())

    def execute_script(self, script):
        conn = self.connect()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.executescript(script)
        finally:
            conn.close()
            print("Connection closed...time:", time.time())

    def get_total_amount_for_customer(self, customer_id):
        sql = """
            SELECT SUM(od.unit_price * od.quantity) 
            FROM Orders o
            JOIN OrderDetail od ON o.order_id = od.order_id
            WHERE o.customer_id = ?
        """
        result = self.execute(sql, (customer_id,))
        return result[0][0] if result else 0

if __name__ == "__main__":
    db = Database()