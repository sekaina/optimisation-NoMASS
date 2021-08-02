'''
import datetime
from datetime import date
import time
s=str(datetime.datetime.now())
s_replace_point=s.replace(".","")
s_replace=s_replace_point.replace(":","")[:17]

with open("./results/data" +s_replace+ ".txt", "w") as front:
    print("ok")

def init_file():
    with open("monitoring.csv", "r") as data:
        content = data.read()
    content = content.split("\n")
    monit = []
    line = []

    from ast import literal_eval
    for row in content[1:-1]:
        line = []
        row = literal_eval(row)
        line.append(literal_eval(row[1]))
        line.append(literal_eval(row[2]))
        monit.append(line)
init_file()'''
import pandas as pd
data={
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
print (data)
monit=pd.DataFrame(data)
with open ("test.csv", 'a') as f:
    monit.to_csv(f, header=False, line_terminator="")
import numpy as np
L=np.array([[1,2],[3,4]])
print(L)
print(L[:,0])
# Bounds walls
LOW_WALLS, UP_WALLS = 0, 40
# Bounds windows
LOW_WINDOW, UP_WINDOW = 0, 4
BOUNDS = [(LOW_WALLS, UP_WALLS), (LOW_WALLS, UP_WALLS),
          (LOW_WALLS, UP_WALLS), (LOW_WINDOW, UP_WINDOW)]
print(BOUNDS)
genome = list()
ranges=BOUNDS
if genome == list():
    print(ranges)
    nparam = len(ranges)
    for p in ranges[0:nparam]:
        genome.append(np.random.randint(*p))
print(genome)
print(str(genome[0])+str(genome[1]))
import random
x=random.randrange(0,10,1)
print (x)