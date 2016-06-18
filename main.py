#!/usr/bin/env python3

import json
from housepy import util, drawing, log
from colors import colors

LENGTH = 50.0 # meters
TRANSECT = 1

gentraso = util.load("niwot.data")

transect = gentraso[TRANSECT]
species = list(set([tree['species'] for tree in transect]))
max_size = max(transect, key=lambda t: t['size'])['size']
log.info("TRANSECT %d" % TRANSECT)
log.info("SPECIES %s" % [species])
log.info("MAX_SIZE %f" % max_size)

ctx = drawing.Context(1000, 300, margin=20)
aspect = ctx.width / ctx.height
for tree in transect:
    radius_x = tree['size'] / LENGTH
    radius_y = radius_x * aspect
    ctx.arc(tree['distance'] / LENGTH, tree['size'] / max_size, radius_x, radius_y, fill=colors[species.index(tree['species']) % len(colors)], thickness=0)

for i, name in enumerate(species):
    ctx.line(10 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), 30 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), stroke=colors[i % len(colors)], thickness=2)
    ctx.label(35 / ctx.width, 1 - ((14 + (i * 10)) / ctx.height), name.upper(), size=8)    

ctx.output("output/")


