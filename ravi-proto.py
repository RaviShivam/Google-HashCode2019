import operator
lines = open("c_memorable_moments.txt").readlines()

def get_score(slide1, slide2):
  (_, _, s1) = slide1
  (_, _, s2) = slide2
  print(s1)
  print(s2)
  return min(len(s1 - s2), len(s1 & s2), len(s2 - s1))

# Global variable
N = int(lines[0]) # number of photos
photos = [] # (i :int , pos, tags: set[string]) where pos is V or H

for (i, line) in enumerate(lines[1:]):
  items = line.replace("\n", "").split(" ")
  pos = items[0]
  size = int(items[1])
  tags = set(items[2:])
  photos.append((i, pos, tags))

vert_only = [x for x in photos if x[1] == 'V']
vert_combi = []
for i in range(len(vert_only)):
    for j in range(i+1, len(vert_only)):
        tags = vert_only[i][2] | vert_only[j][2]
        new_slide = (' '.join([str(vert_only[i][0]), str(vert_only[j][0])]), 'V', tags, len(tags))
        vert_combi.append(new_slide)

vert_combi.sort(key = operator.itemgetter(3))

