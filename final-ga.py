#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import operator
from pyeasyga import pyeasyga
from random import shuffle
import os
from tqdm import tqdm
import glob

def get_score(slide1, slide2):
  # print(slide1, slide2)
  (_, _, s1) = slide1
  (_, _, s2) = slide2
  return min(len(s1 - s2), len(s1 & s2), len(s2 - s1))

def parse_file(fn):
    lines = open(fn).readlines()
    # Global variable
    N = int(lines[0]) # number of photos
    photos = [] # (i :int , pos, tags: set[string]) where pos is V or H

    for (i, line) in enumerate(lines[1:]):
      items = line.replace("\n", "").split(" ")
      pos = items[0]
      size = int(items[1])
      tags = set(items[2:])
      photos.append((i, pos, tags))
    return photos

def get_merged_slides(photos):
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
    return slides_merged


# In[ ]:


def find_best_slideshow(fn):
    def fitness (individual, data):
      # print(len(individual), individual)
      fitness = 0
      for i in range(len(individual)-1):
        fitness += get_score(individual[i], individual[i+1])
      return fitness

    def create_individual(data):
      shuffle(data)
      return data

    def mutate(individual):
      return individual

    slides_merged = get_merged_slides(parse_file(fn))
    ga = pyeasyga.GeneticAlgorithm(slides_merged, generations=10)
    ga.fitness_function = fitness
    ga.create_individual = create_individual 
    ga.mutate_function = mutate
    ga.run()
    return ga.best_individual()[1]

def write_to_file(fn, sol):
    myfile = open(fn, 'w')
    myfile.write("%s\n" % len(sol))

    for s in sol:
        myfile.write("%s\n" % s[0])
    myfile.close()


# In[ ]:


all_files = ['a_example.txt', 'b_lovely_landscapes.txt', 'c_memorable_moments.txt', 'd_pet_pictures.txt', 'e_shiny_selfies.txt']
for f in tqdm(all_files):
    solution = find_best_slideshow(f)
    write_to_file('solutions/{}'.format(f), solution)

