from sympy import symbols, And, Or, Not
from sympy.logic.boolalg import to_int_repr, to_cnf, to_dnf


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
        clauses = set([frozenset(x) for x in clauses])
        new_clauses = set()
        while True:
            for clause1 in clauses:
                for clause2 in clauses:
                    resolvents = self.resolve(clause1, clause2)
                    if set() in resolvents:
                        return True
                    new_clauses |= resolvents
            if new_clauses.issubset(clauses):
                return False
            clauses |= new_clauses

    def entailment(self, proposition, query):
        agent = Agent()
        agent.tell(proposition)
        return agent.ask(query)

    def partial_meet_contraction(self, query):
        new_knowledge_base = set()
        for proposition in self.knowledge_base:
            if not self.entailment(proposition, query):
                new_knowledge_base.add(proposition)
        self.knowledge_base = new_knowledge_base

# tests
agent = Agent()
A, B, C = symbols('A B C')
agent.tell(And(A, B))
agent.tell(Or(A, B))
print(agent.ask(B))
print(agent.ask(C))
agent.partial_meet_contraction(B)
print(agent.knowledge_base)