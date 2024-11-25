import threading
import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


class PaxosNode:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes
        self.proposal_number = 0
        self.promised_number = 0
        self.accepted_value = None
        self.accepted_number = 0
        self.quorum_size = len(nodes) // 2 + 1
        self.lock = threading.Lock()

    def prepare(self, proposal_number):
        with self.lock:
            if proposal_number > self.promised_number:
                self.promised_number = proposal_number
                logging.debug(f"Node {self.node_id} promised number {proposal_number}")
                return self.accepted_number, self.accepted_value
        return None

    def accept(self, proposal_number, value):
        with self.lock:
            if proposal_number >= self.promised_number:
                self.promised_number = proposal_number
                self.accepted_value = value
                self.accepted_number = proposal_number
                logging.debug(f"Node {self.node_id} accepted value {value} with number {self.accepted_number}")
                return True
        return False

    def propose(self, value):
        self.proposal_number += 1
        logging.debug(f"Node {self.node_id} proposing value {value} with proposal number {self.proposal_number}")

        # 1阶段：准备
        promises = []
        for node_id, node in self.nodes.items():
            if node_id != self.node_id:
                response = node.prepare(self.proposal_number)
                if response:
                    promises.append(response)

        if len(promises) < self.quorum_size:
            logging.warning(f"Node {self.node_id} failed to achieve quorum in Prepare phase")
            return False

        # 选取最高值作为接收值
        max_accepted_number = -1
        final_value = value
        for num, val in promises:
            if num > max_accepted_number and val is not None:
                max_accepted_number = num
                final_value = val

        # 2阶段：接受
        accepts = 0
        for node_id, node in self.nodes.items():
            if node_id != self.node_id:
                if node.accept(self.proposal_number, final_value):
                    accepts += 1

        if accepts >= self.quorum_size:
            logging.debug(f"Node {self.node_id} achieved consensus on value {final_value}")
            self.accepted_value = final_value
            return True

        logging.warning(f"Node {self.node_id} failed to achieve quorum in Accept phase")
        return False


def test_paxos():
    num_nodes = 5
    nodes = {i: PaxosNode(i, {}) for i in range(num_nodes)}

    # Connect nodes
    for i in range(num_nodes):
        nodes[i].nodes = nodes

    # Propose random values
    values = [random.randint(1, 100) for _ in range(num_nodes)]
    logging.debug(f"Proposed values: {values}")

    with ThreadPoolExecutor(max_workers=num_nodes) as executor:
        futures = [executor.submit(nodes[i].propose, values[i]) for i in range(num_nodes)]
        for i, future in enumerate(futures):
            try:
                result = future.result(timeout=5)  # 设置超时时间
                logging.debug(f"Node {i} proposal result: {result}")
            except TimeoutError:
                logging.error(f"Node {i} proposal timed out")
            except Exception as e:
                logging.error(f"Node {i} proposal failed: {e}")

    final_values = [node.accepted_value for node in nodes.values()]
    print(f"Final values: {final_values}")
    logging.debug(f"Consensus value: {set(v for v in final_values if v is not None)}")


if __name__ == "__main__":
    test_paxos()
