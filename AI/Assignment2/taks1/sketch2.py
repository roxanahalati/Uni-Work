

# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                
        return imagine        
        

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:        
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                 self.y = self.y + 1
                  
    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        
        return mapImage


class PriorityQueue:
    def __init__(self):
        self._queue = {}

    def isEmpty(self):
        return len(self._queue) == 0

    def pop(self):
        top_priority = None
        top_obj = None
        for obj in self._queue:
            obj_priority = self._queue[obj]
            if top_priority is None or top_priority > obj_priority:
                top_priority = obj_priority
                top_obj = obj
        del self._queue[top_obj]
        return top_obj

    def push(self, obj, priority):
        self._queue[obj] = priority

def manhattan(x1,y1,x2,y2):
    #In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is | x1 - x2 | + | y1 - y2 |
    return abs(x1-x2) + abs(y1-y2)

def searchAStar(mapM, droneD, initialX, initialY, finalX, finalY):
    found = False
    visited = []
    toVisit = PriorityQueue()
    toVisit.push((initialX,initialY),0)
    prev = {}
    cost = {}
    cost[(initialX,initialY)] = 0

    while not toVisit.isEmpty() and found == False:
        current = toVisit.pop()
        visited.append(current)

        if current == (finalX,finalY):
            found = True
        else:

            if current[1] < 19:
                if (current[0],current[1] + 1) not in visited and mapM.surface[current[0], current[1] + 1] == 0:
                    cost[(current[0],current[1] + 1)] = cost[current[0],current[1]] + 1
                    nodeCost = manhattan(current[0],current[1]+1,finalX,finalY) + cost[(current[0],current[1] + 1)]
                    toVisit.push((current[0],current[1]+1), nodeCost)
                    prev[(current[0],current[1]+1)] = (current[0],current[1])

            if current[0] < 19:
               if (current[0] + 1,current[1]) not in visited and mapM.surface[current[0] + 1, current[1]] == 0:
                   cost[(current[0] + 1, current[1])] = cost[current[0], current[1]] + 1
                   nodeCost = manhattan(current[0] + 1, current[1], finalX, finalY) + cost[((current[0] + 1, current[1]))]
                   toVisit.push((current[0] + 1, current[1]), nodeCost)
                   prev[(current[0] + 1, current[1])] = (current[0], current[1])

            if current[1] > 0:
                if (current[0],current[1] - 1 ) not in visited and mapM.surface[current[0], current[1] - 1] == 0:
                    cost[(current[0],current[1] - 1 )] = cost[(current[0],current[1])] + 1
                    nodeCost = manhattan(current[0],current[1] - 1 , finalX, finalY) + cost[((current[0],current[1] - 1 ))]
                    toVisit.push((current[0], current[1] - 1), nodeCost)
                    prev[(current[0], current[1] - 1)] = (current[0], current[1])


            if current[0] > 0:
              if (current[0] - 1 ,current[1]) not in visited and mapM.surface[current[0] -1, current[1]] == 0:
                  cost[((current[0] - 1, current[1]))] = cost[(current[0],current[1])] + 1
                  nodeCost = manhattan(current[0] - 1, current[1], finalX, finalY) + cost[(((current[0] - 1, current[1])))]
                  toVisit.push((current[0] -1 , current[1]), nodeCost)
                  prev[(current[0] - 1, current[1])] = (current[0], current[1])

    path = []
    pathPos = (finalX, finalY)
    pathFinish = (initialX, initialY)
    while pathPos != pathFinish:
        path.append([pathPos[0], pathPos[1]])
        pathPos = prev.get(pathPos)
    path.append([pathPos[0], pathPos[1]])
    path.reverse()
    # print(path)
    return path



