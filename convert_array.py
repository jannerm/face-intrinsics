import math, numpy as np, scipy.io as io, pdb

def rad_to_deg(radians):
    return [rad * 180. / math.pi for rad in radians]

# num_examples = 1
vetter_length = 400
load_path = 'vetter/array.mat'
save_path = 'arrays/example.npy'

mat = io.loadmat(load_path)
latents = mat['latents']
angles = mat['angles']

array = []
num_examples = latents.shape[0]
for ind in range(num_examples):
    lat = latents[ind,:].tolist()
    filename = str(ind)
    outpath = 'output/matching/'
    degrees = rad_to_deg(angles[ind])
    ang = [degrees[0], degrees[1], 0.] ## [rot_x, rot_y, rot_z]
    position = [0., 0., 0.4] ## [x, y, z]
    
    info = [lat, filename, outpath, ang, position]
    array.append(info)

# pdb.set_trace()
np.save(save_path, array)
