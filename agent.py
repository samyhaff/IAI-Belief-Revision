import sympy
from sympy import symbols, And, Or, Not
from sympy.logic.boolalg import to_int_repr, to_cnf
from itertools import combinations


class Agent:
    def __init__(self, name="Agent"):
        self.name = name
        self.knowledge_base = list()

    def get_clauses(self, expr):
        if not isinstance(expr, And):
            return expr,
        return set(expr.args)

    def tell(self, sentence):
        # print('Adding', sentence, 'as', to_cnf(sentence))
        # self.knowledge_base.add(to_cnf(sentence))
        print(self.name, 'now beliefs that', sentence)
        self.knowledge_base.append(sentence)
        print(self.name, '\'s new knowledge base:', self.knowledge_base)
        return list(self.knowledge_base)

    def ask(self, query):
        return self.resolution(query)

    def resolve(self, clause1, clause2):
        resolvents = set()
        for literal1 in clause1:
            for literal2 in clause2:
                if literal1 == - literal2:
                    new_clause1 = clause1 - {literal1}
                    new_clause2 = clause2 - {literal2}
                    new_clause = new_clause1.union(new_clause2)
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
        # print('Clauses:', clauses)
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
        # set_a = to_cnf(And(*set_a)) # change the order of the KB, so we are losing the temporal order of the formula
        # set_a_list = set_a.args
        set_a_list = set_a
        # remainders = set(copy.deepcopy(set_a_list))

        if not self.entailment(knowledge_base=set_a, query=phi):
            return set_a

        for i in range(1, len(set_a_list)):
            to_remove_formulas = [x[0] if len(x) == 1 else x for x in combinations(set_a_list,
                                                                                   i)]  # check if the order make sense (YES: it discard before the last added formulas/clause)
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

    # def partial_meet_contraction(self, query):
    #     print('Contracting', self.knowledge_base, 'with', query)
    #     remainders = self.remainders(set_a=self.knowledge_base, phi=query)
    #     if len(remainders) > 0:
    #         # self.knowledge_base = set.intersection(*[set(fs) for fs in remainders]) # doesn't always work
    #         self.knowledge_base = set(remainders[0])  # testing purposes
    #     return set(self.knowledge_base)

    # def partial_meet_contraction_samy(self, query):
    #     new_knowledge_base = set()
    #     clauses = to_cnf(And(*self.knowledge_base)).args
    #     for clause in clauses:
    #         clause_set = set()
    #         clause_set.add(clause)
    #         if not self.entailment(clause_set, query):
    #             new_knowledge_base.add(clause)
    #     self.knowledge_base = new_knowledge_base

    def revision(self, query, contraction_function):
        print(self.name, 'is revising', self.knowledge_base, 'with', query)
        contraction_function(Not(query))
        print(self.name, '\'s new knowledge base after contraction:', self.knowledge_base)
        self.tell(query)
        print(self.name, '\'s updated knowledge base:', self.knowledge_base)
        print()
        return list(self.knowledge_base)

    """ If phi is not a tautology then phi is not in the 
    closure of the knowledge base contracted with phi """
    def test_contraction_success(self, phi):
        # If phi is not a tautology (test if the negation of phi is unsatisfiable)
        # if not (not satisfiable(Not(phi))):
        if not agent.entailment(set(), phi):
            # Check if phi is in the closure of knowledge base contracted with phi
            contracted = self.partial_meet_contraction(phi)
            if agent.entailment(contracted, phi):
                return False
        return True


    """ The contracted knowledge base is a subset of the original knowledge base """
    def test_contraction_inclusion(self, phi):
        contracted = self.partial_meet_contraction(phi)
        return contracted.issubset(self.knowledge_base)


    """ If phi is not in the closure of the knowledge base then the 
    knowledge base contracted with phi is the original knowledge base """
    def test_contraction_vacuity(self, phi):
        original_knowledge_base = set(self.knowledge_base)
        if not agent.entailment(self.knowledge_base, phi):
            contracted = self.partial_meet_contraction(phi)
            return contracted == original_knowledge_base
        return True


    # consistency?
    """ The original knowledge base is a subset of the result of
    contracting it with phi and then expanding it with phi  """
    def test_contraction_recovery(self, phi):
        original_knowledge_base = set(self.knowledge_base)
        contracted = self.partial_meet_contraction(phi)
        expanded = agent.tell(phi)

        """ DEBUG """
        # print("Original knowledge base:", original_knowledge_base)
        # print("Contracted knowledge base:", contracted)
        # print("Expanded knowledge base:", expanded)

        return original_knowledge_base.issubset(expanded)


    """ If phi and psi are equivalent then the knowledge base contracted 
    with phi is equivalent to the knowledge base contracted with psi """
    def test_contraction_extensionality(self, phi, psi):
        original_knowledge_base = set(self.knowledge_base)
        if agent.equivalent(phi, psi):
            contracted_phi = self.partial_meet_contraction(phi)

            # Reset knowledge base
            self.knowledge_base = original_knowledge_base

            contracted_psi = self.partial_meet_contraction(psi)
            return contracted_phi == contracted_psi
        return True


    def equivalent(self, phi, psi):
        # Two formulas are equivalent if their bi-conditional is a tautology
        biconditional = And(Or(Not(phi), psi), Or(Not(psi), phi))
        return agent.entailment(set(), biconditional)


    """ Phi is in the knowledge base after revision with phi """
    def test_revision_success(self, phi):
        self.revision(phi, self.contraction)
        return self.ask(phi)


    """ The knowledge base revised with phi is a 
    subset of the knowledge base expanded with phi """
    def test_revision_inclusion(self, phi):
        original_knowledge_base = list(self.knowledge_base)
        revised = self.revision(phi, self.contraction)

        # Reset knowledge base
        self.knowledge_base = original_knowledge_base

        expanded = agent.tell(phi)

        return (set(revised)).issubset(set(expanded))


    """ If the negation of phi is not in the knowledge base then the knowledge 
    base revised with phi is the same as the knowledge base expanded with phi """
    def test_revision_vacuity(self, phi):
        if not self.ask(Not(phi)):
            original_knowledge_base = list(self.knowledge_base)
            revised = self.revision(phi, self.contraction)

            # Reset knowledge base
            self.knowledge_base = original_knowledge_base

            expanded = agent.tell(phi)
            return revised == expanded
        return True


    """ The knowledge base revised with phi is consistent if phi is consistent """
    def test_revision_consistency(self, phi):
        self.revision(phi, self.contraction)
        return not self.ask(And(Not(And(*self.knowledge_base)), And(*self.knowledge_base)))


    """ If phi and psi are equivalent then the knowledge base revised 
    with phi is the same as the knowledge base revised with psi """
    def test_revision_extensionality(self, phi, psi):
        if self.equivalent(phi, psi):
            original_knowledge_base = list(self.knowledge_base)

            self.revision(phi, self.contraction)
            contracted_phi = list(self.knowledge_base)

            # Reset knowledge base
            self.knowledge_base = list(original_knowledge_base)

            self.revision(psi, self.contraction)
            contracted_psi = list(self.knowledge_base)

            return contracted_phi == contracted_psi
        return True
    
    

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
p, q = symbols('p q')
agent.tell(p)
agent.tell(q)
agent.tell(Or(Not(p), q))
agent.revision(Not(q), contraction_function=agent.contraction)

