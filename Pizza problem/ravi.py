import matplotlib.pyplot as plt
import numpy as np

def draw(pizza):
  for row in pizza:
    print(row)
    
# Read file
f = open("problems/a_example.in")
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
lowest = 'T' if tomatoCount < mushroomCount else 'M'

cellstopart = {} # { (x,y): partition_id }
parttocells = {} # { partition_id: [(x, y)] }
focus_cells = []
lr, lc = (0, 0)

# Check if point is in the grid
def isValidPoint(r, c):
  return r >= 0 and c >=0 and r < R and c < C

# Get a list of points of the least common ingredient
def findLowestCells():
    for r, row in enumerate(pizza):
        for c, cell in enumerate(row):
          if cell == lowest:
            focus_cells.append((r, c))

def findNextFocus():
    for e in focus_cells:
        yield (e, lowest)
    return None

# Phase 1
findLowestCells()
focus_finder = findNextFocus()
while True:
    a = next(focus_finder, None)
    print(a)
# for e in focus_finder:
#     print(e)
# last_pid = 1
# while True:
#     if not next(focus_finder): 
#         break #If no M available, break

#     # parttocells[last_pid] = findMinimumPartition(next(focus_finder)) # Save partition
#     print(next(focus_finder), last_pid)
#     last_pid += 1

# # Phase 2
    
# print("Solution found:", parttocells)
