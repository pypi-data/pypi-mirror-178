import os
import pandas as pd
import time 
import random 


def pp(frame):
  inter = frame.copy()

  print(inter)
  print(inter.columns.tolist())


def unique_in_col(frame, col):
  inter = frame.copy()
  print(inter)
  print(inter.columns.tolist())
  print(inter[col].unique().tolist())


def null_in_col(frame, col):
  inter = frame.loc[frame[col].isna()].copy()
  print(inter)
  print(inter.columns.tolist())
  print(inter[col].unique().tolist())


def dumper(path, name, frame):
    with open(f'{path}/{name}.csv', 'w') as f:
        frame.to_csv(f, index=False, header=True)


def make_num(frame, col):
    copier = frame.copy()
    copier[col] = pd.to_numeric(copier[col])
    return copier


def combine_from_folder(pathos):

  listo = []

  fillos = os.listdir(pathos)
  fillos = [pathos + x for x in fillos if x != '.DS_Store']

  for fillo in fillos:
    inter = pd.read_csv(fillo)

    listo.append(inter)

  cat = pd.concat(listo)

  return cat


def print_headers(frame, num_row):
  copier = frame.copy()
  cols = copier.columns.tolist()
  for i in range(num_row, len(cols), num_row):
    first = i - num_row
    print(f"{str(cols[first:i])[1:-1]}")


def rand_delay(num):
  import random 
  import time 
  rando = random.random() * num
  print(rando)
  time.sleep(rando)





