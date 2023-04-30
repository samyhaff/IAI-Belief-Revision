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
        if sentence not in self.knowledge_base:
            self.knowledge_base.append(sentence)
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
        set_a_list = set_a

        if not self.entailment(knowledge_base=set_a, query=phi):
            return set_a

        for i in range(1, len(set_a_list)):
            to_remove_formulas = [x[0] if len(x) == 1 else x for x in combinations(set_a_list, i)] 
            for to_remove_formula in to_remove_formulas: 
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

    def revision(self, query):
        print(self.name, 'is revising', self.knowledge_base, 'with', query)
        self.contraction(Not(query))
        print(self.name, '\'s new knowledge base after contraction:', self.knowledge_base)
        self.tell(query)
        print(self.name, '\'s updated knowledge base:', self.knowledge_base, "\n")
        return list(self.knowledge_base)

    """ Phi is in the knowledge base after revision with phi """
    def test_revision_success(self, phi):
        self.revision(phi)
        return self.ask(phi)

    """ The knowledge base revised with phi is a 
    subset of the knowledge base expanded with phi """
    def test_revision_inclusion(self, phi):
        original_knowledge_base = list(self.knowledge_base)
        revised = self.revision(phi)

        # Reset knowledge base
        self.knowledge_base = original_knowledge_base

        expanded = agent.tell(phi)

        return (set(revised)).issubset(set(expanded))

    """ If the negation of phi is not in the knowledge base then the knowledge 
    base revised with phi is the same as the knowledge base expanded with phi """
    def test_revision_vacuity(self, phi):
        if not self.ask(Not(phi)):
            original_knowledge_base = list(self.knowledge_base)
            revised = self.revision(phi)

            # Reset knowledge base
            self.knowledge_base = original_knowledge_base

            expanded = agent.tell(phi)
            return revised == expanded
        return True

    """ The knowledge base revised with phi is consistent if phi is consistent """
    def test_revision_consistency(self, phi):
        self.revision(phi)
        return not self.ask(And(Not(And(*self.knowledge_base)), And(*self.knowledge_base)))

    """ If phi and psi are equivalent then the knowledge base revised 
    with phi is the same as the knowledge base revised with psi """
    def test_revision_extensionality(self, phi, psi):
        if self.equivalent(phi, psi):
            original_knowledge_base = list(self.knowledge_base)

            self.revision(phi)
            contracted_phi = list(self.knowledge_base)

            # Reset knowledge base
            self.knowledge_base = list(original_knowledge_base)

            self.revision(psi)
            contracted_psi = list(self.knowledge_base)

            return contracted_phi == contracted_psi
        return True
    
    def equivalent(self, phi, psi):
        # Two formulas are equivalent if their bi-conditional is a tautology
        biconditional = And(Or(Not(phi), psi), Or(Not(psi), phi))
        return agent.entailment(set(), biconditional)
    
if __name__ == "__main__":
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
    agent.revision(Not(B))

    agent = Agent()
    p, q, r = symbols('p q r')
    agent.tell(p)
    agent.tell(q)
    agent.tell(r)
    agent.revision(Not(Or(q, r)))

    agent = Agent()
    p, q = symbols('p q')
    agent.tell(p)
    agent.tell(q)
    agent.tell(Or(Not(p), q))
    agent.revision(Not(q))

    agent = Agent()
    p, q = symbols('p q')
    agent.tell(Or(Not(p), q))
    agent.tell(p)
    agent.tell(q)
    agent.revision(Not(q))

    agent = Agent()
    p, q = symbols('p q')
    agent.tell(p)
    agent.tell(q)
    agent.revision(Not(q))

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

    alice.revision(Not(p))
    bob.revision(Not(p))

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