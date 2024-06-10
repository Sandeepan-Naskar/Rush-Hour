import sys
from z3 import *

s = Solver()

def solve(formula):
    s = Solver()
    s.add(formula)
    r = s.check()
    if(r==sat):
        print("sat")
        m = s.model()
        print(m)
    else:
        print("unsat")

file = list(map(str.strip, open(sys.argv[1], "r").readlines()))

info = []
with open(sys.argv[1]) as f:
	for line in f:
		info.append([int(v) for v in line.strip().split(',')])

n = info[0][0]
limit = info[0][1]
red_car = info[1]

cars = []
mines = []
car_vars = []

dict = {"orient":0 , "row": 0, "col": 0, "var": 0,"id":  0}

for lines in file[2:]:
    if lines.split(',')[0] != '2':
        k = len(cars)
        cars.append(list(map(int, lines.split(','))))
        car_vars.append({"orient":cars[k][0] , "row": cars[k][1], "col": cars[k][2], "id":  k})
        car_vars[-1]["vars"]=  [Int(f'{t}_{car_vars[-1]["orient"]}_{car_vars[-1]["id"]}_{car_vars[-1]["row"]}_{car_vars[-1]["col"]}') for t in range(limit + 1)]
        
        for i in range(limit + 1):
            s.add(car_vars[-1]["vars"][i] >= 0, car_vars[-1]["vars"][i] <= n - 2)
        for i in range(limit):
            s.add(car_vars[-1]["vars"][i + 1] - car_vars[-1]["vars"][i] <= 1)
            s.add(car_vars[-1]["vars"][i] - car_vars[-1]["vars"][i + 1] <= 1)

        if car_vars[-1]["orient"] == 2:
            s.add(Or([car_vars[-1]["vars"][i] == n-2 for i in range(limit + 1)]))

        if car_vars[-1]["orient"] == 0:
            s.add(car_vars[-1]["vars"][0] == car_vars[-1]["row"])
        else:
            s.add(car_vars[-1]["vars"][0] == car_vars[-1]["col"])
    else:
        mines.append(list(map(int, lines.split(',')))[1:])

car_vars.append({"orient":2 , "row": red_car[0], "col": red_car[1], "id":  'R'})
car_vars[-1]["vars"]=  [Int(f'{t}_{car_vars[-1]["orient"]}_{car_vars[-1]["id"]}_{car_vars[-1]["row"]}_{car_vars[-1]["col"]}') for t in range(limit + 1)]
for i in range(limit + 1):
    s.add(car_vars[-1]["vars"][i] >= 0, car_vars[-1]["vars"][i] <= n - 2)
for i in range(limit):
    s.add(car_vars[-1]["vars"][i + 1] - car_vars[-1]["vars"][i] <= 1)
    s.add(car_vars[-1]["vars"][i] - car_vars[-1]["vars"][i + 1] <= 1)

if car_vars[-1]["orient"] == 2:
    s.add(Or([car_vars[-1]["vars"][i] == n-2 for i in range(limit + 1)]))

if car_vars[-1]["orient"] == 0:
    s.add(car_vars[-1]["vars"][0] == car_vars[-1]["row"])
else:
    s.add(car_vars[-1]["vars"][0] == car_vars[-1]["col"])
        

for mine in mines:
    for car in car_vars:
        if car["orient"] == 0 and car["col"] == mine[1]:
            [s.add(Not(Or(car["vars"][i] == mine[0], car["vars"][i] + 1 == mine[0]))) for i in range(limit + 1)]
        elif (car["orient"] == 1 or car["orient"] == 2) and car["row"] == mine[0]:
            [s.add(Not(Or(car["vars"][i] == mine[1], car["vars"][i] + 1 == mine[1]))) for i in range(limit + 1)]

for a in range(0, len(car_vars)):
    for b in range(a + 1, len(car_vars)):
        car = []
        car.append(car_vars[a])
        car.append(car_vars[b])
        if car[0] == car[1]:
            continue
        if car[0]["orient"] != 0 and car[1]["orient"] != 0:
            if car[0]["row"] == car[1]["row"]:
                for t in range(limit + 1):
                    if car[0]["col"] < car[1]["col"]:
                        s.add(car[1]["vars"][t] - car[0]["vars"][t] > 1)
                    else:
                        s.add(car[1]["vars"][t] - car[0]["vars"][t] < -1)
        if car[0]["orient"] == 0 and car[1]["orient"] == 0:
            if car[0]["col"] == car[1]["col"]:
                for t in range(limit + 1):
                    if car[0]["row"] < car[1]["row"]:
                        s.add(car[1]["vars"][t] - car[0]["vars"][t] > 1)
                    else:
                        s.add(car[1]["vars"][t] - car[0]["vars"][t] < -1)

        if car[0]["orient"] != 0 and car[1]["orient"] == 0:
            for t in range(limit + 1):
                i = []
                i.append(car[0]["row"])
                i.append(car[0]["vars"][t])

                j = []
                j.append(car[1]["vars"][t])
                j.append(car[1]["col"])
                
                s.add(Not(Or(
                    And(i[0] - j[0] == 0,  j[1] - i[1] == 0),
                    And(i[0] - j[0] == 0,  j[1] - i[1] == 1),
                    And(i[0] - j[0] == 1,  j[1] - i[1] == 0),
                    And(i[0] - j[0] == 1,  j[1] - i[1] == 1)
                )))
        if car[0]["orient"] == 0 and car[1]["orient"] != 0:
            for t in range(limit + 1):
                i = []
                i.append(car[0]["vars"][t])
                i.append(car[0]["col"])

                j = []
                j.append(car[1]["row"])
                j.append(car[1]["vars"][t])
                
                s.add(Not(Or(
                    And(i[0] - j[0] == 0, j[1] - i[1] == 0),
                    And(i[0] - j[0] == 0, j[1] - i[1] == -1),
                    And(i[0] - j[0] == -1, j[1] - i[1] == 0),
                    And(i[0] - j[0] == -1, j[1] - i[1] == -1)
                )))

for time in range(limit):
    predicates = []
    for car in car_vars:
        predicates.append((car["vars"][time+1] - car["vars"][time] == 1, 1))
        predicates.append((car["vars"][time] - car["vars"][time+1] == 1, 1))
    s.add(PbEq(predicates, 1))

if s.check() == unsat:
    print("unsat")
else:
    transitions = [[] for t in range(limit + 1)]
    end = 0
    for i in s.model():
        k = int(str(i).split('_')[0])
        transitions[k].append(f"{'_'.join(str(i).split('_')[1:])}_{s.model()[i]}")

    for i in range(len(transitions)):
        for kk in transitions[i]:
            if str(kk).startswith('2') and str(kk).endswith(str(n - 2)):
                end = i
                break
        if end != 0:
            break

    for t in range(end):
        x, y = 0, 0
        for i in transitions[t]:
            if i not in transitions[t + 1]:
                if i.split('_')[0] != '0':
                    x = i.split('_')[2]
                    y = i.split('_')[4]
                else:
                    x = i.split('_')[4]
                    y = i.split('_')[3]
        for i in transitions[t + 1]:
            if i not in transitions[t]:
                if i.split('_')[0] != '0':
                    y = max(int(y), int(i.split('_')[4]))
                else:
                    x = max(int(x), int(i.split('_')[4]))
        print(f'{x},{y}')
