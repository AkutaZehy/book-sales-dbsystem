import os
import sys

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database import Database

def create_btree_index():
    db = Database()
    db.execute("CREATE INDEX IF NOT EXISTS idx_customer_id ON Orders (customer_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_order_id ON OrderDetail (order_id)")

if __name__ == "__main__":
    create_btree_index()