import bpy

### VARIABLES

types = []
objects = bpy.context.scene.objects
collection_names = ['_delete', 'mdl', 'lgt', 'cam', 'ctrl', 'rig', 'fx', 'RENAME']
prefixes = ['geo_', 'crv_', 'meta_', 'txt_', 'lgt_', 'cam_', 'ctrl_', 'rig_', 'RENAME_']
default_names = [
    "Plane",
    "Cube",
    "Circle",
    "Sphere",
    "Icosphere",
    "Cylinder",
    "Cone",
    "Torus",
    "Grid",
    "Suzanne",
    "BezierCurve",
    "BezierCircle",
    "NurbsCurve",
    "NurbsCircle",
    "NurbsPath",
    "Mball",
    "Text",
    "Armature",
    "Lattice",
    "Empty",
    "Point",
    "Sun",
    "Spot",
    "Area",
    "Camera",
    "Field",
]


### FUNCTIONS

# Check if a collection already exists in this scene
def collection_exists(collection_name):
    for collection in bpy.data.collections:
        if collection.name == collection_name:
            return True

def prefix_exists(object):
        current_name = object.name
        index = current_name.find('_')
        prefix = object.name[0:index+1]
        
        if prefix in prefixes:
            return True

   
### CODE

# go through all objects in this scene, check their type and store it in list "types"
for object in objects:
    types.append(object.type)
    types = list(dict.fromkeys(types)) # remove duplicates from types

# go through all objects and check if they have the default name
for object in objects:
    # put prefix "rename_" if they use default name
    if object.name in default_names:
        current_name = object.name
        object.name = prefixes[8] + current_name
        
# create collection "_delete" no matter what, create collections from list "types" using names defined in list "collection_names" and link them to the outliner
if collection_exists(collection_names[0]):
    pass
else: 
    temp_collection = bpy.data.collections.new(collection_names[0])
    bpy.context.scene.collection.children.link(temp_collection) 

for type in types:
    if type == 'MESH' or type == 'CURVE' or type == 'META' or type == 'TEXT':
        if collection_exists(collection_names[1]):
            continue
        else: 
            temp_collection = bpy.data.collections.new(collection_names[1])
            bpy.context.scene.collection.children.link(temp_collection) 
    elif type == 'LIGHT':
        if collection_exists(collection_names[2]):
            continue
        else: 
            temp_collection = bpy.data.collections.new(collection_names[2])
            bpy.context.scene.collection.children.link(temp_collection) 
    elif type == 'CAMERA':
        if collection_exists(collection_names[3]):
            continue
        else: 
            temp_collection = bpy.data.collections.new(collection_names[3])
            bpy.context.scene.collection.children.link(temp_collection) 
    elif type == 'EMPTY' or type == 'LATTICE':
        if collection_exists(collection_names[4]):
            continue
        else: 
            temp_collection = bpy.data.collections.new(collection_names[4])
            bpy.context.scene.collection.children.link(temp_collection) 
    elif type == 'ARMATURE':
        if collection_exists(collection_names[5]):
            continue
        else: 
            temp_collection = bpy.data.collections.new(collection_names[5])
            bpy.context.scene.collection.children.link(temp_collection) 
        
# go through all objects in this scene, unlink them from current collection and move them to the appropriate collection or to "_delete"
for object in objects:
    
    for collection in object.users_collection:
            collection.objects.unlink(object)
            
    if object.type == 'MESH' or object.type == 'CURVE' or object.type == 'META' or object.type == 'FONT':
        bpy.data.collections[collection_names[1]].objects.link(object)
    elif object.type == 'LIGHT':
        bpy.data.collections[collection_names[2]].objects.link(object)
    elif object.type == 'CAMERA':
        bpy.data.collections[collection_names[3]].objects.link(object)
    elif object.type == 'EMPTY' or object.type == 'LATTICE':
        bpy.data.collections[collection_names[4]].objects.link(object)
    elif object.type == 'ARMATURE':
        bpy.data.collections[collection_names[5]].objects.link(object)
    else:
        bpy.data.collections[collection_names[0]].objects.link(object)
            
# go through all objects and add appropriate prefix to its name, determined by its type
for object in objects:
    if prefix_exists(object):
        continue
    else:
        if object.type == 'MESH':
            object.name = prefixes[0] + object.name
        elif object.type == 'CURVE':
            object.name = prefixes[1] + object.name
        elif object.type == 'META':
            object.name = prefixes[2] + object.name
        elif object.type == 'FONT':
            object.name = prefixes[3] + object.name
        elif object.type == 'LIGHT':
            object.name = prefixes[4] + object.name
        elif object.type == 'CAMERA':
            object.name = prefixes[5] + object.name
        elif object.type == 'EMPTY' or object.type == 'LATTICE':
            object.name = prefixes[6] + object.name
        elif object.type == 'ARMATURE':
            object.name = prefixes[7] + object.name
        
        
### DEBUG   
#bpy.app.debug_wm = True