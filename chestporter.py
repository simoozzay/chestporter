from pymclevel import alphaMaterials, MCSchematic, MCLevel

inputs = (
    ("Chestporter filter by simoozzay", "label"),
    ("StorageItems", (alphaMaterials.Chest,alphaMaterials.TrappedChest,alphaMaterials.Furnace,alphaMaterials.LitFurnace,alphaMaterials.Dispenser,alphaMaterials.Hopper,alphaMaterials.Dropper))
)

displayName = "Chestporter"

def perform(level, box, options):
    exportChests(level, box, options)
    level.markDirtyBox(box)
    
def exportChests(level, box, options):
    print 'exportChest: Started!'
    storageItems = myOptions["StorageItems"]
    
    for iterY in xrange(box.miny,box.maxy): #height
        for iterZ in xrange(box.minz,box.maxz): #depth
            for iterX in xrange(box.minx,box.maxx): # width
                block = level.blockAt(iterX, iterY, iterZ)
                for storageItem in storageItems:
                    if block == storageItem.ID:
                        print 'item %s found at x: %s y: %s z: %s!' % (block, iterX, iterY, iterZ)
                        