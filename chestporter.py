import json
from pymclevel import alphaMaterials, MCSchematic, MCLevel

displayName = "Chestporter"

inputs = (
    ("Chestporter filter by simoozzay", "label"),
)

storageItems = [alphaMaterials.Chest.ID,alphaMaterials.TrappedChest.ID,alphaMaterials.Furnace.ID,alphaMaterials.LitFurnace.ID,alphaMaterials.Dispenser.ID,alphaMaterials.Hopper.ID,alphaMaterials.Dropper.ID]

def perform(level, box, options):
    exportChests(level, box, options)
    level.markDirtyBox(box)
    
def exportChests(level, box, options):
    print 'exportChest: Started!'
    entities = []
    
    for (chunk, slices, point) in level.getChunkSlices(box):
        for block in chunk.TileEntities:
            if block["Items"]:
                x = block["x"].value
                y = block["y"].value
                z = block["z"].value
                
                items = []
                for item in block["Items"].value:
                    items.append({
                        "slot": item["Slot"].value,
                        "id": item["id"].value,
                        "count": item["Count"].value,
                        "damage": item["Damage"].value
                    })
                    
                entities.append({
                    "x": x,
                    "y": y,
                    "z": z,
                    "items": items
                })
                print entities