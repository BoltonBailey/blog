# Probabilistic and Cryptographic Logical Systems

*For a while this was in my research ideas folder.
Then it became part of my thesis and I wrote code for it.
Inspired by [this discussion](https://leanprover.zulipchat.com/#narrow/stream/144837-PR-reviews/topic/.237214).*

This post is about certain ways in which logical systems fail to be able to prove certain statements.
The reader might be familiar with Godel's famous theorems about this topic.
But the "unprovable" statements we will discuss will hopefully seem much more mundate than the Godel sentence.

## Introduction: Formal Proof of Primality

The following question came up for me while I was working on [formalizing](https://github.com/leanprover-community/mathlib/pull/8002) [Bertrand's Postulate](https://en.wikipedia.org/wiki/Bertrand%27s_postulate) in [Lean](https://leanprover.github.io/)'s [mathlib](https://github.com/leanprover-community/mathlib).
Bertrand's postulate is the theorem that there is a prime between any positive number and its double.
There is an elegant [proof](https://en.wikipedia.org/wiki/Proof_of_Bertrand%27s_postulate) which has made this problem part of [a benchmark](https://www.cs.ru.nl/~freek/100/) for mathematical formalization systems.

To summarize the relevant aspects of the proof: We prove there is a prime between $n$ and $2n$ by first proving a simple exponential lower bound on the $n$th central binomial coefficient, $\binom{2n}{n}$.
We then assume that there is no prime between $n$ and $2n$ and then examine the prime factorization of $\binom{2n}{n}$ and use this to prove a *subexponential* upper bound on this binomial coefficient.
For sufficiently large $n$ these bounds contradict each other.

The last step (and the step I initially thought would be easiest to formalize) is the "cleanup step" of proving the statement true for all $n$ below the threshold where the contradictory bounds argument kicks in.
This basically means making a list of primes, each less than twice the last, up to the threshold.
The threshold is $468$ in the Wikipedia proof, so the list $3, 5, 7, 13, 23, 43, 83, 163, 317, 631$ works there.
In our case, due to the difficulty of formalizing the calculus implicitly used in the proof, I did an arithmetical proof which was a bit looser, and so I was led in the direction of extending this list up to about $2 \cdot 10^8$.

Unfortunately, I was to find that the lean `norm_num` tactic, which had worked for proving the primality of `631`, timed-out on the proof of the 8-digit prime.
The `norm_num` tactic works (at the time of writing) by checking all possible factors up to the square root of the target, which is an exponential-time algorithm.

This was frustrating mainly because, these tests should not even be exponential time.
In principle, one could create a primality-resolving tactic by:

1. Formalizing the [AKS primality test](https://en.wikipedia.org/wiki/AKS_primality_test)
2. Formalizing the proof in the AKS paper that this algorithm correctly decides PRIMES.
3. Running the algorithm on the desired inputs.

But even this felt a little wrong to me.

The above approach would take us from exponential time to polynomial time - AKS (or improvements thereof) run in $O((\log n)^6)$ time.
But while this is polynomial time, it's a slow polynomial time - I wouldn't want to run it on a 1000-digit number.
Much faster would be to run the [Miller-Rabin test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test), taking only $O((\log n)^2)$ time.

The trouble with the Miller-Rabin test is that it's probabilistic.
It has an extremely high chance of correctly determining whether or not a number is prime if it is repeated a few hundred times - we would not expect even a single error to occur carrying out such tests for a universe lifetime.
But mathematically, this fact takes the form of a statement about probabilities of outcomes of the algorithm, rather than a statement comprising a traditional proof about the prime in question.
It therefore isn't possible to use Miller-Rabin to prove to a proof assistant that a particular natural number is prime.

I am not the first to notice that this situation is somewhat philosophically complicated.
The paper introducing the Miller-Rabin primality test ran a computation to determine that $2^400-593$ was prime.
[This blog post](https://gilkalai.wordpress.com/2021/04/22/the-probabilistic-proof-that-2400-593-is-a-prime-a-revolutionary-new-type-of-mathematical-proof-or-not-a-proof-at-all/) by Gil Kalai highlights that, at the time, we could not deterministically prove this, despite the fact that we knew it to be true.
This should tell us that our conception of proof should go beyond just what we can prove deterministically.

What I think I would like to add to the conversation is that we can still construct statements like this, if we work hard enough.
If, say, we asked "of the first million integers greater than 10^10000, how many are prime?", it seems unlikely that AKS or ECC based methods would be performant enough to provably answer this question, even though it could be answered with Miller-Rabin in a reasonable amount of time.

<!-- 
## Table summarizing proof systems for primes

| Name                              | Complexity                       | Fraction of Primes Indicated    | Deterministic? | Correct? |
| --------------------------------- | -------------------------------- | ------------------------------- | -------------- | -------- |
| Pratt                             | $\exp(\tilde{O}(\log(n)^{1/3}))$ | All                             | Yes            | Yes      |
| Original AKS                      | $\tilde{O}(\log(n)^{12})$        | All                             | Yes            | Yes      |
| Original AKS (under assumptions)  | $\tilde{O}(\log(n)^{6})$         | All                             | Yes            | Yes      |
| Latest AKS (no assumptions)       | $\tilde{O}(\log(n)^{6})$         | All                             | Yes            | Yes      |
| Goldwasser-Killian                | $O(\log(n)^4)$                   | All but $2^{-n^{1/\log\log n}}$ | Yes            | Yes      |
| Miller-Rabin with $\log n$ checks | $\tilde{O}(\log(n)^3)$           | All but $2^{-O(n)}$             | No             | Yes      |
| Miller-Rabin                      | $\tilde{O}(\log(n)^2)$           | All but $2^{-k}$                | No             | No       | 
-->

## Probabilistic Proofs: An Axiom?

<!-- 
What if the degree of the running time of AKS is too large, or the AKS proof is complicated, so I just want to prove my primes using Miller-Rabin? For a concrete example Wikipedia says that ["The difference between consecutive primes, II" by Baker, Harman, and Pintz (paywalled)](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms/83.3.532) is currently the best generalization of Bertrand, it proves that for some $x_0$ that could be determined "with enough effort", for $x > x_0$ there is a prime in $[x-x^{0.525}, x]$. Perhaps we might want to work out what this paper gives us for $x_0$, then start trying to lower the number by giving explicit examples of primes for smaller $x$. (Although, this might not be a good example, since you might be able to grind down the constant on this easily with some kind of certificate, if you were clever enough about giving up on a particular certificate when it took too long. [This](https://arxiv.org/pdf/1401.4233.pdf) might be better, thanks to Gerry Myerson on MathOverflow for pointing it out). 
-->

So what am I to do if I need to use the fact that a particular large number is prime in my proof and I don't want to formalize a complicated deterministic test?
It seems like I will have to somehow modify my Lean environment to be able to accept probabilistic proofs.
Perhaps the easiest way to do this would be to create a Lean `axiom` that directly asserted that probabilistically proved statements are true.
This way, we could avoid modifying the kernel, we would just introduce the statement as an axiom.

Here is what one version of this axiom might look like:

```lean
import Mathlib

TODO

def SampleSpace := Fin (2 ^ 256)

def H (n i x : ℕ) : SampleSpace := sorry -- A hash function

def p (i : Nat) : Prop := sorry -- The family of propositions we are proving

axiom probabilistic 
  (n : Nat) -- Say the randomness of the probabilistic algorithm is sampled from 0 to n-1
  (q : Fin n -> Bool) -- Our algorithm, represented as a map from the sample space to the space of propositions/booleans.
  (hq : n/2 < ((List.finRange n).filter q).length -> p) -- proof that if p is false, q is unlikely to be true
  (h : ∀ i ∈ Finset.range 256, q (H n k i)) -- Condition representing that q is true on 256 "random samples"
  : p
```

## NO

Unfortunately, we cannot simply substitute a cryptographic hash function like SHA256 for `H`.

This runs into the same self-reference problem I discussed [earlier](#updating-consensus-with-formal-rules).
Someone can construct a problem as follows:

- Set p to "false"
- Set n to 1000
- Set q x to a statement equivalent to: "x = SHA256("false", \_q, 1000, i) for some i in range 256"

Since p is "false", the "not p implies q usually false" condition reduces to "q usually false".

Clearly, q x *is* usually false for any value of `_q`; indeed it is only true for at most 256 inputs out of 1000.

But then plugging these facts into the lemma would imply false.
All that remains is to construct a description `_q` of a function `q`, the interpretation of which is equivalent to this condition.
This can be done using quines: Letting `f` be a program which takes a description of (a function from descriptions to expressions) and outputs an expression: on input `_g`, `f` outputs

`f _g = \lambda x, exists i in range 256, x = SHA256("false", descr(eval(_g) _g), 1000, i)`

... where `eval` is a function (in lean) that maps a description to their lean values `descr` maps a lean value to a description of it.
In other words, for any `_g` describing `g`

`f _g <-> \lambda x, exists i in range 256, x = SHA256("false", descr(g _g), 1000, i)`

then let `q = f _f`, so that

`q <-> \lambda x, exists i in range 256, x = SHA256("false", descr(f _f), 1000, i)`

and if, more than simply letting `q = f _f`, we make this definition so that `_q = descr(f _f)`

`q <-> \lambda x, exists i in range 256, x = SHA256("false", _q, 1000, i)`

Which is what we need.

## Automation

You could avoid this whole problem with the hash function if you are willing to modify the kernel to use an RNG to come up with witnesses to prove.
I think you can prove that any system where the witnesses are generated deterministically at runtime is a no-go.
This is interesting: If all you wanted was fast prime checking, I could give you some SHA256 based witness generator.
Even if you gave me (not *my computer*, but *me* in the meta-level sense) a list of BPP problems, I could give you a formal system for all of them.
But I can't make a general purpose formal system.

A weird philosophical question would be: What would happen if some famous math problem...are there any propositions where we have some class of statements where >50% being true implies that all are true, and when we randomly sample them, we can prove \~60% of the statements we sample, but %40 get really complicated?

## Other Domains than primes

See [this stackexchange](https://cstheory.stackexchange.com/questions/31195/when-does-randomization-speed-up-algorithms-and-it-shouldnt) and [this stackexchange](https://cstheory.stackexchange.com/questions/27974/problems-in-mathsfbpp-not-known-to-be-in-mathsf-p) for example problems.

## Integrating cryptography with formal methods proofs

Let's say you could make a [SNARK with collision resistant hash functions](https://eprint.iacr.org/2011/443.pdf) ([see also](https://eprint.iacr.org/2014/580.pdf)) (I'm not sure if this link is exactly that, but ignore this for now).
Then is it the case that if we could include the axiom

`forall a b : list bool, sha256(a) = sha256(b) -> a = b`

... and then use the SNARK construction to make succinct formal proofs within the system?

Trouble is, I think we can prove false from this, [even constructively](https://math.stackexchange.com/a/910790), using the pigeonhole principle.

Is there another logic, satisfying the analogy:

  | logic              | function type                          |
  | ------------------ | -------------------------------------- |
  | classical logic    | functions                              |
  | constructive logic | computable functions                   |
  | *some other logic* | (t-time/polytime) computable functions |

Where each proposition comes with a "time to construct".
You could still prove false from the above axiom in this logic if you were god, but you could not prove false with a time bound less than exponential, so maybe we only accept lemmas with a given time bound.

[See this](https://math.stackexchange.com/a/228604).
[Also, this](https://link.springer.com/article/10.1007/BF01302964).

[Formal verification of probabilistic algorithms by Joe Hurd](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-566.pdf) seems related, but on deeper inspection is just about the non-axiom part.

<!-- 

Could quantum randomness help? 

Another Or paper.
https://eprint.iacr.org/2026/356.pdf

The OSS paper, section 7
https://eprint.iacr.org/2020/107.pdf#page=30.64

This paper linked by it
https://link.springer.com/chapter/10.1007/978-3-030-56877-1_21

 -->
