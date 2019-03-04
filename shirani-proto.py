import operator
from pyeasyga import pyeasyga
from random import shuffle
import os
from tqdm import tqdm
import glob

def get_score(slide1, slide2):
  (_, _, s1, _) = slide1
  (_, _, s2, _) = slide2
  return min(len(s1 - s2), len(s1 & s2), len(s2 - s1))

def parse_file(fn):
    lines = open(fn).readlines()
    photos = [] # (i :int , pos, tags: set[string]) where pos is V or H

    for (i, line) in enumerate(lines[1:]):
      items = line.replace("\n", "").split(" ")
      pos = items[0]
      tags = set(items[2:])
      photos.append((i, pos, tags))
    return photos

def get_merged_slides(photos):
    vert_only = [(x[0], x[1], x[2], len(x[2])) for x in photos if x[1] == 'V']
    vert_only.sort(key = operator.itemgetter(3))
    print('number of vertical images: {}'.format(len(vert_only)))
    slides = []
    for i in tqdm(range(len(vert_only))):
      c = 100
      for j in range(i+1, len(vert_only)):
        tags = vert_only[i][2] | vert_only[j][2]
        new_slide = (vert_only[i][0], vert_only[j][0], 'V', tags, len(vert_only[i][2] & vert_only[j][2])/len(vert_only[i][2] | vert_only[j][2]))
        slides.append(new_slide)
        if c == 0: break
        c -= 1
    slides.sort(key = operator.itemgetter(4))
    vert_exclude = set()
    slides_filtered = []
    for s in slides:
      if s[0] in vert_exclude or s[1] in vert_exclude:
        continue
      else:
        new_slide = (' '.join([str(s[0]), str(s[1])]), 'V', s[3], len(s[3]))
        slides_filtered.append(new_slide)
        vert_exclude.add(s[0])
        vert_exclude.add(s[1])
    slides_merged = [(str(x[0]), x[1], x[2], len(x[2])) for x in photos if x[1] == 'H'] + slides_filtered
    return slides_merged

def find_best_slideshow(fn):
    slides_merged = get_merged_slides(parse_file(fn))
    slides_merged.sort(key = operator.itemgetter(3))
    print("found merged slides")
    remaining_slides = slides_merged[:]
    slideshow = [remaining_slides.pop(0)]
    while True:
      c, best_i, best_score = 1000, -1, -1
      for ci, slide in enumerate(remaining_slides):
        if c == 0: break
        if get_score(slide, slideshow[-1]) > best_score:
          best_i = ci
          best_score = get_score(slideshow[-1], slide)
        c -= 1
      slideshow.append(remaining_slides.pop(best_i))
      if len(remaining_slides) % 1000 == 0: print(len(remaining_slides))
      if (len(remaining_slides)==0): break
    return slideshow

def write_to_file(fn, sol):
    myfile = open(fn, 'w')
    myfile.write("%s\n" % len(sol))

    for s in sol:
        myfile.write("%s\n" % s[0])
    myfile.close()


all_files = ['a_example.txt', 'b_lovely_landscapes.txt', 'c_memorable_moments.txt', 'd_pet_pictures.txt', 'e_shiny_selfies.txt']
# all_files = ['a_example.txt']
# all_files = ['b_lovely_landscapes.txt']
# all_files = ['c_memorable_moments.txt']
# all_files = ['d_pet_pictures.txt']
# all_files = ['e_shiny_selfies.txt']
for f in all_files:
    solution = find_best_slideshow(f)
    write_to_file('solutions_shirani/{}'.format(f), solution)

