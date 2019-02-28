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

def total_score(slideshow):
  score = 0
  for i in range(1, len(slideshow)):
    score += get_score(photos[slideshow[i-1]], photos[slideshow[i]])
  return score

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

def find_tag(new):
  for n in new:
    (_, _, tags) = photos[n]
    for tag in tags:
      if tag in ds:
        return tag


# print(choose_next(0))
# print(get_score(photos[0], photos[3]))
mapall()

bigbois = []
for k, v in tag_to_id.items():
  if len(v) > 2:
    bigbois.append((k, v))
    # print("{:>10}".format(k), "  " + str(v))
s = sorted(bigbois, key=lambda x: len(x[1]))
ds = dict(s)
# s = dict(s)
# for k, v in s:
    # print("{:>10}".format(k), "  " + str(v))
print(len(s))
slideshow = s[-1]

print(slideshow)
exit()
added = {}
c = 0



# print(slideshow)

print(len(slideshow))
print(slideshow)
# print(total_score(slideshow))
