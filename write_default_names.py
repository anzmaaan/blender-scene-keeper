import bpy

objects = bpy.context.scene.objects
f = open("D://3D//Blender//Scripting//blender-scene-keeper//blender_default_names.txt", "x")

for object in objects:
    f.write(object.name + "\n")
    
f.close()