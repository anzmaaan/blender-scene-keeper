import bpy
import os

### variables

objects = bpy.context.scene.objects
collection_names = ['_delete', 'geo', 'lgt', 'cam', 'ctrl', 'rig']
types = []


# go through all objects in this scene, check their type and store it in list "types"
for object in objects:
    types.append(object.type)
    types = list(dict.fromkeys(types)) # remove duplicates from types

# create collection "_delete" no matter what, create collections from list "types" using names defined in list "collection_names" and link them to the outliner
temp_collection = bpy.data.collections.new(collection_names[0])
bpy.context.scene.collection.children.link(temp_collection)

for type in types:
    if type == 'MESH':
        temp_collection = bpy.data.collections.new(collection_names[1])
        bpy.context.scene.collection.children.link(temp_collection)
    elif type == 'LIGHT':
        temp_collection = bpy.data.collections.new(collection_names[2])
        bpy.context.scene.collection.children.link(temp_collection)
    elif type == 'CAMERA':
        temp_collection = bpy.data.collections.new(collection_names[3])
        bpy.context.scene.collection.children.link(temp_collection)
    elif type == 'EMPTY':
        temp_collection = bpy.data.collections.new(collection_names[4])
        bpy.context.scene.collection.children.link(temp_collection)
    elif type == 'ARMATURE':
        temp_collection = bpy.data.collections.new(collection_names[5])
        bpy.context.scene.collection.children.link(temp_collection)
        
# go through all objects in this scene, unlink them from current collection and move them to the appropriate collection or to "_delete"
for object in objects:
    
    for collection in object.users_collection:
            collection.objects.unlink(object)
            
    if object.type == 'MESH':
        bpy.data.collections[collection_names[1]].objects.link(object)
    elif object.type == 'LIGHT':
        bpy.data.collections[collection_names[2]].objects.link(object)
    elif object.type == 'CAMERA':
        bpy.data.collections[collection_names[3]].objects.link(object)
    elif object.type == 'EMPTY':
        bpy.data.collections[collection_names[4]].objects.link(object)
    elif object.type == 'ARMATURE':
        bpy.data.collections[collection_names[5]].objects.link(object)
    else:
        bpy.data.collections[collection_names[0]].objects.link(object)
        
# go through all collections and add the collections name as a prefix to the childrens name 
for collection in bpy.data.collections:
    if collection.name != "_delete":
        prefix = collection.name + "_"
        for object in collection.all_objects:
            object.name = prefix + object.name
        
        
### DEBUG   
#os.system("cls")
#bpy.app.debug_wm = True