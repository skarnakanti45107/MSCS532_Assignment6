import ctypes

# ==========================================
# 1. Arrays and Matrices
# ==========================================
class DynamicArray:
    """
    A dynamic array implementation from scratch, managing its own capacity 
    and memory rather than relying on Python's built-in dynamic list features.
    """
    def __init__(self):
        self.size = 0          # Number of elements currently in the array
        self.capacity = 1      # Actual memory capacity
        self.array = self._make_array(self.capacity)

    def _make_array(self, capacity):
        # Creates a raw, fixed-size C-style array
        return (capacity * ctypes.py_object)()

    def _resize(self, new_capacity):
        new_array = self._make_array(new_capacity)
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def access(self, index):
        if not 0 <= index < self.size:
            raise IndexError("Index out of bounds")
        return self.array[index]

    def insert(self, index, value):
        if not 0 <= index <= self.size:
            raise IndexError("Index out of bounds")
        if self.size == self.capacity:
            self._resize(2 * self.capacity) # Double capacity when full
        
        # Shift elements to the right to make room
        for i in range(self.size - 1, index - 1, -1):
            self.array[i + 1] = self.array[i]
            
        self.array[index] = value
        self.size += 1

    def delete(self, index):
        if not 0 <= index < self.size:
            raise IndexError("Index out of bounds")
        
        # Shift elements to the left to fill the gap
        for i in range(index, self.size - 1):
            self.array[i] = self.array[i + 1]
            
        self.array[self.size - 1] = None # Clear the last reference
        self.size -= 1
        
    def __str__(self):
        return "[" + ", ".join(str(self.array[i]) for i in range(self.size)) + "]"


class Matrix:
    """
    A 2D Matrix implemented using a 1D Array to demonstrate 
    row-major order memory management.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Initialize a 1D array of size rows * cols
        self.data = [0] * (rows * cols)

    def _get_index(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds")
        return row * self.cols + col

    def access(self, row, col):
        return self.data[self._get_index(row, col)]

    def insert(self, row, col, value):
        self.data[self._get_index(row, col)] = value
        
    def display(self):
        for r in range(self.rows):
            row_data = [self.access(r, c) for c in range(self.cols)]
            print(row_data)


# ==========================================
# 2. Stacks and Queues (Array-based)
# ==========================================
class ArrayStack:
    """
    A LIFO Stack implemented using an array.
    """
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.array = [None] * capacity
        self.top = -1 # Points to the top element

    def is_empty(self):
        return self.top == -1

    def push(self, value):
        if self.top + 1 == self.capacity:
            raise OverflowError("Stack is full (Overflow)")
        self.top += 1
        self.array[self.top] = value

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack (Underflow)")
        value = self.array[self.top]
        self.array[self.top] = None # Clear reference
        self.top -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.array[self.top]


class ArrayQueue:
    """
    A FIFO Queue implemented using a circular array to ensure
    O(1) time complexity for both enqueue and dequeue operations.
    """
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.array = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def enqueue(self, value):
        if self.size == self.capacity:
            raise OverflowError("Queue is full")
        # Circular increment
        self.rear = (self.rear + 1) % self.capacity
        self.array[self.rear] = value
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        value = self.array[self.front]
        self.array[self.front] = None
        # Circular increment
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value


# ==========================================
# 3. Linked Lists
# ==========================================
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_tail(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, key):
        """Deletes the first occurrence of the key."""
        current = self.head
        
        # If head node itself holds the key
        if current is not None and current.data == key:
            self.head = current.next
            current = None
            return

        # Search for the key, keeping track of previous node
        prev = None
        while current is not None and current.data != key:
            prev = current
            current = current.next

        # Key was not present
        if current is None:
            return

        # Unlink the node
        prev.next = current.next
        current = None

    def traverse(self):
        """Returns a list of all elements in the linked list."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# ==========================================
# Functional Testing
# ==========================================
if __name__ == "__main__":
    print("--- Testing Dynamic Array ---")
    arr = DynamicArray()
    arr.insert(0, 10)
    arr.insert(1, 20)
    arr.insert(1, 15) # Insert 15 between 10 and 20
    print(f"Array after insertions: {arr}")
    arr.delete(0)
    print(f"Array after deleting index 0: {arr}\n")

    print("--- Testing Matrix ---")
    mat = Matrix(2, 3) # 2 rows, 3 cols
    mat.insert(0, 0, 1)
    mat.insert(0, 2, 5)
    mat.insert(1, 1, 9)
    mat.display()
    print()

    print("--- Testing Stack ---")
    stack = ArrayStack(5)
    stack.push(100)
    stack.push(200)
    print(f"Popped from stack: {stack.pop()}")
    print(f"Current top of stack: {stack.peek()}\n")

    print("--- Testing Circular Queue ---")
    queue = ArrayQueue(5)
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print(f"Dequeued: {queue.dequeue()}")
    queue.enqueue("D")
    print(f"Next in line is: {queue.array[queue.front]}\n")

    print("--- Testing Singly Linked List ---")
    llist = SinglyLinkedList()
    llist.insert_at_tail(1)
    llist.insert_at_tail(2)
    llist.insert_at_head(0)
    print(f"Linked List: {llist.traverse()}")
    llist.delete(1)
    print(f"After deleting '1': {llist.traverse()}")