# Lazy Wordle

- There is analysis of [notions optimal play](https://tomjohnston.co.uk/blog/2022-02-07-optimal-wordle-strategies.html) and [compression of the word list](https://www.youtube.com/watch?v=JYN25TeM5kI)
- What I am interested in is: Is there a simply describable strategy which guarantees that I win?
- Something like: Guess these three words, then depending on the outcome, guess these two other words, and then there will be one winning choice left in the guess list.
- Concrete **Question**: Does there exist a set of 5 words in the wordle guess list, such that for any word in the wordle solution list, there is no other word in the guess list consistent with the revealed information.

In symbols: Let `is_consistent(true_solution, reveal, potential_solution)` be the ternary relation on words which describes the statement, "if `true_solution` is the true solution and `reveal` is guessed so that the information about letters from `reveal` is known, is `potential_solution` consistent with those revelations"

```
exists (guesses : Fin 5 \to guessList), \forall (solution : solutionList) (final_guess : guessList), solution \neq final_guess \to \exists i : Fin 5, not is_consistent (solution, guesses i, reveal)
```

Note that the predicate

```
\forall (solution : solutionList) (final_guess : guessList), solution \neq final_guess \to \exists i : Fin 5, not is_consistent (solution, guesses i, reveal)
```

amounts to asking "is there a guess among the fivve guesses which distinguishes this pair".
So this reduces to a SetCover instance
