# Performal Methods

*A Software-Optimization Approach for Formal Theorem Marketplaces*

In my day job, I work with the [Lean 4 Programming Language and Proof Assistant](https://lean-lang.org/).
In keeping with my interest in markets, I [have often wondered](https://thequantummilkman.substack.com/p/futarchy-for-math) whether it would be possible to get a marketplace for code in this language off the ground.
Others, many in the cryptocurrency space, are interested too -- besides [theorem-marketplace](https://theorem-marketplace.com/), a few other people have presented [their](https://inftychi.vercel.app/) [demos](https://agora.stagiralabs.com/) on the Lean forum.

Lean 4 is interesting in that it's been heavily focused on research mathematics, due the gravitational influence of its premier project, [mathlib](https://github.com/leanprover-community/mathlib4).
In my previous posts, I was somewhat pessimistic about the possibility of a market for mathematical theorems for various reasons.
But I think there is perhaps more potential for a marketplace like this to succeed if it were focused on the computer science / software domain.
In this post, I'll discuss my thoughts on this.

## The Basic Concepts

### What is a proof assistant?

Lean is a "proof assistant" which essentially means it is a programming language capable of representing mathematical propositions and proofs.
In principle, any mathematical statement can be expressed in such a language.
The process of taking a proposition or proof expressed in natural language and converting it to code is called "formalization".
Here is a formalization of the claim that there are infinitely many primes: The line with `theorem` is the statement, and the subsequent lines are the proof.
The code also imports and uses other theorems and definitions (in particular the factorial function, and the function which returns the minimum prime factor of any natural).

```lean
import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Data.Nat.Prime.Defs
import Mathlib.Order.Bounds.Basic

namespace Nat

theorem exists_infinite_primes (n : ℕ) : ∃ p, n ≤ p ∧ Prime p := by
  let p := minFac (n ! + 1)
  have f1 : n ! + 1 ≠ 1 := ne_of_gt <| succ_lt_succ <| factorial_pos _
  have pp : Prime p := minFac_prime f1
  have np : n ≤ p :=
    le_of_not_ge fun h =>
      have h₁ : p ∣ n ! := dvd_factorial (minFac_pos _) h
      have h₂ : p ∣ 1 := (Nat.dvd_add_iff_right h₁).2 (minFac_dvd _)
      pp.not_dvd_one h₂
  exact ⟨p, np, pp⟩
```

[Here is a link to online sandbox](https://live.lean-lang.org/#codez=FASwtgDg9gTgLgAgLIEM4AsA2IBGA6AETRTwDk08AxFAYzlhBUzwCEUBnEG0SWRVDNnxE4JcnDwAFGOACmhWQDN2PaPGRosuPAHkYAE1kxWUAK4A7fe1YcuwYOZRhZ7CLVkJx9jLNiywCLIAHiDscOwA+iDmitEgcLIREDLO7AgAFOYIAFwIgKiEAJQ5CIDARAgQADQIWYAmROUIgORECNJy9dkAvAg4AJ7ACAiYsogQOZ1g0dQ0GVkAhAgA1AgAjAV9COgoAG4eikvFswvLCIAGREcd1YlQihEA5ogAPAA+COymNDQRmHARr+8ITwhFLR6DImEkoGkImsNttyiNci1nG0xhNaEkUjsltCth5zPDqgg6vD2mt+oMIlcIuYoN8bjsLOsEO0AHyk/rrHHrQCBBMURoBiIgJc3O+k2+giQLoDCYGXG5km4MhRXQbP6MI86EAQQS8hACvbndLiPAisUofRikCKa4yG7oRDoLkFPAAJhlqI+xoQEVW7PZEAgeGp32NFPM6o1a2CwIQgAvySrVON+wCX5EA) with this code.
If you move your cursor around in the proof, you will see a readout on the right-hand side communicating intermediate results and manipulations obtained as the proof proceeds.
By the end, the readout says that there are "No goals".

### What is a theorem marketplace?

The idea of the "theorem marketplace" is to have a platform where buyers can formalize statements for which they want proof and provide a bounty for the solution.
Then, sellers can do the (much harder) work to formalize proofs and collect the bounty.

The appealing thing about this is that it centrally utilizes the Lean software's ability to check that a proof has no gaps.
When a desired piece of software is specified informally, it is a matter up for interpretation (and thus contractual dispute) whether software that has been provided is up to spec.
But if the goal is solely to provide a proof of a claim, then Lean's analysis of the proof is all that matters.

### Why software is a good fit for monetizing formal methods

In descriptions of proof assistants and of Lean in particular, it is often possible to come away with the impression that the proofs are solely to do with "math" rather than "programs".
But in fact, Lean is just as much a programming language as a proof assistant, and since programs can be viewed as mathematical objects ([and vice versa](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence)), it is possible to prove things about these too.

The upshot is that it is just about as easy to formalize a notion like "there are infinitely many primes" as it is to formalize the notion that, for example, ["the merge sort algorithm always leaves a list in order"](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/List/Sort.html#List.sorted_mergeSort').

#### The existing formal software verification industry

In fact, most applications of formal languages in industry are along exactly these lines: Essentially, proving that a piece of software meets its description.
It makes perfect sense - technology is a big industry with lots of money to spend, and it has a critical security need to ensure its code is correct.
Furthermore, unlike in math, any particular piece of industrial software generally has a single organization with a primary interest in its correctness, and therefore the possibility for public goods problems related to verifying software is reduced.

There are many small companies that offer their services to formally verify code, like [Galois](https://www.galois.com/), [Runtime Verification](https://runtimeverification.com/), and [CertiK](https://www.certik.com/products/formal-verification).
And there are much larger organizations, like [NASA](https://ntrs.nasa.gov/api/citations/20250006044/downloads/NFM_Keynote_STRIVES-psm.pdf) and [AWS](https://spawn-queue.acm.org/doi/pdf/10.1145/3712057), which use formal tools internally.
The existence of this industry can provide a starting point for any effort to make formal methods more open and widespread.

## Performal Methods: Formal methods for code performance

To be useful, software has to be more than just correct - it has to be performant.
This is where I think there is a big opportunity for markets around formal proof.

Just as one can prove that merge sort correctly sorts a list, one can also prove, given a suitable formal description of the implementation (and model of computation on which that implementation runs) that it will complete in [$O(n log n)$ time, and use $O(n)$ auxiliary space](https://en.wikipedia.org/wiki/Merge_sort).

Suppose I produce an optimization of a function or data structure in the hot path of some heavily-used software library and I prove that it's formally equivalent to the extant implementation.
This gives me several ways of producing a functionally-equivalent but potentially-improved version of the software:

1. I can replace the function with the reimplementation.
2. I can call both implementations in parallel and use whichever returns first.
3. I can run an A-B testing module to determine which is faster on average.
4. If the subroutine is sufficiently heavy, perhaps I can do ML to identify which implementation is best before starting.
5. If space is a constraint, I can run both versions and terminate one when its space consumption grows too large.

And if I have additionally a formal proof of the performance characteristics

1. Simply choose the implementation, for any input size, that performs optimally.

<!-- There could even be other dimensions of performance -->

These options provide a variety of tradeoffs between performance metrics, and different applications will prioritize metrics differently.
But if I can specify the costs of these resources, then when I make savings (directly measured in electricity, processor time, latency, disk-space time) there can be no question what the value of my contribution is.
This provides a convenient baseline for paying out contributors according to the value they provide.

<!-- Relevant, but maybe also attainable https://www.hyrumslaw.com/ -->

## Potential settings for monetizing performal optimization

Where would this kind of optimization find its best home?
I think the best options would be environnments where formal methods are already in relatively common use, and which do computation at a large enough scale that savings are relevant.

I can think of a couple examples.

### Cloud computing

Above, we mentioned [AWS](https://aws.amazon.com/) as an example of an organization which uses formal methods.
Indeed, Amazon are one of the supporters of the [recently-started "CSLib" effort](https://cs-lean.github.io/) to formalize topics in CS in Lean.
AWS also happens to have the [largest share of the global cloud computing market](https://en.wikipedia.org/wiki/Amazon_Web_Services).

The main organizational obstacle to a market for formally-verified optimization of AWS compute tasks would probably be that AWS would like to keep customer code and data private.
But there are a few ways we could still have a marketplace like this even while preserving privacy:

- AWS could identify widespread usage of particular OSS software libraries within its cloud and place bounties on optimizations for these libraries.
- Instead of optimizing code directly, formalists could design formally-verified optimizing compilers, which could operate on production code without the compiler producer having to see that code.

### Blockchains

A few of the other companies I've mentioned that offer formal audits are focused in particular on the blockchain industry.
There is a great need for formal methods in blockchain due to the large amount of money that would otherwise be susceptible to theft through hacks.
But the very reason why hacking is such a big problem here is that blockchain code is publicly visible, which means that code privacy isn't a concern.
So the formal upgrading process I describe above can happen out in the open.

Another reason why formally-verified optimization could be a big win for the blockchain industry is that the complexity of it all offers more dimensions along which optimization can take place.
Instead of simply finding better algorithms for functionally-equivalent code, formal optimizers can potentially completely reengineer protocols in ways that preserve their guarantees.
Here are some concrete examples of levels-of-the-stack where this could be done:

#### At the Cryptography Level

One approach would be to set out a collection of primitives that the protocol uses, formally specify the security requirements for these primitives, and then place bounties for the most effective options.

Consider the [SNARK](https://www.di.ens.fr/~nitulesc/files/Survey-SNARKs.pdf), a primitive used to guarantee the correctness of computation.
There are many different implementations of this primitive, and it seems like every year more research is done on how to make them faster, more secure, more suited to practical methods of algorithm specification, etc. The blockchain community would benefit from formally verified SNARK implementations.
And this is within reach!
FV for SNARKs was a big part of my PhD thesis and there is an now effort supported by the Ethereum Foundation to [formally verify modern SNARK constructions](https://github.com/Verified-zkEVM/ArkLib).

#### At the Consensus Protocol Level

One could imagine using formal upgrading to upgrade the base functionality of a blockchains (the "Layer 1") directly.
Previously, any substantial improvements to the core communication protocols of a blockchain have had to happen through a "hard fork" in which the community agrees on and implements code for an upgraded version of the protocol.
If we had a formal specification of the functionality we wanted the blockchain to implement and a desired performance metric for this functionality, we could propagate and activate formally verified performance upgrades automatically.
This could separate the concerns of the [community specifying its desired features](./utility-function-consensus.md) from the rollout of those features.

#### Fully Integrated "Cryptoeconomic" level

Above the "Layer 1" we have "Layer 2", which is the term used for agile blockchains that are built on top of other blockchains for purposes of speed.
As complex as base blockchains are, Layer 2 systems can be even more complex in the assumptions they make about how cryptoassets move back and forth between them.
I would like to see assumptions about control of cryptoassets move more inside the purview of formal methods, both because I think this would offer more protection for users, and because it would open up new ways of insuring against bad outcomes.
\footnote{For example, you could imagine a formal verification of a system paired with a smart contract for insurance against a violation of some decentralization or cryptographic assumption, so that if users accounts are compromised by this kind of violation, they can get paid back on a more secure chain. [Here is an interesting paper about prediction markets for quantum risk](https://arxiv.org/pdf/2102.00659.pdf)}

## Technical obstacles

Coming back down to Earth, we have to acknowledge that there are a few serious limitations to the state of the art in formal methods that make the kind of system I describe here hard to realize.

1. Most code is not written in languages amenable to full formal verification.
2. Verification is hard to produce, requiring a lot of scarce expertise.
3. The space of complex algorithms any one business uses is limited enough that optimal code can be written in-house.

These are hard challenges, but they seem more technical than social to me.
In particular, if AI becomes very effective at producing formal verification, then this vision could become much more plausible.
So while I think the performal methods markets I've described here aren't likely to come in the next few years, I am more optimistic that they will be developed eventually.
