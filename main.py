from sympy import symbols
from sympy.logic.boolalg import to_cnf, Not, And, to_int_repr
from belief_base import *
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
    bb.tell(formula1, priority=1)
    bb.tell(formula2, priority=2)
    bb.tell(formula3, priority=3)

    # Print the initial knowledge base and priorities
    print(f"Initial knowledge base: {bb.knowledge_base}")
    print(f"Initial priorities: {bb.priority}")

    # Contract the belief base by removing formula2
    bb.contract(formula2)

    # Print the knowledge base and priorities after contracting formula2
    print(f"Knowledge base after contracting formula2: {bb.knowledge_base}")
    print(f"Priorities after contracting formula2: {bb.priority}")

    # DEBUG print the knowledge base
    # print(f"DEBUG: Knowledge base: {bb.knowledge_base}")

    # Define a formula to check if it is a logical consequence of the knowledge base
    phi = to_cnf(A & B)

    # Perform the resolution and print the result
    result = bb.resolution(phi)
    print(f"The formula '{phi}' is a logical consequence of the knowledge base: {result}")

if __name__ == "__main__":
    main()
