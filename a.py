from z3 import *

X = [[[Bool("X[{k}][{i}][{j}]".format(i=i, j=j, k=k)) for k in range(4)] for i in range(4)] for j in range(4)]

X[1][1][0] = False
clause = Or(X[2][1][0], X[1][1][0], X[1][0][0])

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

solve(clause)