import heap

class PriorityQueue:
    def __init__(self):
        self.backing_queue = heap.Heap()

    def insert(self, value):
        self.backing_queue.insert(value)

    def get_highest_priority(self):
        return self.backing_queue.remove_top()
    
    def is_empty(self):
        return self.backing_queue.is_empty()
    
    def set_comparator(self, comp_func):
        self.backing_queue.comparator = comp_func
    
if __name__ == "__main__":
    #For this example, I'm using a tuple as object to insert. Tuples have lexicographical sorting, which means
    #they are compared elementwise left to right until an inequality is found. Semantically, this doesn't matter
    #too much to us here, because if two entries have the same priority, then it doesn't really matter which one
    #comes first, but for more fine grained control, the priority queue can set the custom comparator
    mypq = PriorityQueue()

    #I'm inserting these out of order on purpose
    mypq.insert((500, "Leave home"))
    mypq.insert((2, "Brush teeth"))
    mypq.insert((32, "Get dressed"))
    mypq.insert((2, "Shower"))
    mypq.insert((1, "Have breakfast"))
    mypq.insert((0, "Wake up"))

    while not mypq.is_empty():
        print(mypq.get_highest_priority())
