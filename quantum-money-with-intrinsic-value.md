# Quantum Commodities

"Quantum money" was originally proposed in 1970, long before the advent of modern cryptocurrency.
It remains an object of academic study, and many variants on it have been proposed.
But most versions suffer from a lack of public verifiability, or else require a lot of complicated cryptography to realize.

In this post, I'll argue for an alternative to public-key quantum money, more analogous to a commodity.

## How one might come to this idea

Here's a series of observations:

1. In order to use a public-key quantum money system you would likely need a fault-tolerant quantum computer to carry out the verification procedure.
2. These devices don't exist today, but if you had them, they would be incredibly valuable, as evidenced by the size of the research budgets going into trying to create them.
3. This suggests something odd - if quantum hardware would be so valuable, *doesn't it seem strange that in order to impart value to the hardware + stored quantum money combination, we would have to artificially define that certain quantum states would have value*?
4. To dig more deeply, it is thought that quantum computers will be valuable precisely due to their ability to carry out computations that classical computers cannot.
5. To restate this in an even more overwrought way, one could say that quantum computers are valuable due to their ability to exist in algorithmic states intermediate between the initial state and the solution during the course of solving classically-hard problems.
6. These intermediate states take the form of quantum data existing on the hardware.
7. This quantum data is, in principle, just as easy to transfer between long-term quantum memory systems as any other form of quantum data.
8. Therefore, we are led to the question **Could the intermediate states of quantum computations be themselves used as a kind of quantum asset?**

## Creation, refinement, and verification of quantum commodities

For concreteness, suppose in the future there was some kind of class of industrial optimization problem to do with searching for improvements to parts of a design (e.g. of an algorithm, or a circuit board layout, or a mechanical system).
Suppose further that the question of whether a new proposed design is more effective than the SoTA is efficiently testable by a (?classical?)
algorithm, and that the most hardware-effective way of finding such a new design is by running Grover's algorithm for a period of time on the order of a few minutes.

We could imagine server farms of quantum computers running Grover iterations to try to compute these optimizations en masse.
Then, if the server farm for some reason needed to stop one of these computation before finishing (e.g. if it couldn't get good electricity rates or if some more profitable computation better suited to its architecture came along), then it could bundle together thousands of these partially-computed Grover states and sell them.
Before sale, bundles could be labelled with their "purity" (i.e. the number of Grover iterations completed).

States like these could be verified for autheticity fairly easily: By analogy to [similar concepts for commodity metals](https://www.iso.org/obp/ui/en/#iso:std:iso:12743:ed-4:v1:en), a representative subsample of the states could be chosen, and the Grover procedure on these states could be run to completion, (or the states could simply be measured as they are, and the success rate could be compared to the ascribed "purity").

These states would technically not be quantum money, because it would be possible to run a polynomial time quantum algorithm to create them from nothing.
But this is not a concern, because the process of this creation is computational work with a useful output which is valuable for its own properties.
Even if it were possible for an attacker to create a subverted version of the commodity that wasn't constructed using Grover's algorithm, as long as it passed verification, it would likely still be useful for industrial purposes (see below).

## Possible Objections

### Could the attacker just reverse the verification on a solution they know works?

One could imagine a few ways to mitigate this:

- The firms interested in buying the quantum commodities could publish lists of problem instances for which solutions had already been found, and the verification procedure could be made to check against these.
  - Note that this would not necessarily catch duplicate commodities if none of the samples happened to overlap.
    For a strogner verification procedure, you could think of verifing $\sqrt{N}$ out of $N$ instances.
- We could be sure to only use as quantum commodities registers for which the Grover iteration was less than halfway done -- this way it would be easier to construct these states the honest way than by the dishonest way.
  - This argument might be strengthened by a fact I alluded to in a [footnote of a previous post](https://thequantummilkman.substack.com/p/quantum-bitcoin-mining#footnote-3-165950580), namely that it is actually optimal to stop Grover iteration before probability 1 is reached.
    So the state in which we expect to measure the register is itself nontrivial to reach - perhaps this means an enhanced verification procedure could be done in which some Grover instances are completed and some are reverted?

### Wouldn't it take as long to verify the money as it would to create it?

Yes, but this is potentially not an issue.
You could imagine Grover instances that take only a few seconds to run to completion being useful as quantum commodities.
The important part is that while the contruction of a large quantity of commodity could take a large parallelized quantum server farm and years of quantum processing time, the verification is a statistical sampling process that requires asymptotically much less compute.

One could also imagine a future where there would be two [different substrates for quantum computation which operate at different speeds](https://m-malinowski.github.io/2022/12/04/how-fast-are-quantum-computers-part-2.html), one which runs much faster, and another which is slower but cheaper to manufacture and run at scale.
You could imagine datacenters built mostly out of the slow substrate passing commodites between each other, resuming each computation immediately upon receipt, verifying the commodities by passing samples to auxiliary high-speed cores.

### Wouldn't the commodites get stale as other entities solved the same problems?

For this to work, we have to imagine that either:

1. There is such a wide multiplicity of different problems that it is unlikely for two commodity instances to overlap.
2. The problems are of a nature where additional solutions to the same problem are as valuable as the first.

### Wouldn't the quantum storage for these commodities be better spent on more cores?

This is a question about the relative ease of constructing quantum memory and quantum compute.
Classical memory is much easier to construct than classical compute, but this might not hold true in the quantum world, especially if there has to be some kind of active error correction procedure to keep the quantum memory alive.
I leave this question open to further speculation, but I also note that the "two different substrates" possibility I mentioned above mitigates this.

## Aesthetic value

This post has argued in favor of quantum assets that have intrinsic value, rather than extrinsic.
But even some real-world commodities like gold blur this distinction, being considered valuable more for aesthetic reasons than just for their applications in industry.
Could we develop a quantum commodity that is valuable for analogous reasons?

Perhaps an answer could come from number-theoretical application of quantum computing - many find number theory to be a beautiful subject, and a deeply meaningful party of humanity's quest to understand nature.
If there were an effort to fund such a thing, we could make a quantum commodity from partial Shor's algorithm factorizations of long sequences of 1000-bit consecutive numbers, or from a [full factorization of many Fibonacci numbers](https://manifold.markets/brubsby/will-any-prime-factor-of-the-1801st).
Besides the self-motivated goal of constructing these sequences for their own sake, they might also serve mathematical research, for example -- by giving mathematicians an avenue to extend [random models of the primes](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_conjecture) to make and test conjectures about properties of the factorizations in these sequences.

<!-- 
TODO: Suppose that usefullness/success isn't binary.
Instead, we have a usefulness score for results we could get. Is there an improvement to Grover over just choosing some usefulness threshhold?
 -->
