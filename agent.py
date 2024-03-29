import sympy
from sympy import symbols, And, Or, Not, Xor, Implies
from sympy.logic.boolalg import to_int_repr, to_cnf
from itertools import combinations

class Agent:
    def __init__(self, name=None):
        if name is None:
            self.name = "Agent" + str(id(self))
        else:
            self.name = name
        self.knowledge_base = list()

    def get_clauses(self, expr):
        if not isinstance(expr, And):
            if expr == True:
                return {}
            if isinstance(expr, Or) or isinstance(expr, Not):
                return {expr}
            return expr,
        return set(expr.args)

    def tell(self, sentence):
        if sentence not in self.knowledge_base:
            self.knowledge_base.append(sentence)
        return list(self.knowledge_base)

    def ask(self, query):
        return self.entailment(knowledge_base=self.knowledge_base, query=query)

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

    def resolution(self, set_of_formulas):
        cnf = to_cnf(And(*set_of_formulas))
        clauses = to_int_repr(self.get_clauses(cnf), cnf.free_symbols)
        #if isinstance(cnf, Or):
        #    clauses = [set.union(*clauses)]
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
        return self.resolution(set(knowledge_base).union({Not(query)}))

    def remainders(self, set_a_list, phi, return_all=False):
        return_remainders = list()

        if not self.entailment(knowledge_base=set_a_list, query=phi): # here phi is actually Not(phi) since it's called by contraction(Not(Phi)), which is called by revision(phi)
            return set_a_list

        for i in range(1, len(set_a_list) + 1):
            # Trying to remove first the older formulas/clauses (or combination of them). 
            # This is ensured by the order of the formulas in the list.
            to_remove_formulas = [x[0] if len(x) == 1 else x for x in combinations(set_a_list, i)]
            for to_remove_formula in to_remove_formulas:
                for to_remove_clause in self.get_clauses(to_cnf(to_remove_formula)):
                    # If we need to remove combination of clauses
                    if isinstance(to_remove_clause, sympy.Tuple):
                        new_remainders = self.get_clauses(to_cnf(And(*set_a_list))) - set(self.get_clauses(to_cnf(And(*to_remove_clause))))
                        #new_remainders = self.get_clauses(to_cnf(And(*set_a_list))) - set(to_remove_clause)
                    # If we need to remove one clause at a time    
                    else:
                        new_remainders = self.get_clauses(to_cnf(And(*set_a_list))) - {to_remove_clause}
                    if not self.entailment(knowledge_base=new_remainders, query=phi):
                        if return_all is False:
                            return list(new_remainders)
                        else:
                            if not list(new_remainders) in return_remainders:
                                return_remainders.append(list(new_remainders))

        return return_remainders

    def contraction(self, query):
        remainders = self.remainders(set_a_list=self.knowledge_base, phi=query)
        self.knowledge_base = remainders

    def revision(self, query, test=True, verbose=True):
        original_knowledge_base = self.knowledge_base.copy()
        if verbose: print(self.name, 'is revising', original_knowledge_base, 'with', query)
        # With this check, test_revision_success is not fulfilled
        #if self.is_consistent(query):
        #    self.contraction(Not(query))
        #    print(self.name, '\'s new knowledge base after contraction:', self.knowledge_base)
        #    self.tell(query)

        self.contraction(Not(query))
        if verbose: print(self.name, '\'s new knowledge base after contraction:', self.knowledge_base)
        self.tell(query)

        revised_knowledge_base = self.knowledge_base.copy()
        if verbose: print(self.name, '\'s updated knowledge base:', revised_knowledge_base, "\n")

        if test is True:
            #query = self.get_clauses(to_cnf(query))
            assert self.test_revision_success(phi=query, revision_result=revised_knowledge_base)
            assert self.test_revision_inclusion(phi=query, revision_result=revised_knowledge_base, original_knowledge_base=original_knowledge_base)
            assert self.test_revision_vacuity(phi=query, revision_result=revised_knowledge_base, original_knowledge_base=original_knowledge_base)
            assert self.test_revision_consistency(phi=query, revision_result=revised_knowledge_base)
            assert self.test_revision_extensionality(phi=query, psi=None, revision_result_phi=revised_knowledge_base, original_knowledge_base=original_knowledge_base)

        return list(self.knowledge_base)

    """ Phi is in the knowledge base after revision with phi """
    def test_revision_success(self, phi, revision_result=None):
        if revision_result is not None:
            return self.entailment(query=phi, knowledge_base=revision_result)

        self.revision(phi, test=False)
        return self.ask(phi)

    """ The knowledge base revised with phi is a
    subset of the knowledge base expanded with phi """
    def test_revision_inclusion(self, phi, revision_result=None, original_knowledge_base=None):
        if revision_result is not None and original_knowledge_base is not None:
            original_knowledge_base = self.get_clauses(to_cnf(And(*original_knowledge_base)))
            revision_result = self.get_clauses(to_cnf(And(*revision_result)))
            return set(revision_result).issubset(set(original_knowledge_base).union(self.get_clauses(to_cnf(phi))))

        original_knowledge_base = list(self.knowledge_base)
        revised = self.revision(phi, test=False)

        # Reset knowledge base
        self.knowledge_base = original_knowledge_base

        expanded = self.tell(phi)

        return (set(revised)).issubset(set(expanded))

    """ If the negation of phi is not in the knowledge base then the knowledge
    base revised with phi is the same as the knowledge base expanded with phi """
    def test_revision_vacuity(self, phi, revision_result=None, original_knowledge_base=None):
        if revision_result is not None and original_knowledge_base is not None:
            original_knowledge_base = self.get_clauses(to_cnf(And(*original_knowledge_base)))
            revision_result = self.get_clauses(to_cnf(And(*revision_result)))
            if not self.entailment(query=Not(phi), knowledge_base=original_knowledge_base):
                return set(revision_result) == set(original_knowledge_base).union(self.get_clauses(to_cnf(phi)))
            return True

        if not self.ask(Not(phi)):
            original_knowledge_base = list(self.knowledge_base)
            revised = self.revision(phi, test=False)

            # Reset knowledge base
            self.knowledge_base = original_knowledge_base

            expanded = self.tell(phi)
            return revised == expanded
        return True

    """ The knowledge base revised with phi is consistent if phi is consistent """
    def test_revision_consistency(self, phi, revision_result=None):
        if revision_result is not None:
            if self.is_consistent({phi}):
                return self.is_consistent(revision_result)
            return True

        self.revision(phi, test=False)
        return not self.ask(And(Not(And(*self.knowledge_base)), And(*self.knowledge_base)))


    def is_consistent(self, phi):
        #phi_list = self.get_clauses(to_cnf(phi))
        return not self.resolution(phi)
        #return not self.resolution(query=And(Not(And(*phi_list)), And(*phi_list)), knowledge_base=phi_list)


    """ If phi and psi are equivalent then the knowledge base revised
    with phi is the same as the knowledge base revised with psi """
    def test_revision_extensionality(self, phi, psi=None, revision_result_phi=None, original_knowledge_base=None):
        if revision_result_phi is not None and original_knowledge_base is not None:
            if psi is None:
                # Create a semantically equal formula
                psi = to_cnf(And(phi, And(phi, phi)))
            if self.equivalent(phi, psi):
                agent_psi = Agent()
                if len(original_knowledge_base) > 0:
                    #original_knowledge_base = self.get_clauses(to_cnf(And(*original_knowledge_base)))
                    for belief in original_knowledge_base:
                        agent_psi.tell(belief)

                revision_result_psi = agent_psi.revision(psi, test=False, verbose=False) # To avoid infinite recursion

                contracted_phi = to_cnf(And(*revision_result_phi), simplify=True)
                contracted_psi = to_cnf(And(*revision_result_psi), simplify=True)

                return contracted_phi == contracted_psi

            return True


        if self.equivalent(phi, psi):
            original_knowledge_base = list(self.knowledge_base)

            self.revision(phi, test=False)
            contracted_phi = list(self.knowledge_base)

            # Reset knowledge base
            self.knowledge_base = list(original_knowledge_base)

            self.revision(psi, test=False)
            contracted_psi = list(self.knowledge_base)

            contracted_phi = to_cnf(And(*contracted_phi), simplify=True)
            contracted_psi = to_cnf(And(*contracted_psi), simplify=True)

            return contracted_phi == contracted_psi
        return True

    def equivalent(self, phi, psi):
        # Two formulas are equivalent if their bi-conditional is a tautology
        biconditional = And(Or(Not(phi), psi), Or(Not(psi), phi))
        return self.entailment(knowledge_base=set(), query=biconditional)

