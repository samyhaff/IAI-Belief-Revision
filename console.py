from agent import Agent
from sympy import symbols, And, Or, Not, Implies, parse_expr
from sympy.logic.boolalg import to_int_repr, to_cnf
from itertools import chain, combinations

agent = Agent()

def instructions():
    print('Enter a prompt: ')
    print('"i": Instructions ')
    print('"r b": Revision of belief b ')
    print('"c b": Partial Meet Contraction of belief b ')
    print('"agm postulate": Test AGM Postulates, where postulate is one of the following: \n\t"success", "inclusion", "vacuity", "consistency", "extensionality"')
    print('"p": Print Knowledge Base ')
    print('"q": Quit ')

    print('NOTE: Beliefs must be entered in the form of sympy propositional logic. For example, "p & q" is entered as "And(p, q)"')


if __name__ == '__main__':

    prompt = "running"

    instructions()


    while True:
        
        print('Enter a prompt: ')
        prompt = input().split(" ")

        if prompt[0] == "i":
            instructions()
        
        elif prompt[0] == "r":
            print("".join(prompt[1:]))
            belief = "".join(prompt[1:])
            belief = parse_expr(belief)
            agent.tell(belief)

        elif prompt[0] == "c":
            print("".join(prompt[1:]))
            belief = "".join(prompt[1:])
            belief = parse_expr(belief)
            agent.partial_meet_contraction_samy(belief)
        
        elif prompt[0] == "agm":
            
            match prompt[1]:
                case "success":
                    print('agm')
                    #print(f"Success: {agent.test_revision_success(phi)}")
                case "inclusion":
                    print('agm')
                    #print(f"Inclusion: {agent.test_revision_inclusion(phi)}")
                case "vacuity":
                    print('agm')
                    #print(f"Vacuity: {agent.test_revision_vacuity(phi)}")
                case "consistency":
                    print('agm')
                    #print(f"Consistency: {agent.test_revision_consistency(phi)}")
                case "extensionality":
                    print('agm')
                    #print(f"Extensionality: {agent.test_revision_extensionality(phi, psi)}")
                case _:
                    print('Not a valid postulate. Enter "i" for instructions.')
        
        elif prompt[0] == "p":
            print("Knowledge Base: " + agent.knowledge_base)
        elif prompt[0] == "q":
            print('Quitting program')
            break
        else:
            print('Invalid prompt. Enter "i" for instructions.')



    

