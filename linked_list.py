class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None

    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f" {str(node.data)} ->"
            if node.next_node is None:
                ll_string += " None"
            node = node.next_node
        print(ll_string)

######### example of LinkedList manually create node
# ll = LinkedList()
# node4 = Node("data4", None)
# node3 = Node("data3", node4)
# node2 = Node("data2", node3)
# node1 = Node("data1", node2)
#
# ll.head = node1
#
# ll.print_ll()

    def insert_beginning(self, data):
        # this if statement to keep track on the last_node to replace the while loop from insert_at_end method
        # so that the insert_at_end can be executed cleanly
        if self.head is None:
            self.head = Node(data, None)
            self.last_node = self.head

        new_node = Node(data, self.head)
        self.head = new_node

######### example of LinkedList with insert_beginning method
# ll = LinkedList()
# ll.insert_beginning("data")
# ll.insert_beginning("not data")
# ll.insert_beginning("cow")
# ll.print_ll()

    def insert_at_end(self, data):
        if self.head is None:
            self.insert_beginning(data)

        #### The whole section below can be deleted after adding an if statement on method insert_beginning
        #### to keep track on the last_node
        # if self.last_node is None:
        #     node = self.head
        #     while node.next_node:
        #         node_before = node  # extra code to check the node before then include it on print statement
        #         node = node.next_node
        #         print("iter", node.data, "-- node before = ", node_before.data)
        #
        #     node.next_node = Node(data, None)
        #     self.last_node = node.next_node
        #
        # else:
        self.last_node.next_node = Node(data, None)  # can be directly executed because the last_node is known
        self.last_node = self.last_node.next_node

ll = LinkedList()
ll.insert_beginning("data1")
ll.insert_beginning("data2")
ll.insert_beginning("data3")
ll.insert_beginning("data4")
ll.insert_beginning("data5")
ll.insert_beginning("data6")
ll.insert_beginning("data7")
ll.insert_beginning("data8")
ll.insert_beginning("data9")

ll.insert_at_end("end")
ll.insert_at_end("end2")

ll.print_ll()
