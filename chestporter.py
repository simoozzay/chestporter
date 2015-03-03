import json
from pymclevel import TAG_List, TAG_Compound, TAG_String, TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double
from pymclevel import alphaMaterials, MCSchematic, MCLevel

displayName = "Chestporter"
file = "/Users/simu/Downloads/chests.txt"

types = {"Chest":"Chest","Dispenser":"Trap","Dropper":"Dropper","Hopper":"Hopper","Furnace":"Furnace","Brewing Stand":"Cauldron",
			"Storage Minecart":"MinecartChest","Furnace Minecart":"MinecartFurnace","Hopper Minecart":"MinecartHopper"}

inputs = (
    ("Chestporter filter by simoozzay", "label"),
)

storageItems = [alphaMaterials.Chest.ID,alphaMaterials.TrappedChest.ID,alphaMaterials.Furnace.ID,alphaMaterials.LitFurnace.ID,alphaMaterials.Dispenser.ID,alphaMaterials.Hopper.ID,alphaMaterials.Dropper.ID]

def perform(level, box, options):
    # well you have to make a choice here... there is no gui or stuff...
    #exportChests(level, box, options)
    importChests(level, box, options)
    level.markDirtyBox(box)
    
def exportChests(level, box, options):
    print 'exportChest: Started!'
    entities = []
    
    for (chunk, slices, point) in level.getChunkSlices(box):
        for block in chunk.TileEntities:
            x = block["x"].value
            y = block["y"].value
            z = block["z"].value
            if (x,y,z) in box:
                if block["id"].value in types.values():
                    items = []
                    for item in block["Items"].value:
                        items.append({
                            "slot": item["Slot"].value,
                            "id": item["id"].value,
                            "count": item["Count"].value,
                            "damage": item["Damage"].value
                        })
                        print item["id"].value

                    entity = {
                        "x": x,
                        "y": y,
                        "z": z,
                        "items": items
                    }
                    entities.append(entity)
    
    with open(file, 'w') as outfile:
        json.dump(entities, outfile)

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def importChests(level, box, options):
    with open(file) as infile:
        entities = json.load(infile)
        
    for block in entities:
        if (block["x"],block["y"],block["z"]) in box:
            print "block found..."
            e = level.tileEntityAt((int)(block["x"]),(int)(block["y"]),(int)(block["z"]))
            if e["id"].value in types.values():
                if "Items" in e:
                    del e["Items"]
                e["Items"] = TAG_List()
                for item in block["items"]:
                    i = TAG_Compound()
                    id = item["id"]
                    if isNumber(id):
                        shortVal = True
                        id = int(id)
                    else:
                        shortVal = False
                    if shortVal:
                        i["id"] = TAG_Short(id)
                    else:
                        i["id"] = TAG_String(id)
                    i["Damage"] = TAG_Short(item["damage"])
                    i["Count"] = TAG_Byte(item["count"])
                    i["Slot"] = TAG_Byte(item["slot"])
                    e["Items"].append(i)
    for (chunk, slices, point) in level.getChunkSlices(box):
        chunk.dirty = True