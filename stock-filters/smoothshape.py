# Enlarge Filter by SethBling
# Feel free to modify and reuse, but credit to SethBling would be nice.
# http://youtube.com/sethbling

from numpy import zeros

inputs = (
    ("Smoothing", (1, 1, 20)),
    ("Made by Sethbling", "label")
)

displayName = "Smooth - 3D"

def perform(level, box, options):
    smoothing = options["Smoothing"]
    
    width = box.maxx - box.minx
    height = box.maxy - box.miny
    depth = box.maxz - box.minz

    blocks = zeros((width, height, depth))
    dmgs = zeros((width, height, depth))

    cache = {}

    for dx in range(width):
        for dy in range(height):
            for dz in range(depth):
                x = box.minx + dx
                y = box.miny + dy
                z = box.minz + dz

                (block, dmg) = getSmoothed(level, x, y, z, smoothing, cache)

                blocks[dx, dy, dz] = block
                dmgs[dx, dy, dz] = dmg

    for dx in range(width):
        for dy in range(height):
            for dz in range(depth):
                x = box.minx + dx
                y = box.miny + dy
                z = box.minz + dz

                level.setBlockAt(x, y, z, blocks[dx, dy, dz])
                level.setBlockDataAt(x, y, z, dmgs[dx, dy, dz])

    level.markDirtyBox(box)
    

def getSmoothed(level, x, y, z, smoothing, cache):
    counts = {}
    
    for dx in range(-smoothing, smoothing):
        for dy in range(-smoothing, smoothing):
            for dz in range(-smoothing, smoothing):
                if dx*dx + dy*dy + dz*dz > smoothing*smoothing:
                    continue

                cx = x + dx
                cy = y + dy
                cz = z + dz

                block = 0
                dmg = 0

                if not (cx, cy, cz) in cache:
                    block = level.blockAt(cx, cy, cz)
                    dmg = level.blockDataAt(cx, cy, cz)
                    cache[(cx, cy, cz)] = (block, dmg)
                else:
                    (block, dmg) = cache[(cx, cy, cz)]

                if not (block, dmg) in counts:
                    counts[(block, dmg)] = 0

                counts[(block, dmg)] = counts[(block, dmg)] + 1

    maxcount = 0
    maxbl = (0, 0)
    
    for (bl, count) in counts.items():
        if count > maxcount:
            maxcount = count
            maxbl = bl

    return maxbl
