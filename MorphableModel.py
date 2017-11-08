import os, math, numpy as np, scipy, bpy, pdb

class MorphableModel:

    '''
    loads reference face for modification 
    and morphable model principle components
    '''
    def __init__(self):
        bpy.ops.import_mesh.ply(filepath='ply/face_0.ply')
        obj = bpy.data.objects['face_0']
        mesh = bpy.data.meshes['face_0']
        obj.name = 'shape'
        mesh.name='mesh'

        ## some appropriate default values
        bpy.data.objects['shape'].scale[0] = 0.0000264
        bpy.data.objects['shape'].scale[1] = 0.0000264
        bpy.data.objects['shape'].scale[2] = 0.0000264
        bpy.data.objects['shape'].rotation_euler[0] = 90.*math.pi/180.0
        bpy.data.objects['shape'].rotation_euler[2] = 0.*math.pi/180.0
        bpy.data.objects['shape'].location[0] = 0
        bpy.data.objects['shape'].location[1] = 0
        bpy.data.objects['shape'].location[2] = 0

        ## smooth the faces
        bpy.ops.object.shade_smooth()

        # get face material
        mat = bpy.data.materials.get("face")
        if mat is None:
            mat = bpy.data.materials.new(name="face")

        ## so we can see the vertex colors
        mat.use_vertex_color_paint = True
        ## low specularity so face doesn't look plastic
        mat.specular_intensity = 0.05

        # assign material to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        ## orthographic camera for more realistic rendering
        bpy.data.cameras['Camera'].type='ORTHO'

        self.__load_model()

    '''
    latents : 400-length list of alpha and beta coefficients
    modifies blender face
    '''
    def update_face(self, latents, rot_x = 0, rot_y = 0):
        alpha = latents[:200]
        beta = latents[200:400]
        shape_mat = np.array(self.__coef_to_object(alpha, self.shapeMU, self.shapePC, self.shapeEV, self.segMM, self.segMB, 4))
        tex_mat = np.array(self.__coef_to_object(beta, self.texMU, self.texPC, self.texEV, self.segMM, self.segMB, 4))
        tex_mat = tex_mat.swapaxes(0, 1)
        tex_mat.shape = (53490, 3)
        vertices = self.__get_vertices(shape_mat)
        # pdb.set_trace()
        vertices = self.global_rotate(vertices, rot_x, rot_y)
        # vertices = self.reflect_z(vertices)
        colors = self.__get_colors(tex_mat, self.tl)
        self.__modify_mesh(vertices, colors)

    def __load_model(self, path = 'mat/'):
        shape = scipy.io.loadmat( os.path.join(path, 'shape.mat') )
        tex = scipy.io.loadmat( os.path.join(path, 'tex.mat') )
        seg = scipy.io.loadmat( os.path.join(path, 'seg.mat') )
        tl = scipy.io.loadmat( os.path.join(path, 'tl.mat') )
        self.shapeMU = shape['shapeMU']
        self.shapePC = shape['shapePC']
        self.shapeEV = shape['shapeEV']
        self.texMU = tex['texMU']
        self.texPC = tex['texPC']
        self.texEV = tex['texEV']
        self.segMM = seg['segMM']
        self.segMB = seg['segMB']
        self.tl = tl['new_tl']
        print('Morphable model loaded')

    '''
    modifies shape and colors of blender mesh
        shape : returned by get_vertices
        colors : returned by get_colors
    '''
    def __modify_mesh(self, shape, colors):
        mesh = bpy.data.meshes['mesh']
        cols = mesh.vertex_colors.active.data
        if shape is not None:
            for i in range(len(mesh.vertices)):
                mesh.vertices[i].co = shape[i]
        if colors is not None:
            for i in range(len(cols)):
                cols[i].color = colors[i]
        ## x = -x, to match matlab rendering
        bpy.ops.transform.mirror(constraint_axis=(True,False,False))
        mesh.update()

    '''
    transforms shape object into blender vertices
        obj : returned by coef_to_object
    '''
    def __get_vertices(self, obj):
        # vertices = []
        # count = 0
        # for i in range(53490):
        #     vertices.append((obj[count], obj[count+1], obj[count+2]))
        #     count += 3
        num_verts = int(obj.size / 3)
        vertices = obj.reshape(num_verts, 3)
        return vertices

    def global_rotate(self, vertices, x, y):
        if x != 0 or y != 0:
            rot_mat_x = self.__rotx(x)
            rot_mat_y = self.__roty(y)
            vertices = np.dot(rot_mat_x, np.dot(rot_mat_y, vertices.T)).T
        return vertices

    ## x = -x, to match matlab rendering
    # def reflect_z(self, vertices):
        # vertices[:,0] *= 1
        # bpy.ops.transform.mirror(constraint_axis=(True,False,False))
        # return vertices

    '''
    transforms texture object into blender colors
        obj : returned by coef_to_object
    '''
    def __get_colors(self, intTex, tl):
        colors = []
        tl = tl.swapaxes(0, 1)
        new_tl = tl.reshape(1, 3*106466)
        for i in new_tl[0]:
            colors.append([val/255. for val in intTex[i]])
        return colors

    '''
    transforms alpha / beta latents into shape / texture object
        coef : 200-length list
        coef, mu, pc, ev, mm, mb : loaded by load_model
    '''
    def __coef_to_object(self, coef, mu, pc, ev, mm, mb, dim):
        ## Reconstruction
        coef_array = [str(i) for i in coef]
        coef = np.transpose(np.reshape(coef, (4, 50)))
        ev = np.matrix(ev[0:199])
        pc = np.matrix(pc[:,0:199])
        ones = np.matrix(np.ones((1, dim)))
        obj = (np.matrix(mu) * ones) + (pc[:, :50] * (np.multiply(coef, ev[:50] * ones)))
        
        ## Blending
        n_seg = dim
        n_ver = int(len(obj[:, 0])/3)
        all_vertices = np.zeros((n_seg*n_ver, 3))
        k = 0
        for i in range(n_seg):
            all_vertices[k:k+n_ver, :] = np.reshape(obj[:, i], (n_ver, 3))
            k += n_ver
        obj = np.transpose(scipy.sparse.linalg.spsolve(mm, mb*all_vertices))
        obj = obj.swapaxes(0, 1)
        obj = np.matrix(np.reshape(obj, (160470, 1)))
        return obj

    def __deg_to_rad(self, deg):
        rad = math.pi * deg / 180.
        return rad

    def __rotx(self, deg):
        rad = self.__deg_to_rad(deg)
        R = np.array([  [1,             0,               0],
                        [0,             np.cos(rad),     -np.sin(rad)],
                        [0,             np.sin(rad),      np.cos(rad)]])
        return R

    def __roty(self, deg):
        rad = self.__deg_to_rad(deg)
        R = np.array([  [np.cos(rad),   0,      np.sin(rad)],
                        [0,             1,      0],
                        [-np.sin(rad),  0,      np.cos(rad)]])
        return R