if __name__ == "__main__":
    agent = Agent()
    p,q,r,s,t = symbols('p q r s t')
    agent.tell(p)
    agent.tell(q)
    agent.tell(p & q)
    agent.tell(p | q)
    agent.tell(p >> q)
    print(agent.knowledge_base, "⊥ q:" ,  agent.remainders(agent.knowledge_base, q, return_all=True))

    agent = Agent()
    p,q,r,s,t = symbols('p q r s t')
    #agent.revision((p|q) & (Not(r) | Not(s) | t))
    #agent.revision((p|q|r) & (q|Not(r)|(s>>t)))
    knowledge_base_ex = [to_cnf((p|q) & (Not(r) | Not(s) | t))]
    query_ex = (p|q|r) & (q|Not(r)|(s>>t))
    print("Does", knowledge_base_ex, "|=", query_ex, "?:", agent.entailment(knowledge_base=knowledge_base_ex, query=query_ex))

    agent = Agent()
    a, b, c = symbols('a b c')
    agent.revision(a | b >> c)
    agent.revision(a | c)
    agent.revision(Not(a))
    agent.revision(Not(c))

    agent = Agent()
    a, b, c = symbols('a b c')
    agent.revision(a & b & c)
    agent.revision(b | Not(c))
    agent.revision(Not(b))


    agent = Agent()
    A, B, C = symbols('A B C')
    agent.revision(Or(A, And(B, Not(C))))
    agent.revision(And(A, Not(A)))
    agent.revision(A | B >> C)

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
    print("Does Alice belief Not(q)?", alice.ask(Not(q)))
    bob.revision(Not(p))
    print("Does Bob belief Not(q)?", bob.ask(Not(q)))

    # AGM tests
    agent = Agent()
    A, B = symbols("A B")
    agent.tell(Or(A, Not(B)))
    # agent.tell(Or(A, B))

    phi = A
    psi = B

    # Test the AGM postulates
    print(f"> Success: {agent.test_revision_success(phi)}")
    print(f"> Inclusion: {agent.test_revision_inclusion(phi)}")
    print(f"> Vacuity: {agent.test_revision_vacuity(phi)}")
    print(f"> Consistency: {agent.test_revision_consistency(phi)}")
    print(f"> Extensionality: {agent.test_revision_extensionality(phi, psi)}")
