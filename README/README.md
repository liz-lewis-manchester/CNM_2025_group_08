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

  1. plot_data: Compares the orginal CSV raw data with
    
     interpolated data

  2. plot_initial: generate a initial pollution distribution
    
     inthe whole model

  3. plot_snapshots: Shows concentration's changing at three time
    
     points (start, mid, end)

  4. plot_heatmap: Generates a space-time heatmap, to show the
    
     changing of pollutant over the whole simulation period.
​	
  # main.py

  1. Let user to input all parameters such that CSV file path,
 
     river length, spatial resolution, temporal resolution,

     velocity

  2. the vaild atat type should be float

  3. imoprt the function from the other two files and use them

     to run the whole logic of the modeling.

 # How to run the code
 
 1. open the scr file

 2. then open the model.py, copy all the code in this file to a python system

 3. then open the poltting.py file, don not copy import..from... if you want to combaine

    model.py and poltting.py together.

 4. open the main.py file, don not copy import..from... if you want to combaine

    model.py , poltting.py and main.py together.
   
 5. input the suitable parameters, please sure that the unit of all parameters suitable
    length of river domain (m)

    change in space (m):

    simulation time (s):

    change in time (s):

    velocity (ms^-1): and csv file has a suitable structure.
    

    
















