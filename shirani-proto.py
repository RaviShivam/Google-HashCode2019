import sys
file = "a_example.txt" if len(sys.argv) == 1 else sys.argv[1]
lines = open(file).readlines()
tag_to_id = {}

def printall():
  for r in photos:
    print(r)

# Global variable
N = int(lines[0]) # number of photos
photos = [] # (i :int , pos, tags: set[string]) where pos is V or H

for (i, line) in enumerate(lines[1:]):
  items = line.replace("\n", "").split(" ")
  pos = items[0]
  size = int(items[1])
  tags = set(items[2:])
  photos.append((i, pos, tags))
# printall()

slideshow = []

def get_score(slide1, slide2):
  (_, _, s1) = slide1
  (_, _, s2) = slide2
  return min(len(s1 - s2), len(s1 & s2), len(s2 - s1))

def mapall():
  for (i, pos, tags) in photos:
    for tag in tags:
      if tag not in tag_to_id:
        tag_to_id[tag] = [i]
      else:
        tag_to_id[tag].append(i)

def choose_next(startindex):
    slide0 = photos[startindex]
    (i, pos, tags) = slide0
    maxi = -1
    max_score = 0
    for j in range(N):
        if i == j: continue
        score = get_score(slide0, photos[j])
        if score > max_score:
          maxi = j
          max_score = score
    return maxi, max_score

# print(choose_next(0))
# print(get_score(photos[0], photos[3]))
mapall()

bigbois = []
for k, v in tag_to_id.items():
  if len(v) > 2:
    bigbois.append((k, v))
    # print("{:>10}".format(k), "  " + str(v))

s = sorted(bigbois, key=lambda x: len(x[1]))
for k, v in s:
    print("{:>10}".format(k), "  " + str(v))
slideshow = [0]
added = {}
c = 0

# while True:
#   print('Slide {}'.format(slideshow[-1]))
#   tag, ids = s[slideshow[-1]]
#   sids = sorted(ids, key=lambda x: len(photos[x][2]))
#   for id in sids:
#     if id not in added:
#       slideshow.append(id)
#       added[id] = True
#   c += 1
#   if c == 2: break

print(slideshow)