def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY):
    found = False
    visited = []
    toVisit = PriorityQueue()
    toVisit.push((initialX,initialY),0)
    prev = {}


    while not toVisit.isEmpty() and found==False:
        #if toVisit.isEmpty():
          # return False

        current = toVisit.pop()
        visited.append(current)

        if current == (finalX,finalY):
            found = True
        else:
            aux = []

            if current[1] < 19:
                if (current[0],current[1] + 1) not in visited and mapM.surface[current[0], current[1] + 1] == 0:
                    cost = manhattan(current[0],current[1]+1,finalX,finalY)
                    toVisit.push((current[0],current[1]+1), cost)
                    prev[(current[0],current[1]+1)] = (current[0],current[1])

            if current[0] < 19:
               if (current[0] + 1,current[1]) not in visited and mapM.surface[current[0] + 1, current[1]] == 0:
                   cost = manhattan(current[0] + 1, current[1], finalX, finalY)
                   toVisit.push((current[0] + 1, current[1]), cost)
                   prev[(current[0] + 1, current[1])] = (current[0], current[1])

            if current[1] > 0:
                if (current[0],current[1] - 1 ) not in visited and mapM.surface[current[0], current[1] - 1] == 0:
                    cost = manhattan(current[0],current[1] - 1 , finalX, finalY)
                    toVisit.push((current[0], current[1] - 1), cost)
                    prev[(current[0], current[1] - 1)] = (current[0], current[1])


            if current[0] > 0:
              if (current[0] - 1 ,current[1]) not in visited and mapM.surface[current[0] -1, current[1]] == 0:
                  cost = manhattan(current[0] - 1, current[1], finalX, finalY)
                  toVisit.push((current[0] -1 , current[1]), cost)
                  prev[(current[0] - 1, current[1])] = (current[0], current[1])


    path = []
    pathPos = (finalX, finalY)
    pathFinish = (initialX,initialY)
    while pathPos != pathFinish:
        path.append([pathPos[0], pathPos[1]])
        pathPos = prev.get(pathPos)
    path.append([pathPos[0], pathPos[1]])
    path.reverse()
    #print(path)
    return path

def searchBFS(mapM, droneD, initialX, initialY, finalX, finalY):
    found = False
    visited = []
    toVisit = []
    toVisit.append((initialX,initialY))
    prev = {}

    while len(toVisit)!=0 and found == False:
        current = toVisit.pop()
        visited.append(current)

        if current == (finalX,finalY):
            found = True
        else:
           aux = []

           if current[1] < 19:
               if (current[0], current[1] + 1) not in visited and mapM.surface[current[0], current[1] + 1] == 0:
                   prev[(current[0], current[1] + 1)] = (current[0], current[1])
                   aux.append((current[0], current[1] + 1))

           if current[0] < 19:
               if (current[0] + 1, current[1]) not in visited and mapM.surface[current[0] + 1, current[1]] == 0:
                   prev[(current[0] + 1, current[1])] = (current[0], current[1])
                   aux.append((current[0] + 1, current[1]))

           if current[1] > 0:
               if (current[0], current[1] - 1) not in visited and mapM.surface[current[0], current[1] - 1] == 0:
                   prev[(current[0], current[1] - 1)] = (current[0], current[1])
                   aux.append((current[0], current[1] - 1))

           if current[0] > 0:
               if (current[0] - 1, current[1]) not in visited and mapM.surface[current[0] - 1, current[1]] == 0:
                    prev[(current[0] - 1, current[1])] = (current[0], current[1])
                    aux.append((current[0] - 1, current[1]))

           toVisit.extend(aux)

    path = []
    pathPos = (finalX, finalY)
    pathFinish = (initialX, initialY)
    while pathPos != pathFinish:
        path.append([pathPos[0], pathPos[1]])
        pathPos = prev.get(pathPos)
    path.append([pathPos[0], pathPos[1]])
    path.reverse()
    # print(path)
    return path





def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
    
def displayWithPath(image, path):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))
        
    return image

                  
# define a main function
def main():
    
    # we create the map
    m = Map() 
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")
    
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")
        
    # we position the drone somewhere in the area
    #x = randint(0, 19)
    #y = randint(0, 19)
    x = 5
    y = 15
    #create drona
    d = Drone(x, y)

    #create endpoint
    #finalX = randint(0, 19)
    #finalY = randint(0, 19)
    #while m.surface[finalX, finalY] != 0:
    #    finalX = randint(0, 19)
    #    finalY = randint(0, 19)

    finalX = 18
    finalY = 0

    print('Start at:', x, y)
    print('Reach: ', finalX, finalY)
    
    
    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)
    
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == KEYDOWN:
                d.move(m)
                running = False  # this call will be erased

        
        
        screen.blit(d.mapWithDrone(m.image()),(0,0))
        pygame.display.flip()

    path = searchBFS(m,d,x,y,finalX,finalY)
    print(len(path))
    screen.blit(displayWithPath(m.image(), path),(0,0))
    
    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()