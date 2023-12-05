from z3 import Solver
from z3 import Int, Not, And, Implies





x = Int('x')
y = Int('y')
z = Int('z')
i = Int('i')


# The following isn't exactly Houdini, but I will just take individual constraints we want to check for and see if they hold at the beginning of the loop

s = Solver()        # solver instance
s.add(x == 1, y == 2, z == 3, i == 0)


constraints = [ Not(x == y), i == 0, i > 10, i < 10, i <= 10]
new_constraints = []
for constraint in constraints:
    if str(s.check(Not(constraint))) == 'unsat': # The constraint holds in the program state before the loop
        new_constraints.append(constraint)

constraints = new_constraints   # constraints now stores the constraints that 

# the remaining constraints are Not(x == y), i == 0, i < 10, i <= 10

# Check if constraints are satisfied at the beginning of the loop. If so, check if they are satisfied after the loop
# If they are not. Get model. Get rid of the conficting constraints. Repeat until there is no 'bad' model.

# Skipping the individual transformations during the program. We'll define x1, y1, z1, i1 to be the values of x, y, z, i at the end of a loop iteration.
#
# while (i < 10) {               (x = a, y = b, z = c, i = k)
# tmp = x;
# x = y;
# y = z;
# z = tmp;
# i = i + 1;                     (x = b, y = c, z = a, i = k+1)
# }

x1 = Int('x1')
y1 = Int('y1')
z1 = Int('z1')
i1 = Int('i1')



is_cons = False
s = Solver()
# constraints -> 'invariant before loop'
assumes = [x1 == y, y1 == z, z1 == x, i1 == i + 1, i < 10]   # i < 10 to enter the loop body
constraints1 = [Not(x1 == y1), i1 == 0, i1 < 10, i1 <= 10]
while(is_cons == False):
    new_constraints = []
    new_constraints1 = []
    p = s.check( Not( Implies( And(*assumes, *constraints), And(*constraints1)) ) )
    if str(p) == 'unsat':     # none of the constraints are violated
        is_cons = True
    else:
        model = s.model()
        s1 = Solver()
        for var in model:
            s1.add(var() == model[var()])
        for c in range(len(constraints1)):
            if str(s1.check(Not(constraints1[c]))) == 'unsat':
                new_constraints.append(constraints[c])
                new_constraints1.append(constraints1[c])
        constraints = new_constraints
        constraints1 = new_constraints1

    
print(constraints)
# returns i<=10


# ------------------------------(PT 2) This part does Houdini with constraints Not (z == y), Not( x == z) as well. This shows x != y----
#------------------------------------- Uncomment the the following and comment the above. ----------------------------------------------

# x = Int('x')
# y = Int('y')
# z = Int('z')
# i = Int('i')

# s = Solver()        # solver instance
# s.add(x == 1, y == 2, z == 3, i == 0)


# constraints = [ Not(x == y), i == 0, i > 10, i < 10, i <= 10, Not(z == y), Not(x == z)]
# new_constraints = []
# for constraint in constraints:
#     if str(s.check(Not(constraint))) == 'unsat': # The constraint holds in the program state before the loop
#         new_constraints.append(constraint)

# constraints = new_constraints   # constraints now stores the constraints that 

# print(constraints)

# # while (i < 10) {               (x = a, y = b, z = c, i = k)
# # tmp = x;
# # x = y;
# # y = z;
# # z = tmp;
# # i = i + 1;                     (x = b, y = c, z = a, i = k+1)
# # }

# x1 = Int('x1')
# y1 = Int('y1')
# z1 = Int('z1')
# i1 = Int('i1')



# is_cons = False
# s = Solver()
# # constraints -> 'invariant before loop'
# assumes = [x1 == y, y1 == z, z1 == x, i1 == i + 1, i < 10]   # i < 10 to enter the loop body
# constraints1 = [Not(x1 == y1), i1 == 0, i1 < 10, i1 <= 10, Not(z1 == y1), Not(x1 == z1)]
# while(is_cons == False):
#     new_constraints = []
#     new_constraints1 = []
#     p = s.check( Not( Implies( And(*assumes, *constraints), And(*constraints1)) ) )
#     if str(p) == 'unsat':     # none of the constraints are violated
#         is_cons = True
#     else:
#         model = s.model()
#         s1 = Solver()
#         for var in model:
#             s1.add(var() == model[var()])
#         for c in range(len(constraints1)):
#             if str(s1.check(Not(constraints1[c]))) == 'unsat':
#                 new_constraints.append(constraints[c])
#                 new_constraints1.append(constraints1[c])
#         constraints = new_constraints
#         constraints1 = new_constraints1

    
# print(constraints)
# # This gives [Not(x == y), i <= 10, Not(z == y), Not(x == z)].