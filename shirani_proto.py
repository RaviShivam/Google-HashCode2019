import matplotlib.pyplot as plt
import numpy as np
from termcolor import colored

def draw(pizza):
  for row in pizza:
    print(row)
    
# Read file
f = open("problems/b_small.in")
lines = f.readlines()
R, C, L, H = lines[0].split(" ")
print(R, C, L, H)

pizza = []
tomatoCount = 0
mushroomCount = 0

# Parse file
for i in range(1, len(lines)):
    row = []
    for c in list(lines[i])[:-1]:
      row.append(c)

    tomatoCount += row.count('T')
    mushroomCount += row.count('M')
    pizza.append(row)

draw(pizza)
print("Tomato count: {}".format(tomatoCount))
print("Mushroom count: {}".format(mushroomCount))

cellstopart = { (0,0): 1, (0,1): 1, (0,2): 2, (0,3): 2 } # { (x,y): partition_id }
parttocells = {1: [(0, 0), (1, 0), (0, 1), (1, 1)]} # { partition_id: [(x, y)] }

colors = []

cid = 0
for r, row in enumerate(pizza):
  l = []
  for c, col in enumerate(row):
      part = cellstopart[(r, c)] if (r,c) in cellstopart else 0
      l.append("{:3s}".format(str(pizza[r][c]) + " " + str(part)))
  print(l)
      
      # colorpart = colored(pizza[r][c], part )
      # print(colorpart)



