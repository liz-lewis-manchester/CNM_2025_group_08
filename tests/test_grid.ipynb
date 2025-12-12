import numpy as np
import pytest
from src.grid import create_grid,cfl_number,is_cfl_stable 

def test_create_grid():
    x,t=create_grid(L=20,dx=0.2,T=300,dt=10) 

    assert x[0]==0
    assert x[-1]==20
    assert t[0]==0
    assert t[-1]==300

def test_cfl_number():
    cfl=cfl_number(U=0.1,dx=0.2,dt=10)
    assert cfl==5

def test_cfl_stability_false():
    assert not is_cfl_stable(U=0.1,dx=0.2,dt=10)

def test_cfl_stability_true():
    assert is_cfl_stable(U=0.01,dx=0.2,dt=10)

def test_invalid_grid_parameters():
    with pytest.raises(ValueError):
        create_grid(L=-1,dx=0.1,T=10,dt=1) 

#This file is used to test the boundary conditions set within the src file
#Cfl number is (U*Δt/Δx) and for stability has to be less than or equal to 1
