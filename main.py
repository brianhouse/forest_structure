#!/usr/bin/env python3

import json
from housepy import util, drawing, log
from colors import colors

LENGTH = 50.0 # meters
TRANSECT = 1

# load data
gentraso = util.load("niwot.data")
transect = gentraso[TRANSECT]
species = list(set([tree['species'] for tree in transect]))
max_size = max(transect, key=lambda t: t['size'])['size']
log.info("TRANSECT %d" % TRANSECT)
log.info("SPECIES %s" % [species])
log.info("MAX_SIZE %f" % max_size)

# plot trees
ctx = drawing.Context(1000, 300, margin=20)
aspect = ctx.width / ctx.height
for tree in transect:
    radius_x = tree['size'] / LENGTH
    radius_y = radius_x * aspect
    ctx.arc(tree['distance'] / LENGTH, tree['size'] / max_size, radius_x, radius_y, fill=colors[species.index(tree['species']) % len(colors)], thickness=0)
# labels
for i, name in enumerate(species):
    ctx.line(10 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), 30 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), stroke=colors[i % len(colors)], thickness=2)
    ctx.label(35 / ctx.width, 1 - ((14 + (i * 10)) / ctx.height), name.upper(), size=8)    
ctx.output("output/")

# music time
from braid import *
DURATION = 30.0

# set up voices
voices = []
for s, name in enumerate(species):
    voices.append(Voice(s, rate=1, chord=(C, MAJ), controls={'volume': 20}))

# tree notes
for t, tree in enumerate(transect):
    seconds = (tree['distance'] / LENGTH) * DURATION
    vi = species.index(tree['species'])
    voices[vi].play_at(seconds, vi + 1, tree['size'] / max_size)

play()
