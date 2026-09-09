# Short thoughts on Gödel's letter to von Neumann

This week in general and today in particular seems like an appropriate day for a philosophical post about computer mathematics.

Perhaps the earliest formulation of the P vs NP problem appears in a letter from Kurt Gödel to John von Neumann, ([here is a transcription](https://rjlipton.com/the-gdel-letter/))^[Although I've also seen this [letter from John Nash to Major D. M. Grosjean](https://gwern.net/doc/cs/cryptography/nash/1955-nash) posited as a slightly earlier formulation] .
The relevant section is (paraphrasing mine):

> If there really were a (Turing) machine (deciding the existence of length n proofs of formulas of first order predicate logic) with (runtime) ∼ k ⋅ n (or even ∼ k ⋅ n²), this would have consequences of the greatest importance.
> Namely, it would obviously mean that in spite of the undecidability of the Entscheidungsproblem, the mental work of a mathematician concerning Yes-or-No questions could be completely replaced by a machine.
> After all, one would simply have to choose the natural number n so large that when the machine does not deliver a result, it makes no sense to think more about the problem."

## My thoughts

The passage is very insightful.
Nevertheless, with the benefit of hindsight, I feel we can argue that the letter gets it wrong in two ways.

On one hand, Gödel doesn't account for the possiblity that even if P!=NP, it might still be the case that all human mathematical work on open questions can be mechanized, because we might develop a machine that would come up with a proof whenever a human could have.

<!-- Feels spiritually similar to [Heuristica](https://www.cs.mun.ca/~kol/courses/6743-w15/papers/russell-fiveworlds.pdf) -->

On the other hand, it might also not be so simple "to choose the natural number n so large that when the machine does not deliver a result, it makes no sense to think more about the problem."
If the ∼ k ⋅ n² proof search program can be run for n steps, it would only require 4x the resources to run for 2n steps.
Such an increase could be worthwhile, if the chances of and rewards for success were high enough.
So it seems like human judgement might still end up part of the mathematical process, both to assess the likelihood that more computation would yield a useful result, and to determine what the value of such a result would be

Perhaps I should leave it to the reader to decide which of these observations is the optimistic one, and which the pessimistic.