agent = Agent()
p, q = symbols('p q')
agent.tell(Or(Not(p), q))
agent.tell(p)
agent.tell(q)
agent.revision(Not(q), contraction_function=agent.contraction)

agent = Agent()
p, q = symbols('p q')
agent.tell(p)
agent.tell(q)
agent.revision(Not(q), contraction_function=agent.contraction)

alice = Agent("Alice")
p, q = symbols('p q')
alice.tell(p)
alice.tell(q)

bob = Agent("Bob")
p, q = symbols('p q')
bob.tell(p)
bob.tell(And(
    Or(Not(p), q),
    Or(Not(q), p)
    )
)

alice.revision(Not(p), alice.contraction)
bob.revision(Not(p), bob.contraction)

# AGM tests
agent = Agent()
A, B = symbols("A B")
agent.tell(And(A, B))
# agent.tell(Or(A, B))

phi = A
psi = B

# Test the AGM postulates
print(f"> Success: {agent.test_revision_success(phi)}")
print(f"> Inclusion: {agent.test_revision_inclusion(phi)}")
print(f"> Vacuity: {agent.test_revision_vacuity(phi)}")
print(f"> Consistency: {agent.test_revision_consistency(phi)}")
print(f"> Extensionality: {agent.test_revision_extensionality(phi, psi)}")
