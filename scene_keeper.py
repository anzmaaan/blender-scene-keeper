import bpy

class ANZ_OT_scene_keeper(bpy.types.Operator):
    """Keep your blender scene organized and tidy. Creates collections for every object type in your scene, moves them to the appropriate collection, assigns 
prefixes based on type and checks for unnamed/default named objects."""
    bl_idname = "anz.scene_keeper"
    bl_label = "Scene Keeper"
    
    @classmethod
    def poll(cls, context):
        #print(f"My area is: {context.area.type}")
        return context.area.type == "VIEW_3D" or context.area.type == "OUTLINER"
    
    def execute(self, context):
        print("Executed Scene Keeper")
        
        ### VARIABLES
  
        objects = bpy.context.scene.objects

        types = []
        collection_names = ['_delete', 'mdl', 'lgt', 'cam', 'ctrl', 'rig', 'fx']
        prefixes = ['geo_', 'crv_', 'meta_', 'txt_', 'lgt_', 'cam_', 'ctrl_', 'rig_', 'fx_', 'RENAME_']
        fx_modifiers = ['CLOTH', 'COLLISION', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'FLUID']
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

        # Check if prefix in objects name (except "RENAME_")
        def prefix_applied(object):
                current_name = object.name
                index = current_name.find('_')
                prefix = object.name[0:index+1]
                
                if prefix in prefixes[0:-2]:
                    return True

        # Check if modifier exists on object
        def fx_modifier_applied(object):
            if object.modifiers:
                for modifier in object.modifiers:
                    for fx_modifier in fx_modifiers:
                        if modifier.type == fx_modifier:
                            return True


        ### CODE

        # go through all objects in this scene 
        for object in objects:
            # check objects type and store it in list "types"
            types.append(object.type)
            types = list(dict.fromkeys(types)) # remove duplicates from types
            # check if object has default name
            if object.name in default_names:
                # put "RENAME" into name if they use default name
                current_name = object.name
                object.name = prefixes[-1] + current_name
            # add appropriate prefix to objects name, determined by its type
            if prefix_applied(object):
                continue
            else:
                if object.type == 'MESH':
                    if fx_modifier_applied(object):
                        object.name = prefixes[8] + object.name
                    else:
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


        # create collection "_delete" no matter what, create collections from list "types" using names defined in list "collection_names" and link them to the outliner
        if collection_exists(collection_names[0]):
            pass
        else: 
            temp_collection = bpy.data.collections.new(collection_names[0])
            bpy.context.scene.collection.children.link(temp_collection) 

        for type in types:
            if type == 'MESH' or type == 'CURVE' or type == 'META' or type == 'FONT':
                if collection_exists(collection_names[1]):
                    continue
                else:
                    temp_collection = bpy.data.collections.new(collection_names[1])
                    bpy.context.scene.collection.children.link(temp_collection) 
                if collection_exists(collection_names[6]):
                    continue
                else:
                    temp_collection = bpy.data.collections.new(collection_names[6])
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
                if fx_modifier_applied(object):
                    bpy.data.collections[collection_names[6]].objects.link(object)
                else:
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
                
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(ANZ_OT_scene_keeper)
    
def unregister():
    bpy.utils.unregister_class(ANZ_OT_scene_keeper)
    
if __name__ == '__main__':
    register()