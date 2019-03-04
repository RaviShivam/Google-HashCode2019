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
    def fitness (ind, data):
      fitness = 0
      for i in range(len(ind)-1):
        fitness += get_score(data[ind[i]], data[ind[i+1]])
      return fitness

    def create_individual(data):
      l = list(data.keys())
      shuffle(l)
      return l

    def mutate(individual):
      return individual

    slides_merged = get_merged_slides(parse_file(fn))
    slides_lookup = dict([(x[0], x) for x in slides_merged])
    ga = pyeasyga.GeneticAlgorithm(slides_lookup, population_size=10, generations=20)
    ga.fitness_function = fitness
    ga.create_individual = create_individual 
    ga.mutate_function = mutate
    ga.run()
    final_slideshow = [slides_lookup[i] for i in ga.best_individual()[1]]
    return final_slideshow

def write_to_file(fn, sol):
    myfile = open(fn, 'w')
    myfile.write("%s\n" % len(sol))

    for s in sol:
        myfile.write("%s\n" % s[0])
    myfile.close()


# all_files = ['a_example.txt', 'b_lovely_landscapes.txt', 'c_memorable_moments.txt', 'd_pet_pictures.txt', 'e_shiny_selfies.txt']
all_files = ['b_lovely_landscapes.txt']
# all_files = ['e_shiny_selfies.txt']
for f in all_files:
    print("Working on {}".format(f))
    solution = find_best_slideshow(f)
    write_to_file('solutions/{}'.format(f), solution)

