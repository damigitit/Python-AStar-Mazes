from maze_generator import maze_generator
from queue import PriorityQueue
import tkinter as tk
import time
from math import sqrt

class WeightedGrid:   
    def __init__(self, width, height):
        """
            creates a WeightedGrid object
            
            pre: int width and height are passed in
            post: an empty grid with a empty list of obstructions and an
                 empty dict of (location,weights) k,v pairs is created
        """
        self.width = width
        self.height = height
        self.obstructions = []
        self.weights = {}
        print("total map area is ",width*height)

    def on_grid(self,location):
        """
            pre: location (x,y) is passed in
            post: if it is within bounds of the grid, returns True, else False
        """
        return 0 <= location[0] < self.width and 0 <= location[1] < self.height

    def traversable(self,location):
        """
            pre: location (x,y) is passed in
            post: if the location is in the list of obstructions, returns False
                  otherwise returns True
        """
        if location in self.obstructions: return False
        else: return True
        
    def neighbors(self,p):
        """
            pre: a location is passed in
            post: returns a list of valid_moves.  valid_moves are
                    1) on the grid, and
                    2) traversable
        """     
        x,y = p[0],p[1]
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # There is an explanation for this next snippet in the "Ugly Path" section
        # from the article I used as a source.
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E       
        valid_moves = filter(self.on_grid, neighbors)
        valid_moves = filter(self.traversable, valid_moves)
        return valid_moves

    
    def cost(self, A, B):
        """
            pre: A is current location, B is destination location.
            post: returns weight value of B if the location's weight has been calculated,
                    or 1 otherwise.
        """
        return self.weights.get(B, 1)


def heuristic(p, goal):
    """
        manhattan heuristic
        pre: 'p' and 'goal' are (x,y) coordinates
        post: returns the calculated distance between the points.
    """   
    return sqrt((p[0] - goal[0])**2 +(p[1] - goal[1])**2)


