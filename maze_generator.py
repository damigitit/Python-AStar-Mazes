# Author: Damian Archer
# Date: 4/9/2021
# Purpose: CIS 120 HW -- Algorithm Assignment
# Title: maze_generator.py

import random
"""
    Prim's randomized maze generation.
    
    1. Start with a grid full of walls.
        Note: I started with a grid full of unvisited 'u' locations.  For all we know,
              they could be walls, so we'll assume they are.
              
    2. Pick a random cell, and mark it as part of the maze.
        Add the walls surrounding that the cell to the walls list.
        
    3. While there are walls in the list:
    
        1. Pick a random wall from the list.
           If only one of the two cells that the
           wall divides is visited, then:
           
                a) Make the wall a passage and mark the unvisited cell
                    as part of the maze
                    
                b) Add the neighboring walls of the cell to the wall list.
                
        2. Remove the wall from the list.

"""
class maze_generator:

    def __init__(self,width=30,height=15,wall='#',cell=' '):
        """
            Creates a maze_generator object.
        """
        self.cell = cell
        self.wall = wall
        self.width = width
        self.height = height
        self.walls = []

        # grid begins
        # Step 1 and 2 happen within new_grid
        self.new_grid(self.width,self.height)
        # Step 3.1a, 3.1b, and 3.2 happen in make_maze and its helper methods.
        self.make_maze()
      
    def new_grid(self,width,height):
        """
            pre: an integer width and height are passed in
            post: makes self.grid a new unvisited grid,  creates
                  a random startpoint for algorithm, and visits
                  the first neighboring squares to make them into walls.
                  example: u is unvisited, and r is random spot.
                  
                            uuuuuuuuuu
                            uuuuwuuuuu
                            uuuwrwuuuu
                            uuuuwuuuuu
                            uuuuuuuuuu
                            uuuuuuuuuu
        """

        # 1. Start with a grid full of walls (or presumably walls)
        self.grid = [ ['u' for i in range(width)] for j in range(height)]

        # 2. Pick a random cell on the grid, and add the
        #    surrounding cells to the wall list.
        self.start = (x,y) = self.__random_start()
        self.grid[y][x] = self.cell
        self.visit_neighbors(self.start)
        
    def __random_start(self):
        """
            pre: self.grid must have been initialized.
            post: returns a random (x,y) coordinate that is not along the edge
                  of the grid
        """
        if self.grid is not None:
            return (random.randrange(1,len(self.grid[0])-1),random.randrange(1,len(self.grid)-1))
        else:
            raise Exception("self.grid was not initialized")

    def visit_neighbors(self, p):
        """
            pre: an (x,y) startpoint p is passed in.
            post: if the neighbor is on the grid and is not a cell,
                  it is made a wall.
        """   
        neighbors = [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
        for p in neighbors:
            if self.on_grid(p) and self.grid[p[1]][p[0]] == 'u':
                self.grid[p[1]][p[0]] = '#'
                self.walls.append((p[0],p[1]))

    def cell_count(self,grid,p):
        """
            pre: a grid[y][x] and an (x,y) point p are passed in.
            post: returns a count of the neighboring squares that are cells
        """
        neighbors = [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
        count = 0
        for p in neighbors:
            if grid[p[1]][p[0]] == ' ': count+=1
        return count

    def on_grid(self, p):
        """
            pre: an (x,y) startpoint p is passed in.
            post: if the point is on the grid, returns True.
                  Otherwise returns False
        """ 
        return 0 <= p[0] < len(self.grid[0]) and \
               0 <= p[1] < len(self.grid)
               
    def display(self,filename=None):
        """
            pre: if a filename is passed in, will print to a file,
                 else will print to console.
            post: the output is applied to the destination.
        """
        rows = []
        for row in self.grid:
            out = ''
            for item in row:
                out += item
            rows.append(out)

        if filename:
            f = open(filename, 'w')
            for row in rows: print(row,file=f)
            f.close()
        else:
            return rows

    def print_maze(self, filename=None):
        """
        pre: a maze has already been generated.
        post: prints the output of the last generated maze to the console, or an optional file.
        """
        if filename is not None:
            f = open(filename, 'w')
            for line in self.display(): print(line,file=f)
            f.close()
        else:
            for line in self.display(): print(line)
            

    def new_maze(self,width=30, height=15):
        """
        pre: an optional width and height is passed in
        post: generates a new maze and prints it to the console
        """
        self.new_grid(width,height)
        self.make_maze()
        self.print_maze()

    def make_maze(self):
        """
            pre: a random starting point on the grid has been chosen, and four
                 walls were initialized around that point.  This happens in the
                 new_grid function.

            post: the maze has been completed, the border is completely walled
                  in, except for the randomly chosen start and goal points.
        """
        
        # by the time make_maze begins, four walls should have been initialized
        # during the call to _random_start(). Or else, there is a problem.
        if not self.walls: raise Exception("No Walls initialized")

        # while there are walls in the list.  Choose a random wall, and visit
        # its check its neighbors (east and west, and then north and south)
        while self.walls:

            # walls get popped from self.walls here, and later in visit check
            # they conditionally are added back to the self.walls list
            # in calls to visit_neighbors.
            rdm_wall = self.walls.pop(random.randrange(len(self.walls)))
            self._visit_check(rdm_wall)
            
        # completes the surrounding border walls
        # closing the maze in.
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'u': self.grid[i][j] = '#'
                
        # selects a random start and goal
        self.start,self.goal = self.start_and_goal()
                
    def start_and_goal(self):
        """
            start and goal selects a random starting position
            and goal position along the border.

            post: a random point along the borders are chosen
                  for the start and goal.
        """
        grid_h = len(self.grid)

        grid_w = len(self.grid[0])
        #print('height is,', grid_h)
       #print('width is,',grid_w)
        
        while True:
            i = random.randrange(1, grid_w)
            if random.randrange(2) == 0:
                if self.grid[1][i] == ' ':
                    self.grid[0][i] = ' '
                    p1 =  (i,0)
                    break
            else:
                if self.grid[grid_h-2][i] == ' ':
                    self.grid[grid_h-1][i] = ' '
                    p1 = (i,grid_h-1)
                    break
        while True:
            j = random.randrange(1, grid_h)
            if random.randrange(2) == 0:
                if self.grid[j][1] == ' ':
                    self.grid[j][0] = ' '
                    p2 = (0,j)
                    break
            else:
                if self.grid[j][grid_w-2] == ' ':
                    self.grid[j][grid_w-1] = ' '
                    p2 = (grid_w-1,j)
                    break

        # For randomized direction of path.
        if random.randrange(2) == 1: return p1,p2
        else: return p2,p1
    
    def _visit_check(self,p):
        """
        pre: an (x,y) coordinate pair on the graph is passed in as p.
        post:
                if neighbor is cell and
                opposite neighbor unvisited and
                count of surrounding cells < 2:
                    the wall locaiton is made into a cell/hallway, and
                    the surrounding unvisited areas are confirmed as/become walls.
                    
        _visit_check is where most of the maze-making work is done.
        Checks left and right neighbors, and then top and bottom neighbors.
        """        
        g = self.grid
        x,y = p[0],p[1]
        # Directionals points
        west,east = (x-1,y),(x+1,y)
        north,south = (x,y-1),(x,y+1)

        # if the left (L) and right (R) points are on the grid
        if self.on_grid(west) and self.on_grid(east):
            
            # get the values from grid location associated with them.
            L,R = g[y][x-1],g[y][x+1]

            # if L == cell and right == unvisited.
            # or R == cell and right == unvisited.
            if (L == ' ') & (R == 'u') | \
               (L== 'u') & (R == ' '):

                # if surrounding cell count of p < 2
                # make the location a cell/hallway.
                if self.cell_count(g,p) < 2:
                    g[y][x] = ' '
                    # The unvisited neighbors are visited and made into walls
                    self.visit_neighbors(p)
                
        # Same process happens for the top (T) and bottom (B) neighbors.
        if self.on_grid(north) and self.on_grid(south):      
            T,B = g[y-1][x], g[y+1][x]  
            if (T == ' ') & (B == 'u') | \
               (T == 'u') & (B == ' '):            
                if self.cell_count(g,p) < 2:
                   g[y][x] = ' '
                   self.visit_neighbors(p)
          
if __name__ == '__main__':
    # can pass in different height and width,
    # has default of 30 by 15.
    mg = maze_generator()
    for i in (mg.display()):
        out = ''
        for c in i:
            out += c
        print(out)  
    
