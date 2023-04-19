from sympy import symbols
from sympy.logic.boolalg import to_cnf, Not, And, to_int_repr
from beliefBase import *
import numpy as np

def main():
    # Define propositional symbols
    A, B, C = symbols('A B C')

    # Define example formulas
    formula1 = to_cnf((A | B) & (~A | ~B))
    formula2 = to_cnf(C | ~A)
    formula3 = to_cnf(~C | B)

    # Create a BeliefBase instance and add the example formulas to the knowledge base
    bb = BeliefBase()
    bb.tell(formula1)
    bb.tell(formula2)
    bb.tell(formula3)

    # DEBUG print the knowledge base
    # print(f"Knowledge base: {bb.knowledge_base}")

    # Define a formula to check if it is a logical consequence of the knowledge base
    phi = to_cnf(A & B)

    # Perform the resolution and print the result
    result = bb.resolution(phi)
    print(f"The formula '{phi}' is a logical consequence of the knowledge base: {result}")

if __name__ == "__main__":
    main()
