#!/usr/bin/env python3

import json
from housepy import util, drawing, log
from colors import colors

LENGTH = 50.0 # meters
COLORS = {  'contorta':     colors[0], 
            'engelmannii':  colors[1],
            'lasiocarpa':   colors[2],
            'flexilis':     colors[3]
            }


gentraso = util.load("niwot.data")

transect = gentraso[1]
# print(json.dumps(transect, indent=4))
print(set([tree['species'] for tree in transect]))

max_size = max(transect, key=lambda t: t['size'])['size']
log.info("MAX_SIZE: %f" % max_size)

ctx = drawing.Context(1000, 300, margin=20)
aspect = ctx.width / ctx.height
for tree in transect:
    radius_x = tree['size'] / LENGTH
    radius_y = radius_x * aspect
    ctx.arc(tree['distance'] / LENGTH, tree['size'] / max_size, radius_x, radius_y, fill=COLORS[tree['species']], thickness=0)

ctx.output("output/")