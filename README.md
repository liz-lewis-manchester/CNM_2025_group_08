# CNM_2025_group_08
import numpy as np
import panda as pd
def test_case_2(csv_file):
  # if the csv exist
  assert pd.read_csv("initial_conditions.csv"), “csv {'initial_conditions.csv'} is not exist"

  # if the function can read csv file
  assert final_function("initial_conditions.csv"), "the function can not read csv file"
  df = pd.read_csv("initial_conditions.csv")
  x = df["Distance (m)"]
  theta = df["Concentration (�g/m_ )"]
  
  
