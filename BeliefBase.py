from sympy import symbols
from sympy.logic.boolalg import to_cnf, Not, And, Or
from sympy.logic.inference import literal_symbol

class BeliefBase:
    def __init__(self):
        # Initialize the knowledge base as an empty set
        self.knowledge_base = set()

    def resolve(self, clause1, clause2):
        # Initialize a set to store the new clauses resulting from the resolution
        resolved = set()
        
        # Iterate through each pair of literals from the input clauses
        for literal1 in clause1:
            for literal2 in clause2:
                # If the literals are complementary (e.g., A and ~A)
                if literal1 == ~literal2:
                    # Create a new clause by combining the input clauses without the resolved literals
                    new_clause = (clause1 - {literal1}) | (clause2 - {literal2})
                    
                    # If the new clause is empty, return None (indicating an empty clause was derived)
                    if not new_clause:
                        return None
                    
                    # Add the new clause (in frozenset form) to the set of resolved clauses
                    resolved.add(frozenset(new_clause))
                    
        # Return the set of new clauses resulting from the resolution
        return resolved

    def resolution(self, phi):
        # Convert the knowledge base and the negation of the input formula phi to CNF
        knowledge_base_cnf = to_cnf(And(*self.knowledge_base, Not(phi)))

        # DEBUG Print the knowledge base and the negation of the input formula phi in CNF
        print(f"DEBUG: Knowledge base in CNF: {knowledge_base_cnf}")

        # DEBUG Print knowledge base arguments
        # print(f"DEBUG: Knowledge base arguments: {knowledge_base_cnf.args}")
        
        # Initialize the set of clauses with the CNF arguments
        clauses = set(knowledge_base_cnf.args)

        # DEBUG Print the clauses
        # print(f"DEBUG: Clauses: {clauses}")

        # Convert the Or objects to sets of their arguments (using frozenset for immutability)
        clauses = {frozenset(clause.args) for clause in clauses}

        # Main resolution loop
        while True:
            # Initialize a set to store the new clauses generated during the resolution process
            new_clauses = set()
            
            # Iterate through each pair of clauses
            for clause1 in clauses:
                for clause2 in clauses:
                    if clause1 != clause2:
                        # Resolve the pair of clauses
                        resolved = self.resolve(clause1, clause2)
                        
                        # If the resolution derived an empty clause, return True
                        if resolved is None:

                            # DEBUG print the empty clause
                            print(f"DEBUG: Empty clause derived from {clause1} and {clause2}")

                            return True
                        
                        # Add the new clauses resulting from the resolution to the set of new clauses
                        new_clauses |= resolved

            # If no new clauses were generated or the new clauses are a subset of the existing clauses, break the loop
            if not new_clauses or new_clauses.issubset(clauses):
                break

            # Add the new clauses to the set of clauses
            clauses |= new_clauses

        # If the loop terminated without deriving an empty clause, return False
        return False

    def ask(self, fact):
        # Check if a fact is in the knowledge base and return True or False accordingly
        return fact in self.knowledge_base

    def tell(self, fact):
        # Add a fact to the knowledge base and return the updated knowledge base
        self.knowledge_base.add(fact)
        return self.knowledge_base
