
# Explaining Constructive Russell's Paradox with Lean

[Five stages of accepting constructive mathematics](https://www.ams.org/journals/bull/2017-54-03/S0273-0979-2016-01556-4/S0273-0979-2016-01556-4.pdf) is a nice introduction to [constructivism](https://en.wikipedia.org/wiki/Constructivism_(philosophy_of_mathematics)) by [Andrej Bauer](https://math.andrej.com/). But whenever I come back to it, I always get confused by the following passage:

> Theorem 1.1 (Russell). There is no set of all sets.

> Proof. Let us follow a classic text on set theory, such as that by Halmos [11, Sect. 2]
or Jech [13, 1.11]. Suppose V were the set of all sets, and consider its subset

> R = { x ∈ V | x ∉ x }.

> Observe that
>
> (1) if R ∈ R, then by the definition of R also R ∉ R, which is absurd;
> (2) if R ∉ R, then again by the definition of R also R ∈ R, which is absurd.
>
> These two observations are both proofs of negation, the first one proving ¬(R ∈ R)
and the second ¬(R ∉ R). By the law of noncontradiction this cannot be the case,
therefore there is no set of all sets. ∎

> This is indeed a proof of negation: we assume that the set of all sets exists, and
we derive a contradiction. We could read the above splitting of the proof into two
observations as an application of excluded middle (either R ∈ R or R  ∈ R), but we
do not have to!

## My Explanation

I think I am primarily confused by the last paragraph of the proof, where I often fail to remember the definition of the notation ¬(R ∈ R) := R ∉ R. If I had to rewrite the proof to emphasize the constructivism, I would write

> Proof. Let us follow a classic text on set theory, such as that by Halmos [11, Sect. 2]
or Jech [13, 1.11]. Suppose $V$ were the set of all sets, and consider its subset

> R = { x ∈ V | x ∉ x }.

> Observe that
>
> (1) if R ∈ R, then by the definition of R also R ∉ R, which is absurd;
> (2) if R ∉ R, then again by the definition of R also R ∈ R, which is absurd.
>
> These two observations are both proofs of negation, the first one proving ¬(R ∈ R) = (R ∉ R)
and the second ¬(R ∉ R). Applying modus ponens, we obtain false. Thus, we have reached contradiction from the assumption that there is a set of all sets.
Therefore there is no set of all sets. ∎

In Lean the two different proofs are ([sandbox](https://live.lean-lang.org/#codez=FDCWFsAcHsCcBcAEBZAhvAFgG1AIxACYCmAZigJ4DKRSAXIgCrmRGK0C8iAznLOSKAB2XeKkEBjVvWRFwuIrC4ZQkCtSTIqNNpx6w+hUmpoA6ErGjh1iABRc2ia5vUBKB8+0duvfsCyzwVGN4E3BZAH1zS2s7BycteDcbAA93BLd6VMAIImCzCytte0AUwkRs7h1EXHJvfV9MIjhZRHrYInDQLnDBaHCuGnDoEnDULCxemk7xLFQuLlBxEdsANTTXBwAaxEAAIlt7aXSAGnKcla8q4EREAForxwBXSBg+xBWAdwVWeu5tQcQRrG+8C4F0QQngFj+o3CYXAIJuf0EBEQ4mgwlAxFgoKB3DuuD6SBB/iQACUKh4QlECkgAN5lFYAH1KiEAkESlAC+cNu0DxCgAbp8MOgQVVwgs+vYMKT6KScsSQQB2663GwARjcAEkyDLEHLLpdBfyHKTWVLOOc9Xr4fVBJVql9iCQhKB4KBUYhfqSRjwdSydSCLbBXogANrk0IRSnqI7qcPgcbwADyQyIAEcALp/JCS/16ojJVDiLPEkwAJhz8NeynEGFB9lQeLusAIObzBaQmA6iGzl0V8JsJY1Wt9ur1BqkPtlFXNFqVzQwRBtqAA5qghLa56wHU6XW6PZDvdqRwGg6GErHIvko45TDD40nwqmjt14MNEU/oC/nxn0F2j3rUI8WDVN2M6toWkJjDCfoWhWVY1p29ZcI2zYWmBRZzh0nKMPOzzwK80DujysC8ugrrCH8rSVB+NaQBYgz2L8ghECuO6CEcXyOooSCoqwtHQLyQhLog6w2IeLhYWISJfH0KKIsJonDi4JiIAAQna86INMQaMaisngqgBDzKxGH2AsgjPpUAqsGKRAHFhLSkI0G6UZ23SAu6ZD/ICXDKYAcET+sA9SNOAzltB0XQ9PiAxDP88aTKiIiwHchagIaNinMEGTCdsuyrDQLhHPYJxTvwlzwpQDxPKwbwfBu7m/F5+LApcYIQrFMISXJslzBiWL2EhPIEpcRI+l4YaRtotKIMVjKpKyyQcmVXJEYamBCktthqogmoTj61rrvapDbmRHk+l6BHGjqRyVvM8F1g2TYgmOyIzG0KobLtpq2jmrUESB+qoIa0rDiVOaXPiv4AOQVP9lrKgARCYylVHVW6CM6ZFIyY8PiTOiCBiGYa3hN8DRjeET4veqbfkWYN/IBwHFmWMEI4hyE4y2+bgR2Eojn2A7bUOJrsfOi4rmuKOHY66PGXu52fddcG1n8D0oV2gPWa94Qlh9l1fdOLWCOCf1/n2iPI+pm5HTLmNIxzFrPcDk5nKVM4E6eMbE5eNBkyEt6U8m6aZr+dNzFAwew5cAGQEBId42hEHQk0pus6r9u5lzSA2eE7081hDA4Z8+GEX0xGkQlFGsLg1GIHx9GnUxLFkSLrCcSI7pMbXFgCYIQkiWJnVSRpMmoki/eKcpWFqXVWkN7pqL6YZKVujzL3mR+ll1TZdmXAn2c69nKr2fOrQkE5DnK25EMNaM3l+UAA))

```lean

import Mathlib

def MySet : Type := sorry

instance : Membership MySet MySet := sorry

def MySet.fromSet (s : Set MySet) : MySet := sorry

lemma MySet.mem_fromSet (s : Set MySet) (x : MySet) : x ∈ MySet.fromSet s ↔ x ∈ s := by sorry

theorem there_is_no_set_of_all_sets_classical (V : MySet) : ¬ ∀ (s : MySet), s ∈ V := by
  -- Suppose V were the set of all sets
  intro all_mem
  -- and consider its subset 
  let R := MySet.fromSet {x ∈ V | x ∉ x}
  -- observe that
  by_cases hR : R ∈ R
  · -- (1) If R ∈ R
    have : R ∉ R := by
      -- then by the definition of R also R ∉ R
      rw [MySet.mem_fromSet, Set.mem_setOf_eq] at hR
      exact hR.2
    -- which is absurd
    exact this hR
  · -- (2) If R ∉ R
    have : R ∈ R := by
      -- then again by the definition of R also R ∈ R
      rw [MySet.mem_fromSet, Set.mem_setOf_eq, not_and, not_not] at hR
      apply hR
      exact all_mem R
    -- which is absurd
    exact hR this
  -- These two observations are both proofs of negation, the first one proving ¬(R ∈ R)
  -- and the second ¬(R ∉ R). By the law of noncontradiction this cannot be the case,
  -- therefore there is no set of all sets. ∎
   
theorem there_is_no_set_of_all_sets_constructive (V : MySet) : ¬ ∀ (s : MySet), s ∈ V := by
  -- Suppose V were the set of all sets
  intro all_mem
  -- and consider its subset 
  let R := MySet.fromSet {x ∈ V | x ∉ x}
  -- observe that
  -- (1) If R ∈ R then by the definition of R also R ∉ R, which is absurd
  have case_1 : ¬ R ∈ R := by
    intro hR
    have : R ∉ R := by
      set hR' := hR
      -- (".. by the definition...")
      rw [MySet.mem_fromSet, Set.mem_setOf_eq] at hR
      apply hR.2
    -- ("absurd")
    exact this hR
  -- (2) If R ∉ R, then again by the definition of R also R ∈ R, which is absurd
  have case_2 : ¬ R ∉ R := by
    intro hR
    -- (".. by the definition...")
    have : R ∈ R := by
      rw [MySet.mem_fromSet, Set.mem_setOf_eq] at hR
      simp at hR
      apply hR
      exact all_mem R
    -- ("absurd")
    exact case_1 this
  -- These two observations are both proofs of negation, the first one proving ¬(R ∈ R)
  -- and the second ¬(R ∉ R). 
  -- By the law of noncontradiction this cannot be the case,
  exact case_2 case_1
  -- therefore there is no set of all sets. ∎
```
