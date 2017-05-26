## point to your blender app
BLENDER=/om/user/janner/blender-2.76b-linux-glibc211-x86_64/blender 
## if necessary, point to python3 scipy 
PACKAGES=/om/user/janner/anaconda/lib/python3.4/site-packages/

${BLENDER} --background -noaudio --python render.py -- --start 0 --end 10 --light_pos [-4,-10,3] --light_energy 5 --include ${PACKAGES}