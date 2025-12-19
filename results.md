Test Case 1 Result

csv file: test_case1.csv

length of river domain (m): 20

change in space (m): 0.2

simulation time (s): 300

change in time (s): 10

velocity (ms^-1): 0.1

Data read successfully.

Original Distance points: 21

Data interpolated successfully.

<img width="563" height="358" alt="截屏2025-12-19 02 42 29" src="https://github.com/user-attachments/assets/9993a3f1-36b4-435a-8e33-a3efb4b3dd28" />

*** WARNING: CFL condition (U*dt/dx <= 1) violated (CFL=5.00). Changing dt from 10.00s to 1.80s ***

<img width="569" height="436" alt="截屏2025-12-19 02 43 07" src="https://github.com/user-attachments/assets/9b699c56-28a0-4ded-a6be-08abc8d55e05" />

<img width="576" height="447" alt="截屏2025-12-19 02 43 21" src="https://github.com/user-attachments/assets/4c99148b-0cd6-43f3-89ce-89ae16651c25" />

<img width="576" height="446" alt="截屏2025-12-19 02 43 36" src="https://github.com/user-attachments/assets/26cbab7f-a6c9-4c29-b183-425b11bb7894" />

Test Cases 2 Result

csv file: initial_conditions.csv

length of river domain (m): 20

change in space (m): 0.2

simulation time (s): 300

change in time (s): 10

velocity (ms^-1): 0.1

Data read successfully.

Original Distance points: 21

Data interpolated successfully.

<img width="571" height="355" alt="截屏2025-12-19 02 45 17" src="https://github.com/user-attachments/assets/33f6459e-a5d5-4bd2-9cb3-2ea91aa753fa" />

*** WARNING: CFL condition (U*dt/dx <= 1) violated (CFL=5.00). Changing dt from 10.00s to 1.80s ***

<img width="569" height="425" alt="截屏2025-12-19 02 45 41" src="https://github.com/user-attachments/assets/2e9b4e92-7dab-415a-9e90-a94189c71264" />

<img width="574" height="442" alt="截屏2025-12-19 02 45 54" src="https://github.com/user-attachments/assets/b5bad6d7-6f25-4bdf-a19a-5635bc64b18b" />

<img width="563" height="447" alt="截屏2025-12-19 02 46 07" src="https://github.com/user-attachments/assets/a42a426a-9595-4f0e-8898-7ed6dd6c6023" />

# Result from case 2: Can read in any initial conditions provided and to interpolate them onto the model grid. 

Test Case 3 Result (Use the same data as test 2 and change the Values of U, spatial and temporal resolution srespectively)

# Result for test 3
For U, it had the largest influence on pollution transport, 
Spatial resolution (dx) affact the grids, finer grids reduced oscillations, and vice versa
Temporal resolution (dt) will affect CFL, if it was too large, the modle will be instability. 

test 4, change the value of 'k' in function advect














