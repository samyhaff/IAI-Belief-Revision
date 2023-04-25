from sympy import symbols, And, Or, Not
from sympy.logic.boolalg import to_int_repr, to_cnf
from itertools import chain, combinations


class Agent:
    def __init__(self):
        self.knowledge_base = set()

    def tell(self, sentence):
        #print('Adding', sentence, 'as', to_cnf(sentence))
        #self.knowledge_base.add(to_cnf(sentence))
        print('Adding', sentence)
        self.knowledge_base.add(sentence)
        print('New knowledge base:', self.knowledge_base)

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

    def resolution(self, query, knowledge_base=None):
        if knowledge_base is None:
            cnf = to_cnf(And(*self.knowledge_base, Not(query)))
        else:
            cnf = to_cnf(And(*knowledge_base, Not(query)))
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

    def entailment(self, knowledge_base, query):
        return self.resolution(query=query, knowledge_base=knowledge_base)

    def remainders(self, set_a, phi):
        set_a = to_cnf(And(*set_a))
        #set_a_list = to_int_repr(set_a.args, set_a.free_symbols)
        set_a_list = set_a.args
        set_a_subsets = list(chain.from_iterable(combinations(set_a_list, r) for r in range(1, len(set_a_list))))
        set_a_subsets.sort(key=len, reverse=True)

        remainders = list()
        for set_a_subset in set_a_subsets:
            set_a_subset = frozenset(set_a_subset)
            if not self.entailment(set_a_subset, phi) and not any([set_a_subset.issubset(r) for r in remainders]):
                remainders.append(set_a_subset)

        #for remainder in remainders:
        #    if not any([remainder.issubset(r) for r in remainders if r != remainder]):
        #        remainders.remove(remainder)

        return remainders


    def partial_meet_contraction(self, query):
        print('Contracting', self.knowledge_base, 'with', query)
        remainders = self.remainders(set_a=self.knowledge_base, phi=query)
        self.knowledge_base = set.intersection(*[set(fs) for fs in remainders])
        print('New knowledge base:', self.knowledge_base)

    def partial_meet_contraction_samy(self, query):
        print('SAMYs METHOD: Contracting', self.knowledge_base, 'with', query)
        new_knowledge_base = set()
        clauses = to_cnf(And(*self.knowledge_base)).args
        for clause in clauses:
            clause_set = set()
            clause_set.add(clause)
            if not self.entailment(clause_set, query):
                new_knowledge_base.add(clause)
        self.knowledge_base = new_knowledge_base
        print('New knowledge base:', self.knowledge_base)

    def revision(self, query):
        self.partial_meet_contraction(Not(query))
        self.tell(query)


# tests
agent = Agent()
A, B, C = symbols('A B C')
agent.tell(And(A, B))
agent.tell(Or(A, B))
print('Does', agent.knowledge_base, 'entails', B, '?', agent.ask(B))
print('Does', agent.knowledge_base, 'entails', C, '?', agent.ask(C))
agent.partial_meet_contraction(B)


agent = Agent()
A, B, C = symbols('A B C')
agent.tell(And(A, B))
agent.tell(Or(A, B))
agent.partial_meet_contraction_samy(B)
# print(agent.knowledge_base)
