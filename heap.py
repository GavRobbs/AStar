class Heap:
    """ Takes a custom comparator function. If you leave it as is, it functions as a min-heap. 
    If you use greater than instead of less than it becomes a max heap. It also allows you to manage
    custom data types, as long as they are comparable - you'll see me use this in the PriorityQueue"""
    def __init__(self, comparator = lambda x, y : x < y):
        self.elements = []
        self.comparator = comparator

    def parent(self, index):
        if index == 0:
            return None
        return max(index-1, 0) // 2
    
    def left_child(self, index):
        return 2 * index + 1
    
    def right_child(self, index):
        return 2 * index + 2
    
    def swap(self, index1, index2):
        if index1 == index2:
            return
        self.elements[index1], self.elements[index2] = self.elements[index2], self.elements[index1]

    def insert(self, element):
        #One useful property I rely on a lot is that the python len function operates in constant time
        self.elements.append(element)
        
        last_index = len(self.elements) - 1
        parent_index = self.parent(last_index)

        #Bubble up the value
        while parent_index != None:
            if self.comparator(element, self.elements[parent_index]):
                self.swap(parent_index, last_index)
                last_index = parent_index
                parent_index = self.parent(last_index)
            else:
                break

    def remove_top(self):

        if len(self.elements) == 0:
            return None
        
        if len(self.elements) == 1:
            return self.elements.pop()
        
        top_value = self.elements[0]
        self.elements[0] = self.elements[len(self.elements) - 1]
        self.elements.pop()

        last_value = self.elements[0]
        
        current_index = 0
        
        #Bubble down the value
        while True:

            lchild = self.left_child(current_index)
            rchild = self.right_child(current_index)

            if lchild >= len(self.elements):
                break
            elif rchild >= len(self.elements):
                break
            else:
                smaller_child = lchild if self.comparator(self.elements[lchild], self.elements[rchild]) else rchild

            if not self.comparator(last_value, self.elements[smaller_child]):
                self.swap(current_index, smaller_child)
                current_index = smaller_child
            else:
                break

        return top_value
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def __str__(self):
        return str(self.elements)

if __name__ == '__main__':
    myheap = Heap()

    print("This is the heap application. The default implementation used here in a min-heap.")
    print("Enter as many integer numbers as you like in random order, when you're done, type 'd'")

    entry_done = False

    while not entry_done:
        next_input = input("Enter a number: ")

        if next_input.lower() == 'd':
            entry_done = True
        else:
            myheap.insert(int(next_input))

    numbers_sorted = []

    while not myheap.is_empty():
        numbers_sorted.append(myheap.remove_top())

    print("The numbers you entered in ascending order are : " + str(numbers_sorted))