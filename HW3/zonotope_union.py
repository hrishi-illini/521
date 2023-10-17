import z3
from z3 import Ints, Reals, Solver, ForAll, And, Implies, Exists, Real


# Vertices              (e1,e2)
# x11, y11 = 6, 2         # (1,1)
# x12, y12 = 2, 0         # (1,-1)
# x13, y13 = 4, 0         # (-1,1)
# x14, y14 = 0, -2        # (-1,-1)

# x21, y21 = 0, 2         # (1,1)
# x22, y22 = -2, 0         # (1,-1)
# x23, y23 = 4, 0         # (-1,1)
# x24, y24 = 2, -2        # (-1,-1)

# will simplify the list of vertices by removing convex combinations. A zonotope that contains two points also contains their convex combinations.
#  (4,0) and (-2,0) in a zonotope means (2,0) is as well. (6,2) & (2,-2) gives (4,0).
vertex_list = [(6,2), (0,-2), (0,2), (-2,0), (2,-2)]

# e1, e2, e3 = Reals('e1 e2 e3')

c0, c1, c2, c3 = Reals('c0 c1 c2 c3')
d0, d1, d2, d3 = Reals('d0 d1 d2 d3')

e_list = []
for i in range(1,6):
    e_list.append(  (  Real('e1'+str(i)), Real('e2'+str(i)), Real('e3'+str(i)) )  )

# we just want a c,d that satisfies the constraint
s = Solver()

for i, (x,y) in enumerate(vertex_list):
    e1, e2, e3 = e_list[i]
    s.add(And(e1>=-1, e2>=-1, e3>=-1, e1<=1, e2<=1, e3<=1, 
                            (c0 + c1*e1 + c2*e2 + c3*e3) == x, (d0 + d1*e1 + d2*e2 + d3*e3) == y))
print('checking')
s.check()
print(s.model())

# A model upon running was : d = (2,1/2,-7,8), c = (6,-1/2,-1/4,12)