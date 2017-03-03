#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

# This code is based on 3dWorld.py from the Book TBA

from math import sin, cos, radians
import sys
sys.path.insert(1,'/home/patrick/raspberry_pi/pi3d')
import pi3d


def limit(value, inMin, inMax):
    if value < inMin:
        value = inMin
    elif value > inMax:
        value = inMax
    
    return value


def world3dA(inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap):
    from PIL import Image
    import numpy as np
    DISPLAY = pi3d.Display.create(x=50, y=50, far=5000, near=0.5)

    CAMERA = pi3d.Camera.instance()
    base_tex = np.array(Image.open(inTextureMap))
    # texture for land
    base_gr = base_tex.copy()
    ix = np.where(base_gr[:,:,2] > 20) # i.e. was blue
    base_gr[ix[0], ix[1], 1] += 50 # increase green
    base_gr[ix[0], ix[1], 2] = 0  # reduce blue
    texg = pi3d.Texture(base_gr)
    # texture for water
    base_bl = base_tex.copy()
    base_bl[:,:] = [0, 0, 60, 170] # uniform slightly transparrent
    texb = pi3d.Texture(base_bl)
    grass_tex = pi3d.Texture('/home/patrick/raspberry_pi/pi3d_demos/textures/grasstile_n.jpg')
    w_norm = pi3d.Texture('/home/patrick/raspberry_pi/pi3d_demos/textures/water/n_norm000.png')


    shader = pi3d.Shader("uv_bump")
    rshader = pi3d.Shader("uv_reflect")
    mapwidth = inWidth
    mapdepth = inDepth
    mapheight = inHeight
    
    mymap = pi3d.ElevationMap(inHeightmap, width=mapwidth, depth=mapdepth, height=mapheight, divx=199, divy=199, ntiles=1, name="sub", y=-0.0)
    mymap.set_draw_details(shader, [texg, grass_tex], 200.0)
    wmap = pi3d.ElevationMap(inHeightmap, width=mapwidth, depth=mapdepth, height=mapheight * 0.1, divx=40, divy=40, ntiles=1, name="water", y=25.0)
    wmap.set_draw_details(rshader, [texb, w_norm, texg], 500.0, 0.2)
    rot = 0.0
    tilt = 0.0
    height = 20.0
    viewHeight = 1.5
    sky = 2000
    xm, ym, zm = 0.0, height, 0.0
    onGround = False
 
    mykeys = pi3d.Keyboard()
    mymouse = pi3d.Mouse(restrict=False)
    mymouse.start()
    
    omx, omy = mymouse.position()
    fr = 0
    while DISPLAY.loop_running():
        mx, my = mymouse.position()

        rot -= (mx - omx) * 0.2
        tilt -= (my - omy) * 0.2

        omx = mx
        omy = my

        CAMERA.reset()
        CAMERA.rotate(-tilt, rot, 0)
        CAMERA.position((xm, ym, zm))

        mymap.draw()
        wmap.draw()

        k = mykeys.read()

        if k > -1:
            if k == 48:  # ESCAPE key - '0' Key
                DISPLAY.destroy()
                mykeys.close()
                mymouse.stop()
                break
            elif k == 87 or k == 119:
                #        if inputs.key_state("KEY_W"):
                xm -= sin(radians(rot)) * 2.0
                zm += cos(radians(rot)) * 2.0
            elif k == 83 or k == 115:
                #        elif inputs.key_state("KEY_S"):
                xm += sin(radians(rot)) * 2.0
                zm -= cos(radians(rot)) * 2.0
            elif k == 82 or k == 114:
                #        elif inputs.key_state("KEY_R"):
                ym += 4
                onGround = False
            elif k == 84 or k == 116:
                #        elif inputs.key_state("KEY_T"):
                ym -= 4
        
        ym -= 0.2
        
        xm = limit(xm, -(mapwidth / 2), (mapwidth / 2))
        zm = limit(zm, -(mapdepth / 2), (mapdepth / 2))
        
        if ym >= sky:
            ym = sky
        
        ground = max(mymap.calcHeight(xm, zm), wmap.calcHeight(xm, zm)) + viewHeight
        
        if (onGround is True) or (ym <= ground):
            ym = ground
            onGround = True

        pi3d.screenshot("/home/patrick/Downloads/Untitled Folder/scr_caps/world{:04d}.jpg".format(fr))
        fr += 1

if __name__ == '__main__':
  world3dA('Maps (copy)/seed_11111_grayscale.png', 
           10000, 10000, 1.5, 
           'Maps (copy)/seed_11111_elevation.png', 
           'Maps (copy)/seed_11111_normal.png')
