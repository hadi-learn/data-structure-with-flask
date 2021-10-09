class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class Stack:
    def __init__(self):
        self.top = None

    # to peek the current top node
    def peek(self):
        return self.top

    # add new data to be the top node
    def push(self, data):
        next_node = self.top
        new_top = Node(data, next_node)
        self.top = new_top
        return

    def pop(self):
        if self.top is None:
            return None
        removed = self.top
        self.top = self.top.next_node
        return removed
