import sympy
from sympy import symbols, And, Or, Not
from sympy.logic.boolalg import to_int_repr, to_cnf
from itertools import combinations


class Agent:
    def __init__(self):
        self.knowledge_base = list()

    def get_clauses(self, expr):
        if not isinstance(expr, And):
            return expr,
        return set(expr.args)

    def tell(self, sentence):
        #print('Adding', sentence, 'as', to_cnf(sentence))
        #self.knowledge_base.add(to_cnf(sentence))
        print('Adding', sentence)
        self.knowledge_base.append(sentence)
        print('New knowledge base:', self.knowledge_base)

    def ask(self, query):
        return self.resolution(query)

    def resolve(self, clause1, clause2):
        resolvents = set()
        for literal1 in clause1:
            for literal2 in clause2:
                if literal1 == - literal2:
                    new_clause = clause1.union(clause2) - {literal1, literal2}
                    resolvents.add(frozenset(new_clause))
        return resolvents

    def resolution(self, query, knowledge_base=None):
        if knowledge_base is None:
            cnf = to_cnf(And(*self.knowledge_base, Not(query)))
        else:
            cnf = to_cnf(And(*knowledge_base, Not(query)))
        clauses = to_int_repr(cnf.args, cnf.free_symbols)
        if isinstance(cnf, Or):
            clauses = [set.union(*clauses)]
        #print('Clauses:', clauses)
        clauses = set([frozenset(x) for x in clauses])
        new_clauses = set()
        while True:
            for clause1 in clauses:
                for clause2 in clauses - {clause1}:
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
        #set_a = to_cnf(And(*set_a)) # change the order of the KB, so we are losing the temporal order of the formula
        #set_a_list = set_a.args
        set_a_list = set_a
        #remainders = set(copy.deepcopy(set_a_list))

        if not self.entailment(knowledge_base=set_a, query=phi):
            return set_a

        for i in range(1, len(set_a_list)):
            to_remove_formulas = [x[0] if len(x) == 1 else x for x in combinations(set_a_list, i)] #check if the order make sense (YES: it discard before the last added formulas/clause)
            for to_remove_formula in reversed(to_remove_formulas):
                for to_remove_clause in self.get_clauses(to_cnf(to_remove_formula)):
                    if isinstance(to_remove_clause, sympy.Tuple):
                        new_remainders = self.get_clauses(to_cnf(And(*set_a_list))) - set(to_remove_clause.args)
                    else:
                        new_remainders = self.get_clauses(to_cnf(And(*set_a_list))) - {to_remove_clause}
                    if not self.entailment(knowledge_base=new_remainders, query=phi):
                        return list(new_remainders)

        return list()

    def contraction(self, query):
        remainders = self.remainders(set_a=self.knowledge_base, phi=query)
        self.knowledge_base = remainders


    def partial_meet_contraction(self, query):
        print('Contracting', self.knowledge_base, 'with', query)
        remainders = self.remainders(set_a=self.knowledge_base, phi=query)
        if len(remainders) > 0:
            # self.knowledge_base = set.intersection(*[set(fs) for fs in remainders]) # doesn't always work
            self.knowledge_base = set(remainders[0]) # testing purposes


    def partial_meet_contraction_samy(self, query):
        new_knowledge_base = set()
        clauses = to_cnf(And(*self.knowledge_base)).args
        for clause in clauses:
            clause_set = set()
            clause_set.add(clause)
            if not self.entailment(clause_set, query):
                new_knowledge_base.add(clause)
        self.knowledge_base = new_knowledge_base


    def revision(self, query, contraction_function):
        print('Revising', self.knowledge_base, 'with', query)
        contraction_function(Not(query))
        print('New knowledge base after contraction:', self.knowledge_base)
        self.tell(query)
        print('Updated knowledge base:', self.knowledge_base)
        print()




# tests
agent = Agent()
A, B, C = symbols('A B C')
print(agent.entailment(knowledge_base=None, query=Or(A, Not(A))))
agent = Agent()
print(agent.entailment(knowledge_base=None, query=And(A, Not(A))))


agent = Agent()
A, B, C = symbols('A B C')
agent.tell(And(A, B))
agent.tell(Or(A, B))
print('Does', agent.knowledge_base, 'entails', B, '?', agent.ask(B))
print('Does', agent.knowledge_base, 'entails', C, '?', agent.ask(C))
agent.revision(Not(B), contraction_function=agent.contraction)


agent = Agent()
p, q, r = symbols('p q r')
agent.tell(p)
agent.tell(q)
agent.tell(r)
agent.revision(Not(Or(q, r)), contraction_function=agent.contraction)


agent = Agent()
p, q = symbols('p, q')
agent.tell(p)
agent.tell(q)
agent.tell(Or(Not(p), q))
agent.revision(Not(q), contraction_function=agent.contraction)

agent = Agent()
p, q = symbols('p, q')
agent.tell(Or(Not(p), q))
agent.tell(p)
agent.tell(q)
agent.revision(Not(q), contraction_function=agent.contraction)
