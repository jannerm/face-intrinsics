import numpy as np

num_examples = 1
vetter_length = 400
save_path = 'arrays/example.npy'

array = []
for ind in range(num_examples):
    # latents = np.random.randn(vetter_length).tolist()
    latents = [1 for i in range(vetter_length/2)] + [0 for i in range(vetter_length/2)]
    filename = str(ind)
    outpath = 'output/example/'
    angles = [30., 0., 0.] ## [rot_x, rot_y, rot_z]
    position = [0., 0., 0.4] ## [x, y, z]
    
    info = [latents, filename, outpath, angles, position]
    array.append(info)

np.save(save_path, array)
