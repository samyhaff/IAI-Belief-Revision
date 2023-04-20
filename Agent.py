from sympy import *
from sympy.logic.boolalg import to_int_repr

class Agent:
    def __init__(self):
        self.knowledge_base = set()

    def tell(self, sentence):
        self.knowledge_base.add(sentence)

    def ask(self, query):
        return self.resolution(query)

    def resolve(self, clause1, clause2):
        resolvents = set()
        for literal1 in clause1:
            for literal2 in clause2:
                if literal1 == -literal2:
                    new_clause = clause1.union(clause2) - {literal1, literal2}
                    resolvents.add(frozenset(new_clause))
        return resolvents

    def resolution(self, query):
        cnf = to_cnf(And(*self.knowledge_base, Not(query)))
        clauses = to_int_repr(cnf.args, cnf.free_symbols)
        while True:
            new_clauses = set()
            n = len(clauses)
            for i in range(n):
                for j in range(i + 1, n):
                    resolvents = self.resolve(clauses[i], clauses[j])
                    new_clauses |= resolvents
                    if set() in new_clauses:
                        return True
            if not new_clauses:
                return False
            for clause in new_clauses:
                if clause not in clauses:
                    clauses.append(clause)

agent = Agent()
A, B, C = symbols('A B C')
agent.tell(And(A, B))
agent.tell(Or(A, B))
print(agent.ask(A))
print(agent.ask(B))
print(agent.ask(C))
