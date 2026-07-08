# [Futarchy for math](https://thequantummilkman.substack.com/p/futarchy-for-math)

Previously, [I wrote](https://thequantummilkman.substack.com/p/speculations-on-adoption-of-theorem) about [Vadim's work](https://ratandtiger.substack.com/p/a-theorem-marketplace-awaits-your) towards a [decentralized marketplace for formal theorems](https://theorem-marketplace.com/).
Now, he's [announced](https://ratandtiger.substack.com/p/theorem-marketplace-source-code) that the code for this site [has been made open-source](https://github.com/wadimiusz/theorem-marketplace).
Hooray!

In honor of this, and in keeping with some of my [recent](https://thequantummilkman.substack.com/p/better-Futarchy-with-combinatorial) [posts](https://thequantummilkman.substack.com/p/Futarchy-and-manipulability) on [Futarchy](https://mason.gmu.edu/~rhanson/Futarchy.html), here are some thoughts on the potential synergies of these epistemic technologies.

## Theorem marketplaces and the theory-building problem

In a [footnote](https://thequantummilkman.substack.com/p/speculations-on-adoption-of-theorem#footnote-anchor-6-153779803) on my previous post, I alluded to how I thought that one challenge formal theorem bounties face has to do with "theory building", (which is a term I took from [this essay](https://www.dpmms.cam.ac.uk/~wtg10/2cultures.pdf) by W.T. Gowers, I encourage you all to read it).

To elaborate on this with a visual example, take a look at this diagram.

![](https://substackcdn.com/image/fetch/$s_!dVXD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e7cc791-3787-414e-b99a-216343eaecbb_2048x386.png)

This graph (zoomable/clickable version [here](https://alexkontorovich.github.io/PrimeNumberTheoremAnd/web/dep_graph_document.html)) is the dependency chart for the ["Prime Number Theorem +" project](https://alexkontorovich.github.io/PrimeNumberTheoremAnd/web/sect0001.html), a [multi-collaborator](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/graphs/contributors) effort to formalize various versions of the [prime number theorem](https://en.wikipedia.org/wiki/Prime_number_theorem) in Lean.
As should be clear from the picture, the vast majority of effort in this project is not to do with direct formalization of PNT itself from its direct dependencies.
Rather, most of the work has to do with the formalization of those dependencies (and of the dependencies of the dependencies, et cetera).

The larger the theorem gets, the harder this becomes.
I would like to be able to show you the same chart for [Kevin Buzzard's project to formalize Fermat's Last Theorem](https://imperialcollegelondon.github.io/FLT/), but unfortunately it's grown so large that it seems it's been [split](https://imperialcollegelondon.github.io/FLT/blueprint/dep_graph_chapter_9.html) up [into](https://imperialcollegelondon.github.io/FLT/blueprint/dep_graph_chapter_10.html) multiple [pages](https://imperialcollegelondon.github.io/FLT/blueprint/dep_graph_chapter_12.html).
The FLT project is a particularly interesting example because as [Kevin has described](https://www.youtube.com/watch?v=MH4XDFEUUaA), an important part of the work of that project was making choices about what proof approach to take - As I understand it, much mathematical research has been done on the ideas behind Wiles' original proof, and there are now multiple versions of the FLT proof to choose from.
For the sake of the FLT project's success, it's important to choose one that will be amenable to formalization.

The problem this poses to theorem marketplaces is: Given that so much of the work of formalizing a major theorem is nonproximate to the proof of the theorem itself, how can we ensure that those who complete that work are compensated in proportion to their contribution?
Put another way, how can markets do the important work of planning out something like a dependency chart in advance, so that we can tell what low level work is really needed?

## Futarchy to the rescue

The framing of "markets need to formulate a plan" suggests Futarchy as an answer.
And closer inspection suggests this could be a promising application for other reasons: For example, the person or team most confident in a particular plan seems likely to be both the one(s) with the most expertise in the style of approach behind that plan, as well as the most holdings in shares that the plan will succeed.
Thus, there is a built-in incentive mechanism for them to contribute work towards realizing that plan when the Futarchy decides to use it.
Many of the markets the Futarchy makes will touch on related formal questions, and so there will likely be arbitrage opportunities to support the liquidity in these markets.
Also, the formal verification procedure provides an uncontroversial resolution mechanism.

## A Proposal

<!-- Basically, the question is: If we were to fund smart contracts to produce a formalization of FLT, how would we go about it?

One way would just be the naive "formalize FLT and you get all the money". I think the essential problem with this is that it's not factorable: people can't claim money for partial credit. -->

Here is a proposal.
Effectively, you could think of this as parametrizable pseudocode for a futarchic smart contract designed to maximize the likelihood of creating a successful formal proof of a target theorem by a target date.

1. We start with the theorem to be proved by year XXXX.
   (For example ["Fermat's Last Theorem will be formally proved by 2029"](https://manifold.markets/BoltonBailey/will-we-have-a-formalized-proof-of))
2. Some percentage of the funding is set aside as a prize for the formalization itself
3. The rest is set aside for the recursive construction of markets for intermediate results
4. People can then propose candidates for what these results will be in the form of "factorizations": Pairs or sets of subclaims that together imply the result (for example: "the Taniyama-Shimura conjecture is true" and "Taniyama-Shimura conjecture implies Fermat's last theorem").
   The important considerations for the subclaims are that they:
   1. Are likely to be proved by year XXXX (As a recursively constructed futarchic contract will attempt to make true)
   2. Together, they consitute formal proof of the main theorem (As guaranteed by the formal proof verification procedure)
5. If multiple factorizations are proposed, Futarchy decides which factorization gets funded.

You could augment this in a few ways:

- Make additional markets about the length of the proofs, and motivate the Futarchy to find a short one, so that the proof is more comprehensible.
- If you are interested in a proof without a particular preference over time frame, you could create multiple futarchies, and set up an agent to bet NO on near-term proofs which funds those futarchies with its profits.
