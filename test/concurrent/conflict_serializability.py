import os
import sys
import threading
import time

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/src'
sys.path.append(src_dir)

from database_concurrent import Database

class ConflictSerializability:
    def __init__(self, db):
        self.db = db
        self.transactions = []
        self.conflict_matrix = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def build_conflict_matrix(self):
        self.conflict_matrix = [[0 for _ in range(len(self.transactions))] for _ in range(len(self.transactions))]
        for i, t1 in enumerate(self.transactions):
            for j, t2 in enumerate(self.transactions):
                if i != j and self.has_conflict(t1, t2):
                    self.conflict_matrix[i][j] = 1

    def has_conflict(self, t1, t2):
        for op1 in t1:
            for op2 in t2:
                if op1['table'] == op2['table'] and op1['key'] == op2['key']:
                    if (op1['type'] == 'write' or op2['type'] == 'write'):
                        return True
        return False

    def is_serializable(self):
        self.build_conflict_matrix()
        return not self.has_cycle()

    def has_cycle(self):
        visited = [False] * len(self.transactions)
        rec_stack = [False] * len(self.transactions)

        for i in range(len(self.transactions)):
            if not visited[i]:
                if self.is_cyclic_util(i, visited, rec_stack):
                    return True
        return False

    def is_cyclic_util(self, i, visited, rec_stack):
        if rec_stack[i]:
            return True
        if visited[i]:
            return False

        visited[i] = True
        rec_stack[i] = True

        for j in range(len(self.transactions)):
            if self.conflict_matrix[i][j] == 1:
                if self.is_cyclic_util(j, visited, rec_stack):
                    return True

        rec_stack[i] = False
        return False

def test_conflict_serializability(db):
    cs = ConflictSerializability(db)

    # 添加10个事务
    transactions = [
        [{'type': 'read', 'table': 'Orders', 'key': 1}, {'type': 'write', 'table': 'OrderDetail', 'key': 1}],
        [{'type': 'write', 'table': 'Orders', 'key': 1}, {'type': 'read', 'table': 'OrderDetail', 'key': 1}],
        [{'type': 'read', 'table': 'Orders', 'key': 2}, {'type': 'write', 'table': 'OrderDetail', 'key': 2}],
        [{'type': 'write', 'table': 'Orders', 'key': 2}, {'type': 'read', 'table': 'OrderDetail', 'key': 2}],
        [{'type': 'read', 'table': 'Orders', 'key': 3}, {'type': 'write', 'table': 'OrderDetail', 'key': 3}],
        [{'type': 'write', 'table': 'Orders', 'key': 3}, {'type': 'read', 'table': 'OrderDetail', 'key': 3}],
        [{'type': 'read', 'table': 'Orders', 'key': 4}, {'type': 'write', 'table': 'OrderDetail', 'key': 4}],
        [{'type': 'write', 'table': 'Orders', 'key': 4}, {'type': 'read', 'table': 'OrderDetail', 'key': 4}],
        [{'type': 'read', 'table': 'Orders', 'key': 5}, {'type': 'write', 'table': 'OrderDetail', 'key': 5}],
        [{'type': 'write', 'table': 'Orders', 'key': 5}, {'type': 'read', 'table': 'OrderDetail', 'key': 5}]
    ]

    for transaction in transactions:
        cs.add_transaction(transaction)

    print("Conflict Serializability:", "Serializable" if cs.is_serializable() else "Not Serializable")

if __name__ == "__main__":
    db = Database()
    test_conflict_serializability(db)