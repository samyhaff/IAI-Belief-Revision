from sympy import symbols
from sympy.logic.boolalg import to_cnf, Not, And, to_int_repr
from test import *

A, B, C, D = symbols('A B C D')

formula1 = to_cnf(~(A | B) | D)
formula2 = to_cnf(~(A | C) | B | ~D)
formula3 = to_cnf(~(A | ~C) | B | ~ (D | ~A))

kb = And(formula2, formula3)
not_phi = to_cnf(Not(formula1))

bb = BeliefBase()


bb.tell(formula2)
bb.tell(formula3)
bb.resolution(kb, phi=formula1, symbols=[A, B, C, D])