from sympy import symbols
from sympy.logic.boolalg import to_cnf, Not, And, to_int_repr

class BeliefBase:
    def __init__(self):
        self.knowledge_base = set()

    def resolve(self, clauses):
        pass

    def resolution(self, phi):
        knowledge_base_cnf = to_cnf(And(*self.knowledge_base, Not(phi)))
        symbols = knowledge_base_cnf.free_symbols
        clauses = knowledge_base_cnf.args
        
        new = {}

        
        

    
        
    def ask(self, fact):
        return fact in self.knowledge_base

    def tell(self, fact):
        self.knowledge_base.add(fact)
        return self.knowledge_base
    
