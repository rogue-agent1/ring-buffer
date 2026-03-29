#!/usr/bin/env python3
"""Lock-free ring buffer (circular buffer) for embedded/real-time use."""
import sys

class RingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = self.tail = 0
        self.count = 0
    def push(self, item):
        if self.count == self.capacity: return False
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.count += 1; return True
    def pop(self):
        if self.count == 0: return None
        item = self.buffer[self.head]
        self.head = (self.head + 1) % self.capacity
        self.count -= 1; return item
    def peek(self):
        return self.buffer[self.head] if self.count > 0 else None
    def is_full(self): return self.count == self.capacity
    def is_empty(self): return self.count == 0
    def __len__(self): return self.count
    def to_list(self):
        result = []
        idx = self.head
        for _ in range(self.count):
            result.append(self.buffer[idx])
            idx = (idx + 1) % self.capacity
        return result
    def clear(self): self.head = self.tail = self.count = 0

class OverwriteRingBuffer(RingBuffer):
    def push(self, item):
        if self.count == self.capacity:
            self.head = (self.head + 1) % self.capacity
            self.count -= 1
        return super().push(item)

def main():
    if len(sys.argv) < 2: print("Usage: ring_buffer.py <demo|test>"); return
    if sys.argv[1] == "test":
        rb = RingBuffer(4)
        assert rb.is_empty(); assert len(rb) == 0
        rb.push(1); rb.push(2); rb.push(3); rb.push(4)
        assert rb.is_full(); assert not rb.push(5)
        assert rb.peek() == 1; assert rb.pop() == 1; assert len(rb) == 3
        rb.push(5); assert rb.to_list() == [2, 3, 4, 5]
        rb.clear(); assert rb.is_empty()
        # Overwrite buffer
        ob = OverwriteRingBuffer(3)
        ob.push(1); ob.push(2); ob.push(3)
        ob.push(4)  # overwrites 1
        assert ob.to_list() == [2, 3, 4]
        ob.push(5); assert ob.to_list() == [3, 4, 5]
        assert ob.pop() == 3
        # Empty pop
        rb2 = RingBuffer(2); assert rb2.pop() is None
        assert rb2.peek() is None
        print("All tests passed!")
    else:
        rb = RingBuffer(8)
        for i in range(10): print(f"Push {i}: {'OK' if rb.push(i) else 'FULL'}")
        print(f"Contents: {rb.to_list()}")

if __name__ == "__main__": main()
