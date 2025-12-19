This program modles the 1D advection equation to simulate pollutant concentration evolution in rivers

the main equation is  ∂t/∂θ	=−U*(∂x/∂θ), 
 θ is pollutant concentration (µg/m³)
 t is time(s)
 x is distance (m)
 U is stream velocity (m/s)

# Folder Structure

# 1.src

# modle.py 

1. read_boundary_conditions: it reads initial concentration from
  
   CSV,  if the file has a error structure it will read fail

2. interpolate_conditions: It Interpolates non-grid-aligned to

   fit grid.
   
3. create_grid: gererates grid model in time (dt) and distance

   (dx)

4. advect: solve equation by backword finite difference method.

   check if the CFL was suiutible (stability), if not, it will

   give a suitable CFL to make the modle follow the physic law. 

   And you can change exponential decay by change the value of k

   in this function, defult k=0.0 at first

   
  # plotting.py

  
​	
 

