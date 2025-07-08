"""
this file contains utility functions to be used in combination with three axis stages
"""

import numpy as np
    
def get_zigzag_pattern(Nx,Ny,Nz,xmin,xmax,ymin,ymax,zmin,zmax):
    N=Nx*Ny*Nz
    deltax=(xmax-xmin)/(Nx-1)
    deltay=(ymax-ymin)/(Ny-1)
    deltaz=(zmax-zmin)/(Nz-1)

    #traverse the workspace in zigzag pattern and compute the points to be traversed
    dirxpos=True
    dirypos=True
    pos=np.array([xmin,ymin,zmin])
    dx=np.array([deltax,0,0])
    dy=np.array([0,deltay,0])
    dz=np.array([0,0,deltaz])

    positions=np.zeros((3,N))
    position_indices=np.zeros((3,N))
    def add_position(pos):
        positions[:,add_position.idx]=pos
        position_indices[:,add_position.idx]=np.array([(pos[0]-xmin)/deltax,(pos[1]-ymin)/deltay,(pos[2]-zmin)/deltaz])
        add_position.idx+=1
    add_position.idx=0

    for k in range(0,Nz):
        add_position(pos)
        for j in range(0,Ny):
            for i in range(0,Nx-1):
                #move in x direction
                if dirxpos:
                    pos=pos+dx
                else:
                    pos=pos-dx
                add_position(pos)
            #adjust the x direction
            dirxpos=not dirxpos
            if(j!=Ny-1):
                #move in y direction
                if dirypos:
                    pos=pos+dy
                else:
                    pos=pos-dy
                add_position(pos)
        #move in z direction
        pos=pos+dz
        #adust the y direction
        dirypos=not dirypos

    return (positions,position_indices)     