class AStarMaze(tk.Frame):
    """
        Tkinter driver
    """
    def __init__(self,width,height):
        super().__init__()
        self.master.title("AStar")
        self.width = width
        self.height = height
        self._screen()        
        self.grid(row=0,
                  column=0,
                  sticky=tk.N+tk.S+tk.E+tk.W)

        self.mg = maze_generator()
        self.mg.new_grid(width,height)
        self.mg.make_maze()   

        # create a WeightedGrid to use with the A* search
        self.wgrid = WeightedGrid(self.width,self.height)

        """#<-- Adjust comments to alternate between behaviors
        # use this block of code to see the cool maze example
        fip = open('cool_maze.txt', 'r')
        lines = [line.strip() for line in fip]
        self.wgrid.obstructions = self.walls_from_maze(lines)
        self.start =  (11,1)
        self.goal = (39,39)
        # """
     
        #<-- use this block of code to generate random mazes
        self.wgrid.obstructions = self.walls_from_maze(self.mg.display())
        self.start = self.mg.start
        self.goal = self.mg.goal
        print("start is",self.start)
        print("goal is", self.goal)
         
        
        self.path_from = self.a_star_search(self.wgrid,
                                            self.start,
                                            self.goal)
        
        
        # Configurations to make window resizable
        self.top = self.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.columnconfigure(0,minsize=960, weight=1)
        self.rowconfigure(0,minsize=640, weight=1)
        self._draw_weighted_grid(self.wgrid,self.retrace_steps(self.path_from,
                                                           start=self.start,
                                                           goal=self.goal))
        self.gfx.bind('<Configure>', self.__redraw)


    def _screen(self):
        """
            _screen() is a helper method used to create the canvas
        """
        self.gfx = tk.Canvas(
            self,
            bg="#111",
            width=480,
            height=320,
            relief="ridge")
        self.gfx.grid(row=0,
                      column=0,
                      sticky=tk.N+tk.S+tk.E+tk.W)


    def _draw_weighted_grid(self, g, path):
        """
            _draw_weighted_grid is used to draw the maze onto the canvas
        """
        self.update_idletasks()

        # used to calculate the size of a location for drawing.
        x = int(self.top.winfo_width())/self.width
        y = int(self.top.winfo_height())/self.height
        locX,locY = 0,0

        """ draws all the walls """
        for i in range(self.height):
            for n in range(self.width):
                if (n,i) in g.obstructions:
                    self.gfx.create_rectangle(locX,locY,locX+x,locY+y,fill="#ddd",stipple='gray75',outline="gray")
                elif (n,i) == self.start:
                    self.gfx.create_rectangle(locX,locY,locX+x,locY+y,fill="#f00")
                elif (n,i) == self.goal:
                    self.gfx.create_rectangle(locX,locY,locX+x,locY+y,fill="#00f")
                else: pass
                self.gfx.update()
                locX += x
            locX = 0
            locY += y
        locY = 0

        """ then draws the path found by the A*"""
        for i in path:
            if not i in [self.start, self.goal]:
                locX += x*i[0]
                locY += y*i[1]
                self.gfx.create_rectangle(locX,locY,locX+x,locY+y,fill="#99ff44",outline="black")
                self.gfx.update()
                time.sleep(0.01)
                locX = 0
                locY = 0
                 
    def __redraw(self, event):
        """ __redraw() is an event handler for events fired
                by configuring (resizing) the window
        """
        
        self.gfx.create_rectangle(0, 0, int(self.gfx.winfo_width()), int(self.top.winfo_height()), fill="#111", outline="#eee")     
        self._draw_weighted_grid(self.wgrid,self.retrace_steps(self.path_from,
                                                                   start=self.start,
                                                                 goal=self.goal))

    def walls_from_maze(self, display):
        """
            pre: display is a list of rows with in the maze. Each row is a string representation
                 of the row
                 post: if the (x,y) locaito of the character is a wall '#', location is appended to
                       walls list, walls list is returned.
        """
        walls = []
        loc = [0,0]
        for line in display:
            for c in line:
                loc[1] += 1
                if c == "#": walls.append((loc[1]-1, loc[0]))
            loc[1] = 0
            loc[0] += 1
        return walls

    def retrace_steps(self, path_from, start, goal):
        """
        pre: path_from is the path taken to get from start to goal,
             start and goal are (x,y) tuple coordinates.
        post: path_from is traced back to the start, and each location is appended to the
                path[] list. The list is reversed to reflect the actual order of the path.
                finally path is returned.
        """
        at = goal
        path = []
        while at != start:
            path.append(at)
            at = path_from[at]
        path.append(start)
        path.reverse()
        print(f'steps to goal: {len(path)}')
        return path
            
    def a_star_search(self, graph, start, goal):
        """
            A* search used with a weighted_grid to
               find shortest path from start to goal.
                        
            pre: graph is th weighted_grid, start and goal are (x,y) coordinates
            post: finds shortest path using manhattan distance heuristic
            
        """

        # create a priority queue for the frontier and add the start
        frontier = PriorityQueue()
        frontier.put(start, 0)

        # an empty dictionary to store the path from start to current locations along the way.
        path_from = {}

        # an empty dictionary to store the cost of moving to a location from start.
        accumulated_cost = {}
        # the accumulated_cost of being at the start point is 0
        accumulated_cost[start] = 0
        # start has no parent location
        path_from[start] = None

        # while exploring.
        while not frontier.empty():

            # get the priority
            at = frontier.get()

            # if we are at the goal, break out.
            if at == goal: break

            # otherwise... for available neighboring destinations 'to' from 'at', do the following.
            for to in graph.neighbors(at):

                # new cost is the sum of the accumulated cost of the current 'at' location and the
                # cost of the next location 'to'.  'to' has either been explored already and has a weight,
                # or it is unexplored and the added cost to move is accumulated_cost[at] + 1
                new_cost = accumulated_cost[at] + graph.cost(at,to)

                # if destination 'to' not in the dictionary of locations that have had their
                # costs from start calculated, or the new_cost of reaching the location 'to'
                # is less than the previously recorded cost of reaching 'to',
                # then set the new_cost, and place 'to' back into the priority queue with
                # a newly calculated priority.
                if to not in accumulated_cost or new_cost < accumulated_cost[to]:
                    accumulated_cost[to] = new_cost

                    # priority is calculated by adding the new cost of reaching location 'to'
                    # plus the calculated manhattan distance of goal from that location.
                    priority = new_cost + heuristic(to, goal)
                    frontier.put(to, priority)

                    # the move is recorded in the path_from dictionary
                    path_from[to] = at

        return path_from


if __name__ == '__main__':
    app = AStarMaze(80,40)
    # The only way out is in...

    


