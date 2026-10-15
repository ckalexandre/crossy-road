import random

from src.game import constants


side = constants.CELL_SIZE # the width of every line


class Vehicle():
    def __init__(self, x, y, length, color, type):
        self.x = x
        self.y = y
        self.width = side
        self.length = length
        self.color = color
        self.type = type


class Player():
    def __init__(self, x, y):
        self.width = side
        self.height = side
        self.x = x
        self.y = y


class Wood():
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = side
        self.length = length


class Line():

    lilypads_generated = False

    def __init__(self, y, speed, road_type, list_cars, trees, rocks, lilypads, coin):
        self.y = y
        self.speed = speed
        self.road_type = road_type
        self.list_cars = list_cars
        self.trees = []
        self.rocks = []
        self.lilypads = []
        self.coin = []

        if road_type == "grass":
            self.generate_trees_rocks()
        if road_type == "water":
            self.generate_lilypad()
        else: # no coin in the water
            self.generate_coin()

    def generate_trees_rocks(self):
        """randomly generates trees and rocks on the grass"""
        if self.y != 90: # we don't modify the first generated line
            number_of_trees = random.randint(0, 3)
            number_of_rocks = random.randint(0, 2)
            if self.y != 190:
                x = [50, 150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1250]
            else:
                x = [50, 150, 250, 350, 450, 550, 750, 850, 950, 1050, 1150, 1250] # we can't generate a tree or a rock on the starting position of the player
            
            x_tree = []
            for i in range(number_of_trees):
                tree_x = random.choice(x)
                tree_y = 0
                self.trees.append((tree_x, tree_y,random.randint(8,9)))
                x_tree.append(tree_x)
            for i in range(number_of_rocks):
                x_rocks = [e for e in x if e not in x_tree] # the rocks can't get at the same place as the trees
                rocks_x = random.choice(x_rocks)
                rocks_y = 0
                self.rocks.append((rocks_x, rocks_y,random.randint(6,7)))

    def generate_lilypad(self):
        """randomly generates lilypads on the water (they might be replaced later in the verify_lilypad function)"""
        number_of_lilypad = random.randint(3, 5)
        x = [250, 350, 450, 550, 650, 750, 850, 950, 1050] # not on the edges
        if not Line.lilypads_generated: # we only generate lilypads once
            p = random.random()
            if p >= 0.3: # probability of 70 % to have lilypads on this line
                for i in range(number_of_lilypad):
                    lilypad_x = random.choice(x)
                    lilypad_y = 0
                    self.lilypads.append((lilypad_x, lilypad_y))
                Line.lilypads_generated = True
    
    def generate_coin(self):
        """randomly generates a coin on a line (but not in the water)"""
        p = random.random()
        proba_coin = 0.4
        
        if p <= proba_coin: # probability of 40 % to have a coin on a given line
            squares_x = [50, 150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1250]
            possible_x = []

            trees_of_line = self.trees
            trees_x = [trees_of_line[i][0] for i in range(len(trees_of_line))]

            rocks_of_line = self.rocks
            rocks_x = [rocks_of_line[i][0] for i in range(len(rocks_of_line))]

            for x in squares_x :
                if not (x in trees_x) and not (x in rocks_x) : # a coin can't be generated on a rock or a tree
                    possible_x.append(x)
            
            x = random.choice(possible_x)

            self.coin.append((x,0))
