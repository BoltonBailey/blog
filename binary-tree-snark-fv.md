# The Binary Tree of SNARKs and Formal methods

*This post is a broad collection of ideas around integrating cryptography, cryptoeconomics, and formal methods, somewhat [related to this prior post](https://thequantummilkman.substack.com/p/performal-methods).
I'm posting it now because some related ideas came up in the verifed-zkevm telegram chat, so thanks to the members of that chat, and also all the other people I've talked to over the years about aspects of this, (Sanjam Garg, Yupeng Zhang, John Burnham, etc.).*

One of the hallmarks of computer science is that it studies composability.
Most subfields of computer science has its own favorite kind of computer or program and we all love figuring out how best to simulate each other's programs on each of the various kinds.

My favorite kinds of programs are ones which touch on the concept of "proof", like formal verification (FV) systems and SNARKs.
I have noticed you can basically make a binary tree of proof-flavor-applications out of these concepts.
Some nodes of this tree have already been explored in the literature:

- FV(FV): This is the concept of a "verified kernel" where you formally verify the core proof checker in another system (or your own).
- SNARK(SNARK): This is the concept of a "recursive SNARK", where you check a SNARK within another SNARK to avoid the state getting too big.
- SNARK(SNARK(SNARK)): Sometimes we even switch between multiple recursive SNARK verification systems to reach different parts of the performance tradeoff curve.
- FV(SNARK): SNARKs are tricky to implement, so it is nice to formally verify them.
  This was basically the subject of my PhD research and also an ongoing [EF effort](https://verified-zkevm.org/).

I think that a part of the tree which has remained relatively unexplored is SNARK(FV) and other branching off points from that, so that is what I'm doing to discuss today.

## Theorem proving with a SNARK verifier

One could associate each proof in the Lean system a recursive SNARK, so that checking them would be trivial.
There are a few projects that seem interested in this, like [Ix](https://github.com/argumentcomputer/ix), or [zkPi](https://eprint.iacr.org/2024/267).
One could even construct this SNARK within Lean itself as a function from `Prop` to `Type`, which associates any `Prop` with the subset of byte sequences that check as a valid proof of that `Prop`.

One thing this could be useful for is computation-heavy proofs.
For example, ["all primes up to 300 trillion have a Miller-Rabin witness below 18"](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Testing_against_small_sets_of_bases) or [All odd numbers below 10^27 are a sum of three primes](https://arxiv.org/pdf/1312.7748#page=2.62).
These are useful/cool theorems, but a library like `mathlib` protects its compile time, so it doesn't want to include them for that reason.
If a library/system would allow these SNARK proofs in it's logical framework, we could include these theorems without much cost in recompilation.

This idea raises philosophical questions: Do we as a society really care about the proofs themselves, or just that the proofs exist?
Mathematical aesthetes would say the former, but there are many applications, such as software verification, where the correctness/spec-compliance is most of what matters.

This could be useful for an anti-bloat program-synthesis/logical language based on imports that state what the requirements for the code are, and then code that satisfies those requirements is automatically generated.
You could say "I need a function which takes a list of distinct elements and returns a list with the same elements where each element is greater than the last", and the computer would say, "ok, here's a sorting function, with succinct proof that it's asymptotically optimal".

In languages like Go and Rust you can import GitHub libraries, and these are secured in various ways.
One could imagine a language where proofs of common but intensive computations are zkSNARK proved and then put online, so you could use the results of that code without having to run it.
In such a language, functions could be content addressed.
See [Unison](https://www.unisonweb.org/) for a language that does this.

## SNARKed theorem provers as Blockchain Scaling Solutions

Another benefit might be some kind of blockchain acceleration.
Suppose we want to have a blockchain which processes transactions faster than any one node can.
How might we achieve this?
One way is to just publish the transactions included in any block, and then have a team of "SNARK worker nodes" (I think this is [Mina's terminology](https://docs.minaprotocol.com/mina-protocol/snark-workers)) divide those transactions into sets that touch different parts of the state, separately make SNARK proofs about the state changes those transactions effect, and then combine those diffs into a proof of the new state.
The problem is that if we aren't sure how much state is effected, we aren't sure if we are updating in the most efficient way.

SNARKed formal proof could make this faster.
In this system, say you voluntarily place a constraint on your smart contract that prevents it from spending more than 1 ETH per block (you might impose such a spending limit anyway as a protection against hacking).
If I have 100 ETH 99 blocks ago, and if I then make a Uniswap transaction now, then the SNARK worker responsible for my transaction *doesn't even have to wait for the state of my contract* to be computed for the previous block!
They can just take the state from 100 blocks ago, and SNARK a formal proof that my transaction will succeed in this block because I can't have possibly spent enough money to have gone bankrupt.
This gives the SNARK worker a head start on computing the final state of the Uniswap pair, and makes the whole thing run faster.

Another example could be a governance mechanism.
Let's say enough votes are in to be certain that a certain vote succeeds.
Then a SNARK worker can prove this formally and get that state out without checking what the rest of the votes are.

<!-- 
[See this link](https://decentralizedthoughts.github.io/2021-10-16-the-ideal-state-machine-model-multiple-clients-and-linearizability/) that might be relevant. -->

## Updating Cryptography Formally

This is maybe getting into a deeper layer of the tree, like SNARK(FV(SNARK)).

I attended the [Science](https://cbr.stanford.edu/sbc22/) [of](https://cbr.stanford.edu/sbc23/) [Blockchain](https://www.sbc-conference.com/2024/) conference several years during my PhD (and in fact I think it was at this conference that I first discussed some of these ideas with Sanjam Garg).

There are many wonderful papers at SBC on cryptography/consensus algorithms, all claiming to have benefits in terms of performance for SNARKs/other blockchain protocols.
But we cannot upgrade the major blockchains/zk-rollups every time one of these papers comes out, since there is too much academic overhead to checking the math and gaining social consensus on each new upgrade.
Formal methods could save the day: Encode the properties you want your protocol to have, along with metrics for how well it performs, and allow anyone to submit a protocol upgrade if it comes with formal proof that it does better at achieving the metrics.

More broadly, this could apply not just to blockchains a whole, but to arbitrary blockchain systems/functionalities/smart contracts.
Cryptographers who formally prove their work achieves some goal better than the best extant solution could submit their formalizations to cryptonetworks, have them automatically adopted, and get paid for the computing resources they save (again, see [prior post](https://thequantummilkman.substack.com/p/performal-methods)).

There would be some big social downsides to this, and a technical downside.
The social downsides are along the lines that it would be hard to get social consensus for the initial upgrade from non-upgradable to upgradable.
This is especially true because whatever metric you choose will possibly benefit some users over others it, and would generally make the system more chaotic ( I plan on me and my business competitors having a certain compute resource usage, but then it suddenly drops down, and then it suddenly shoots back up again and a different usage aspect goes down more, etc.)

### The ROM issue

The technical downside is a frustrating issue with SNARKs in particular that I haven't been able to solve to my satisfaction.

To be a bit clearer about the model, I am envisioning something like this for the basic architecture of how the Formal verification can be wrapped up an internalized into the SNARK checking: We have some bog-standard "Fast Verifier SNARK" that we want to convert into something that has a fast prover.
So we design a "Fast Prover SNARK" as fast as we possibly can make it and formally verify it's sound.
We then verify the formal proof of soundness with the Fast Verifier SNARK, and we save this as a "precomputation" (in blue).
Whenever we want (in our red "hot path") to verify a statement/witness pair for our relation, we verify it with the Fast prover and then fold that verification recursively in with the existing SNARKed formal proof of soundness.
This way we simultaneously achieve:

1. Proving speeds within a \~constant additive factor of the fastest speeds possible.
   Whenever a faster "Fast Prover" is invented, we formally verify it and swap out the proof.
2. We never have to update the user's verifier code, because it is just checking(recursive certificates of) the fast verifier.

![](./Screenshot%202026-05-15%20at%2014.20.35.png)

Let's say that we are comfortable using the random oracle model in our cryptography/SNARKs.
The typical way of implementing such a protocol in the real world would be to instantiate it with a known hash function like SHA256.

The problem is that a malicious protocol implementer might know that we are going to do this and plan for it.
Lets say we have a `Prover(x, w), Verifier(x, proof)` pair and a proof that this constitutes a SNARK in the ROM.
The Malicious implementer might switch the verifier out for

`Verifier'(x, proof) := Verifier(x, proof) \or Hash(proof) = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`

In fact `Prover, Verifier'` is still secure in the ROM.
As far as the ROM is concerned `ba78...15ad` is just a random sequence of characters and it's statistically impossible to find a preimage to it.
But in the real world, this string is `SHA256("abc")`, so the malicious prover can now cause any proof it wants to verify.

We could try to do some kind of Fiat-Shamir kung fu and make sure that SHA256 calls includes some kind of hash of the `Prover, Verifier` protocol code itself.
But this doesn't work either: The adversary might make the code for the consensus algorithm a quine such that it can evaluate the SHA256 of the protcol code from within the code itself.

[The Random Oracle Methodology, Revisited, by Canetti, Goldreich, and Halevi](https://eprint.iacr.org/1998/011.pdf) seems relevant.
It gives schemes secure in the ROM that are insecure with any instantiation.
Does the idea of checking these algorithms are "well-typed" in some sense indeed rule these algorithms out?
Can we come up with some kind of "meta-random-oracle-model" where we design a formal proof system resistant to this?
This all seems like a really challenging problem.
See also [this](https://www.math.uwaterloo.ca/~ajmeneze/publications/rom.pdf) and [this](https://www.researchgate.net/publication/225142528_Formal_Methods_and_Cryptography).

<!-- 
## A role for Universal Composability

Perhaps one way to code this would be to bake in (some version of) the [UC framework](https://en.wikipedia.org/wiki/Universal_composability) and let people implement faster and faster implementations of UC secure primitives.

## Composing Cryptography with Economics

Another aspect ryptography can be composed with economics, making the term "cryptoeconomics" very concrete
  * For example, suppose I have some functionality that depends on a cryptographic assumption, in such a way that it becomes publicly obvious if the assumption is broken in a way that breaks the construction. This could be "composed" with a prediction market on the break being reported, so that one can buy insurance in the scheme not being broken, and therefore potentially gain an unconditionally secure primitive.
    * See this paper, which proposes this for [quantum assumptions](https://arxiv.org/pdf/2102.00659.pdf).

## Automatic Eigenlayer

Formal methods for EigenLayer: Allow stakers to join eigenlayer pools with formal assurance that they won't be slashed if they follow the protocol. -->
