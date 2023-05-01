from agent import Agent
from sympy import parse_expr

def instructions():
    print('''Enter a prompt: 
    "i": Instructions 
    "r b": Revision of belief b 
    "a b": Ask if belief b is in the knowledge base 
    "agm postulate": Test AGM Postulates, where postulate is one of the following: 
        "success", "inclusion", "vacuity", "consistency", "extensionality"
    "p": Print Knowledge Base 
    "q": Quit 

    NOTE: Beliefs must be entered in the form of sympy propositional logic. For example, "p & q" can be entered as "And(p, q)" or "p & q"''')


if __name__ == '__main__':
    agent = Agent()

    instructions()

    while True: 
        print('Enter a prompt: ')
        prompt = input().split(" ")

        if prompt[0] == "i":
            instructions()

        elif prompt[0] == "a":
            print("b in knowledge set:", agent.ask(parse_expr("".join(prompt[1:]))), '\n')
        
        elif prompt[0] == "r":
            #print("".join(prompt[1:]))
            belief = "".join(prompt[1:])
            belief = parse_expr(belief)
            agent.revision(belief)
        
        elif prompt[0] == "agm":
            
            match prompt[1]:
                case "success":
                    phi = parse_expr(input("Enter phi: "))
                    print(f"Success: {agent.test_revision_success(phi)}")
                case "inclusion":
                    phi = parse_expr(input("Enter phi: "))
                    print(f"Inclusion: {agent.test_revision_inclusion(phi)}")
                case "vacuity":
                    phi = parse_expr(input("Enter phi: "))
                    print(f"Vacuity: {agent.test_revision_vacuity(phi)}")
                case "consistency":
                    phi = parse_expr(input("Enter phi: "))
                    print(f"Consistency: {agent.test_revision_consistency(phi)}")
                case "extensionality":
                    phi = parse_expr(input("Enter phi: "))
                    psi = parse_expr(input("Enter psi: "))
                    print(f"Extensionality: {agent.test_revision_extensionality(phi, psi)}")
                case _:
                    print('Not a valid postulate. Enter "i" for instructions.')
        
        elif prompt[0] == "p":
            print("Knowledge Base: ", agent.knowledge_base)
        elif prompt[0] == "q":
            print('Quitting program')
            break
        else:
            print('Invalid prompt. Enter "i" for instructions.')