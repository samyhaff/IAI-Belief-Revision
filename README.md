# Belief Revision Agent
## Output
```
Agent now beliefs that A & B
Agent 's new knowledge base: [A & B]
Agent now beliefs that A | B
Agent 's new knowledge base: [A & B, A | B]
Does [A & B, A | B] entails B ? True
Does [A & B, A | B] entails C ? False
Agent is revising [A & B, A | B] with ~B
Agent 's new knowledge base after contraction: [A | B, A]
Agent now beliefs that ~B
Agent 's new knowledge base: [A | B, A, ~B]
Agent 's updated knowledge base: [A | B, A, ~B]

Agent now beliefs that p
Agent 's new knowledge base: [p]
Agent now beliefs that q
Agent 's new knowledge base: [p, q]
Agent now beliefs that r
Agent 's new knowledge base: [p, q, r]
Agent is revising [p, q, r] with ~(q | r)
Agent 's new knowledge base after contraction: [p]
Agent now beliefs that ~(q | r)
Agent 's new knowledge base: [p, ~(q | r)]
Agent 's updated knowledge base: [p, ~(q | r)]

Agent now beliefs that p
Agent 's new knowledge base: [p]
Agent now beliefs that q
Agent 's new knowledge base: [p, q]
Agent now beliefs that q | ~p
Agent 's new knowledge base: [p, q, q | ~p]
Agent is revising [p, q, q | ~p] with ~q
Agent 's new knowledge base after contraction: [p]
Agent now beliefs that ~q
Agent 's new knowledge base: [p, ~q]
Agent 's updated knowledge base: [p, ~q]

Agent now beliefs that q | ~p
Agent 's new knowledge base: [q | ~p]
Agent now beliefs that p
Agent 's new knowledge base: [q | ~p, p]
Agent now beliefs that q
Agent 's new knowledge base: [q | ~p, p, q]
Agent is revising [q | ~p, p, q] with ~q
Agent 's new knowledge base after contraction: [q | ~p]
Agent now beliefs that ~q
Agent 's new knowledge base: [q | ~p, ~q]
Agent 's updated knowledge base: [q | ~p, ~q]

Agent now beliefs that p
Agent 's new knowledge base: [p]
Agent now beliefs that q
Agent 's new knowledge base: [p, q]
Agent is revising [p, q] with ~q
Agent 's new knowledge base after contraction: [p]
Agent now beliefs that ~q
Agent 's new knowledge base: [p, ~q]
Agent 's updated knowledge base: [p, ~q]

Alice now beliefs that p
Alice 's new knowledge base: [p]
Alice now beliefs that q
Alice 's new knowledge base: [p, q]
Bob now beliefs that p
Bob 's new knowledge base: [p]
Bob now beliefs that (p | ~q) & (q | ~p)
Bob 's new knowledge base: [p, (p | ~q) & (q | ~p)]
Alice is revising [p, q] with ~p
Alice 's new knowledge base after contraction: [q]
Alice now beliefs that ~p
Alice 's new knowledge base: [q, ~p]
Alice 's updated knowledge base: [q, ~p]

Bob is revising [p, (p | ~q) & (q | ~p)] with ~p
fuck
Bob 's new knowledge base after contraction: [p | ~q, q | ~p]
Bob now beliefs that ~p
Bob 's new knowledge base: [p | ~q, q | ~p, ~p]
Bob 's updated knowledge base: [p | ~q, q | ~p, ~p]


Process finished with exit code 0

```