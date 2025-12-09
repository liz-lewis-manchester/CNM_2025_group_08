import numpy as np

def create_grid(L,dx,T,dt):

#this creates spatial and temporal grids 
#L=length of river domain (m)
#dx=change in space (m) 
#T=simulation time (s)
#dt=change in time (s) 

if L<=0 or dx<=0 or dt<=0 or T<0 
    raise ValueError('Invalid grid parameters') 

nx=int(L/dx)+1
nt=int(T/dt)+1

x=np.linspace(0,L,nx)
t=np.linspace(0,T,nt)

return x,t 

def cfl_number(U,dx,dt)

#this computes cfl number 

if dx<=0 or dt<=0:
    raise ValueError('dx and dt must be positive')
    
