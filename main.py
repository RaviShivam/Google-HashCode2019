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
slides = []
for i in range(len(vert_only)):
    for j in range(i+1, len(vert_only)):
        tags = vert_only[i][2] | vert_only[j][2]
        new_slide = (vert_only[i][0], vert_only[j][0], 'V', tags, len(tags))
        slides.append(new_slide)

slides.sort(key = operator.itemgetter(4))
vert_exclude = set()
slides_filtered = []
for s in slides:
  if s[0] in vert_exclude or s[1] in vert_exclude:
    continue
  else:
    new_slide = (' '.join([str(s[0]), str(s[1])]), 'V', s[3])
    slides_filtered.append(new_slide)
    vert_exclude.add(s[0])
    vert_exclude.add(s[1])

slides_merged = [(str(x[0]), x[1], x[2]) for x in photos if x[1] == 'H'] + slides_filtered

