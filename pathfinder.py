import priorityqueue

#This is a grid based implementation of the A* algorithm using a priority queue
class PathfindingMap:
    def __init__(self, gmap, map_w, map_h, show_details=False):
        self.grid_map = gmap
        self.map_width = map_w
        self.map_height = map_h
        self.detail_mode = show_details

    def coordinates_to_index(self, x, y):
        #Converts x, y coordinates to an array index on the map
        return y * self.map_width + x
    
    def index_to_coordinates(self, index):
        #Converts an array index to x,y coordinates
        return (index % self.map_width, index//self.map_width)
    
    def _filter_node(self, t):
        #We filter coordinates bigger than the size of the map
        #And also filter out unwalkable areas
        if t[0] >= 0 and t[0] < self.map_width and t[1] >= 0 and t[1] < self.map_height:
            ind = self.coordinates_to_index(t[0], t[1])
            if self.grid_map[ind] == '1':
                return True
            
        return False

    def get_adjacent_nodes(self, x, y):

        node_array = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        
        #We filter this array to ensure all of the adjacent nodes returned are valid
        return [x for x in filter(self._filter_node, node_array)]
    
    def calculate_heuristic(self, current_pair, end_pair):
        #Just used Manhattan distance here to keep it simple
        return abs(end_pair[1] - current_pair[1]) + (end_pair[0] - current_pair[0])

    def find_path(self, start_pair, end_pair):
        distance_map = [float('inf') for element in self.grid_map]
        predecessors = {}
        start_index = self.coordinates_to_index(start_pair[0], start_pair[1])
        end_index = self.coordinates_to_index(end_pair[0], end_pair[1])
        distance_map[start_index] = 0.0
        
        already_visited = set()

        if self.detail_mode:
            print("Finding a path from " + str(start_pair) + " to " + str(end_pair))

        #We add our starting point to the priority queue to kick off the algorithm
        path_pq = priorityqueue.PriorityQueue()
        path_pq.insert((0.0 + self.calculate_heuristic(start_pair, end_pair), start_pair))

        if self.detail_mode:
            print("Inserted the starting point into the priority queue with a weight of 0")

        while not path_pq.is_empty():
            #Get the point at the top of the priority queue
            #That would be the lowest cost point
            visiting = path_pq.get_highest_priority()

            if self.detail_mode:
                print("Currently visiting " + str(visiting[1]))

            #This is a little confusing but remember that its stored in the heap as (priority, (x, y))
            neighbours = self.get_adjacent_nodes(visiting[1][0], visiting[1][1])

            if self.detail_mode:
                print("The neighbours of  " + str(visiting[1]) + " are " + str(neighbours))

            visiting_index = self.coordinates_to_index(visiting[1][0], visiting[1][1])
            already_visited.add(visiting[1])

            #We visit each neighbour
            for neighbour in neighbours:
                if self.detail_mode:
                    print("Currently visiting neighbour " + str(neighbour) + " from " + str(visiting[1]))

                #if the neighour has already been visited, we can move on
                if neighbour in already_visited:
                    if self.detail_mode:
                        print("This neighbour has already been visited")
                    continue

                #We calculate the tentative cost from the current node to the neighbour at the moment
                #All path weights are the same in this example, so we can just add a constant 1.0
                tentative_cost = distance_map[visiting_index] + 1.0

                #Use neighbour_index for easier array access
                neighbour_index = self.coordinates_to_index(neighbour[0], neighbour[1])

                #If the tentative cost to the neighbour through the node we are currently visiting
                #is less than whatever it currently is, we replace it and let add it to the predecessors list
                if tentative_cost < distance_map[neighbour_index]:
                    if self.detail_mode:
                        print("We found a new low cost path to this neighbour via our current visiting node")

                    distance_map[neighbour_index] = tentative_cost
                    predecessors[neighbour_index] = visiting_index
                    path_pq.insert((tentative_cost + self.calculate_heuristic(neighbour, end_pair), neighbour))

        final_path = []

        if self.detail_mode:
            print("The predecessor list is now: " + str(predecessors))
            print("Going to read this from end to start and then reverse it to get the path")

        next_node_index = end_index
        while next_node_index != start_index:
            final_path.append(next_node_index)
            next_node_index = predecessors[next_node_index]

        final_path.append(start_index)
        final_path.reverse()
        return [self.index_to_coordinates(index) for index in final_path]
    
    def print_map(self, start_pos, end_pos, path_tracked = None):
        printable_map = list(self.grid_map)

        if path_tracked is not None:
            for coord in path_tracked:
                printable_map[self.coordinates_to_index(coord[0], coord[1])] = '.'

        printable_map[self.coordinates_to_index(start_pos[0], start_pos[1])] = '+'
        printable_map[self.coordinates_to_index(end_pos[0], end_pos[1])] = 'X'
        for i in range(0, self.map_width * self.map_height, self.map_width):
            print(printable_map[i:i+self.map_width])


if __name__ == '__main__':
    nav_map_raw = "0001000" + "0001000" + "0001110" + "0111010" + "0101010" + "0101010" + "0000000"
    pf = PathfindingMap(nav_map_raw, 7, 7, False)
    path = pf.find_path((3, 0), (1, 5))
    print(path)
    print("Here is the map. Your start point is shown by a + and your end point is shown by an X, and the . represents the path taken.")
    pf.print_map((3, 0), (1, 5), path)
    print("You can rerun this with PathfindingMap.show_details set to True to watch the algorithm work")

