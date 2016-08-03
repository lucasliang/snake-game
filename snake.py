import random
from graphics import *
import time
from msvcrt import getch
import threading

window_length = 480
window_width = 480
board_length = 20
board_width = 20

class Location(object):
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
    def conflict (self, other_loc):
        return (self.x == other_loc.x) and (self.y == other_loc.y)
    def __eq__(self, other):
        if not type(other) is Location:
            return False
        return self.conflict(other)
    
def moveInDirection (location, direction):
    if direction == 0:
        return Location(location.x+1,location.y)
    elif direction == 90:
        return Location(location.x,location.y-1)
    elif direction == 180:
        return Location(location.x-1,location.y)
    elif direction == 270:
        return Location(location.x,location.y+1)

class Snake(object):
    def __init__(self):
        self.locations = []
        self.direction = 90 #clockwise from x-axis
    def moveForward(self):
        new_head = moveInDirection(self.locations[0], self.direction)
        if self.hasConflict(new_head):
            return False
        if new_head.x < 0 or new_head.x > board_width+1 or new_head.y < 0 or new_head.y > board_length+1:
            return False
        self.locations.insert(0, new_head)
        return self.locations.pop()
    def hasConflict(self, newLoc):
        for loc in self.locations:
            if loc.conflict(newLoc):
                return True
        return False
    def changeDirection(self, newDirection):
        self.direction = newDirection

class Board(object):
    def __init__(self):
        self.snake = Snake()
        self.length = board_length #NOTE: the way I have this set up, locations are actually 1 indexed
        self.width = board_width
        self.availableLocations = [Location(x,y) for x in range(1,self.length+1) for y in range(1,self.length+1)]
        self.apple = self.generateLocation()
        self.snake.locations.append(Location(10,10))
        self.score = 0
        self.playing = True
    def generateLocation(self):
        nonConflicts = self.availableLocations
        for loc in nonConflicts:
            if loc in self.snake.locations:
                nonConflicts.remove(loc)
        return random.sample(nonConflicts,1)[0]
    def advanceBoard(self):
        result = self.snake.moveForward()
        if result == False:
            self.playing = False
            return False
        elif self.apple.conflict(self.snake.locations[0]):
            self.snake.locations.append(result) #add back last square
            self.apple = self.generateLocation()
            self.score += 1
            return True
        return True

def initiateFrame(board):
    #draw lines
    win = GraphWin("Snake Window", window_length, window_width)
    for row in range(board.length):
        l = Line(Point(row*(window_length/board.length),0), Point(row*(window_length/board.length),window_width))
        l.draw(win)
    for col in range(board.width):
        l = Line(Point(0,(col*(window_width/board.width))), Point(window_length,(col*(window_width/board.width))))
        l.draw(win)
    return(win)


def redrawFrame(board, win):
    squares = []
    for loc in board.snake.locations:
        r = Rectangle(Point(((loc.x-1) * (window_width/board.width)), (loc.y-1) * (window_length/board.length)), Point(((loc.x) * (window_width/board.width)), (loc.y) * (window_length/board.length)))
        r.setFill('green')
        squares.append(r)
        r.draw(win)
    loc = board.apple
    r = Rectangle(Point(((loc.x-1) * (window_width/board.width)), (loc.y-1) * (window_length/board.length)), Point(((loc.x) * (window_width/board.width)), (loc.y) * (window_length/board.length)))
    r.setFill('yellow')
    squares.append(r)
    r.draw(win)
    return squares

def run(board):
    while board.playing:
        key = ord(getch())
        if key == 80:
            board.snake.changeDirection(270)
        elif key == 72:
            board.snake.changeDirection(90)
        elif key == 75:
            board.snake.changeDirection(180)
        elif key == 77:
            board.snake.changeDirection(0)
        elif key == 27:
            break

print("Click the command prompt window for the keyboard controls to register!")
b = Board()
threading.Thread(target=run, args=(b,), name="thread_function").start()
w = initiateFrame(b)
locs = redrawFrame(b, w)
count = 0
while b.advanceBoard():
    time.sleep(0.4)
    for loc in locs:
        loc.undraw()
    locs = redrawFrame(b, w)
w.close()
print("Game Over!")
print("Your score: ", b.score)
threading.Thread
exit()