import sys, os, math, argparse, time, random, subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--x_res', default=300,
    help='x dim of rendered image')
parser.add_argument('--y_res', default=300,
    help='y dim of rendered image')
parser.add_argument('--light_pos', default=[0,-10,3], 
    help='lights [x,y,z] position')
parser.add_argument('--light_energy', type=float, default=4.5, 
    help='intensity of lamp')
parser.add_argument('--array_path', default='arrays/example.npy',
    help='path to np array with render info')
parser.add_argument('--include', default='', 
    help='path with python3 scipy if not included in blender python')
parser.add_argument('--start', type=int, default=0, 
    help='first rendered index of array')
parser.add_argument('--end', type=int, default=10, 
    help='last rendered index of array')

cmd = sys.argv
args = parser.parse_args(cmd[cmd.index('--')+1:])

if type(args.light_pos) == str:
    args.light_pos = eval(args.light_pos)

print('\n', args)

sys.path.append(args.include)
import scipy.io, scipy.stats, numpy as np


sys.path.append('.')
from BlenderRender import BlenderRender
from IntrinsicRender import IntrinsicRender
from MorphableModel import MorphableModel

Blender = BlenderRender(light_pos=args.light_pos, light_energy=args.light_energy)
Intrinsic = IntrinsicRender(args.x_res, args.y_res)
Morphable = MorphableModel()

## load array with file info
render_array = np.load(args.array_path)

for [identity, filename, outpath, angles, position] in render_array[ args.start : args.end ]:

    ## update face shape and texture
    Morphable.update_face(identity, rot_x = angles[0], rot_y = angles[1])

    ## duplicate objects for intrinsics rendering
    Blender.duplicate('shape', 'shape_shading')
    Blender.duplicate('shape', 'shape_normals')
    
    ## move / rotate objects
    Blender.translate( ['shape', 'shape_shading', 'shape_normals'], position )
    Blender.rotate( ['shape', 'shape_shading', 'shape_normals'], [90, 0, 0] )

    ## render object and intrinsic images
    for mode in ['composite', 'albedo', 'depth', 'normals', 'shading']:
        Intrinsic.changeMode(mode)
        Blender.write(outpath, filename + '_' + mode, extension='png')

    ## delete duplicates
    Blender.delete(lambda x: x.name in ['shape_shading', 'shape_normals'] )



