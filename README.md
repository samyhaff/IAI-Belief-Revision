# Belief Revision Agent

This project implements a belief revision agent that satisfies AGM postulates using propositional logic. The agent can add, revise, and query beliefs in its knowledge base. The code is written in Python and uses the Sympy library for logical expressions.

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

In this example, the agent revises its knowledge base with beliefs `p & q` and `~q`. It then answers a query about belief `p` and prints its current knowledge base. Finally, the agent quits the program.
