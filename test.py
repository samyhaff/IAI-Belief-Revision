kb = to_cnf(kb)
not_phi = to_cnf(Not(phi))

clauses = And(kb, not_phi) # already sorted by number of literals
#clauses = [list(clause.args) for clause in clauses.args] # list of clauses, each composed by list of literals
clauses = to_int_repr(clauses.args, symbols) # already sorted by number of literals
print('clauses:', clauses)    

# print(np.array(clauses).flatten())
# literals = set(clauses)
# print('literals', literals)

literals_clauses = defaultdict(list)
for clause_id, clause in enumerate(clauses):
    # TODO: delete clauses containing both A and notA
    for literal in clause:
        #heappush(literals_clauses[literal], (len(clause), clause_id))
        literals_clauses[literal].append((len(clause), clause_id))
        
#print(literals_clauses)        
    
# not necessary: already sorted    
# for literal, clauses in literals_clauses.items():
#    clauses.sort(key=clauses[0])

print('literals:', literals_clauses.keys())

i = 0
while(i < len(clauses)):
    for literal in clause:   
        if (literals_clauses[- literal] is not None):
            new_clause = resolve(clause, literals(not literal)[0])
            if is_empty(new_clause):
                return True
            clauses.append(new_clause) # TODO: sort by number of literals
            i = 0            
    i = i+1
                            
return False    

def resolve(clause1, clause2):

    return new_clause

def is_empty(clause):

    return True
    

