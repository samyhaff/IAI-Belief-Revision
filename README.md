# Belief Revision Agent
Belief Revision Assignment as part of the Introduction To Artificial Intelligence course at Technical University of Denmark, A.Y. 2022-2023. 

This project implements a belief revision agent that satisfies AGM postulates using propositional logic. The agent can add, revise, and query beliefs in its knowledge base. The code is written in Python and uses the Sympy library for logical expressions. 
A report explaining the work that has been done for this project is available [here](IAI_report_2_team_17.pdf).


## TODOs
- Remove the possibility of running AGM postulate tests from the console.py (and keep only the part that uses the belief set passed through the parameters);
- Right it is possible to revise with inconsistent formula such as `And(A, Not(A))` and this will result in a new belief base containing only `And(A, Not(A))`.
 
## Requirements

- Python 3.11
- Sympy library (install via `pip install sympy`)

## Instructions

When you run the `console.py` script, the agent will display the following instructions:

```
Enter a prompt:
"i": Instructions
"r b": Revision of belief b
"a b": Ask if belief b is in the knowledge base
"agm postulate": Test AGM Postulates, where postulate is one of the following:
    "success", "inclusion", "vacuity", "consistency", "extensionality"
"p": Print Knowledge Base
"q": Quit

NOTE: Beliefs must be entered in the form of sympy propositional logic. For example, "p & q" can be entered as "And(p, q)" or "p & q"
```

You can use the available prompts to interact with the agent:

- `i`: Display the instructions again.
- `r b`: Revise the agent's knowledge base with belief `b`.
- `a b`: Ask the agent if belief `b` is in its knowledge base.
- `agm postulate`: Test AGM postulates on the agent's revision operation.
- `p`: Print the agent's current knowledge base.
- `q`: Quit the program.

## Example

Here is an example of how to interact with the agent:

```
Enter a prompt:
r p & q

Agent is revising [] with And(p, q)
Agent 's new knowledge base after contraction: []
Agent 's updated knowledge base: [And(p, q)]

Enter a prompt:
r ~q

Agent is revising [And(p, q)] with Not(q)
Agent 's new knowledge base after contraction: [p]
Agent 's updated knowledge base: [p, Not(q)]

Enter a prompt:
a p

b in knowledge set: True

Enter a prompt:
p

Knowledge Base:  [p, Not(q)]

Enter a prompt:
q

Quitting program
```
