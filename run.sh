## point to your blender app
BLENDER=/Applications/Blender/blender.app/Contents/MacOS/blender
## if necessary, point to python3 scipy 
PACKAGES=/Users/Janner/anaconda2/envs/blender/lib/python3.4/site-packages/

${BLENDER} --background -noaudio --python render.py -- --start 0 --end 10 --light_pos [-4,-10,3] --light_energy 5 --include ${PACKAGES}