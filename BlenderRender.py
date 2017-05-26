import sys, os, math, time, random, subprocess, numpy as np, bpy


class BlenderRender:

    '''
    initializes the blender scene
    with camera and lighting conditions
    '''
    def __init__(self, light_pos=[0,-10,3], light_energy=4.5):
        self.delete(lambda x: x.name != 'Camera')
        self.translate('Camera', [0, -10, 0])
        self.rotate('Camera', [90, 0, 0])

        bpy.ops.object.lamp_add(type='POINT')
        bpy.data.lamps['Point'].use_specular = True
        self.translate('Point', light_pos)
        bpy.data.lamps['Point'].energy = light_energy

        bpy.data.worlds['World'].horizon_color = (1, 1, 1)
        bpy.data.scenes['Scene'].render.resolution_percentage = 100

    '''
    save image
        path, name : strings
        name should not include extension
    '''
    def write(self, path, name, extension = '.png'):
        bpy.context.scene.render.filepath = os.path.join(path, name + '.' + extension)
        bpy.ops.render.render(write_still = True)

    '''
    hide all objects
    '''
    def hideAll(self):
        for obj in bpy.data.objects:
            obj.hide_render = True

    '''
    size : int
    '''
    def __scale(self, name, size):
        obj = bpy.data.objects[name]
        for dim in range(3):
            obj.scale[dim] = size

    '''
    converts inp to list if not already
    '''
    def __ensureList(self, inp):
        if type(inp) != list:
            inp = [inp]
        return inp

    '''
    scales many objects
    names : list of strings (for multiple objects) 
            or string (for single object)
    size : scale (int)
    ''' 
    def resize(self, names, size, dim=0):
        names = self.__ensureList(names)
        if type(names) == str:
            names = [names]
        for name in names:
            obj = bpy.data.objects[name]
            obj.dimensions[dim] = size
            scale = obj.scale[dim]
            self.__scale(name, scale)

    '''
    coords : [x,y,z] position
    '''
    def translate(self, names, coords):
        names = self.__ensureList(names)
        for name in names:
            obj = bpy.data.objects[name]
            for dim in range(3):
                obj.location[dim] = coords[dim]

    '''
    angles : [rot_x, rot_y, rot_x] angles (in degrees)
    '''
    def rotate(self, names, angles):
        names = self.__ensureList(names)
        for name in names:
            obj = bpy.data.objects[name]
            for dim in range(3):
                obj.rotation_euler[dim] = self.__toRadians(angles[dim])

    '''
    deletes all objects for which 
    function(object.name) is true
    '''
    def delete(self, function):
        for obj in bpy.data.objects:
            if function(obj):
                obj.select = True
            else:
                obj.select = False
        bpy.ops.object.delete()

    '''
    converts degrees to radians
    '''
    def __toRadians(self, degree):
        return degree * math.pi / 180.

    '''
    selects all objects for which
    function(object.name) is true
    '''
    def __select(self, function):
        for obj in bpy.data.objects:
            if function(obj):
                obj.select = True
            else:
                obj.select = False

    '''
    make duplicate of object
    by specifying old and new name
    '''
    def duplicate(self, old, new):
        self.__select(lambda x: x.name == old)
        bpy.ops.object.duplicate()
        obj = bpy.data.objects[old + '.001']
        obj.name = new



