import matplotlib.pyplot as plt
import numpy as np

def draw(pizza):
  for row in pizza:
    print(row)
    
# Read file
f = open("problems/a_example.in")
lines = f.readlines()
R, C, L, H = [int(x) for x in lines[0].split(" ")]
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

def findMinimumPartition(r, c):
  delta_coords = [(1,0), (0,1), (-1, 0), (0, -1)]
  center = pizza[r][c] # center point of the partition
  next_cell = center
  part = [(r, c)] # list of points of the partition
  # Counters for each ingredient
  lowestCount = 1
  highestCount = 0
  print("Start {}".format(pizza[r][c]))
  print("Find {}".format(next_cell))

  rl, rr = r,r
  cl, cr = c,c
  
  while True:
    for point in part:
      for (dr, dc) in delta_coords:
        x = point[0] + dr
        y = point[1] + dc
        if isValidPoint(x, y) and pizza[x][y] == next_cell and (x, y) not in cellstopart and (x, y) not in part:
          part.append((x, y))
          print("Found {} - r:{} c:{}".format(next_cell, x, y))
          if pizza[x][y] == center:
            lowestCount += 1
            if lowestCount == L:
              next_cell = 'M' if next_cell == 'T' else 'T'
              print("Switch")
          else:
            highestCount += 1
            if highestCount == L:
              return part
    return part


part = findMinimumPartition(1,1)
print(part)
exit()
# Phase 1
focus_finder = findNextFocus()
print(focus_cells)
# while True:
#     if not next(focus_finder): 
#         break #If no M available, break
#     parttocells[last_pid] = findMinimumPartition(next(focus_finder)) # Save partition
#     last_pid += 1

# # Phase 2
    
# print("Solution found:", parttocells)
