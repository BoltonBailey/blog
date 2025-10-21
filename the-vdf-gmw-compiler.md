
# The VDF GMW Compiler

*This post assumes some knowledge of topics in crypto, like zk-SNARKs and VDFs. Thanks to Sylvain Bellemare, Sam Breckenridge, Or Sattath, Pratyush Tiwari, and the hosts of "The Quantum State Podcast", for disscussing this topic with me, and Alex Obadia for linking me the article I mention below, which was the impetus for writing this post.*

Here is an image of the "Verge" section of Vitalik Buterin's roadmap diagram.

![Verge](./verge.png)

I want to draw your attention to the "Fully-SNARKed Ethereum" item, towards the end of this list. If you are reading this post, likely you know what it means to SNARK a circuit or program. But what does it mean to SNARK a protocol? How do we know that it will be possible to do to Ethereum, especially in light of uncertain future upgrades that might change Ethereum in unpredictable ways?

As it turns out, these questions have answers that date back to the 80s. This post goes over this concept and possible extensions of it.

## The GMW compiler

I didn't realize this before [TAing a class on MPC](https://courses.grainger.illinois.edu/cs598dh/sp2024/) last term, but the concept that is today called "SNARKing a protocol" or "wrapping a protocol in a SNARK" goes back to [the 1987 paper "How to play any Mental Game" of Goldwasser, Micali, and Widgerson](https://www.cs.miami.edu/home/burt/learning/Csc609.062/docs/gmw.pdf). In academic circles, the idea goes by the name of "The GMW Compiler".

The idea is ultimately very simple. Suppose we have a protocol that some computers want to undertake. We are concerned that some computers may try, on their own or in collaboration with others, to subvert the normal functioning of the protocol. We can prevent this by augmenting the protocol with zero-knowledge proofs:

> In fact, he is required to prove, in zero-knowledge (in the sense of Goldwasser, Micali and Rackoff [GoMiRa]), that each message he sends is what he should have sent being honest, given his private input, his random choices and the messages he received so far. (Here, an essential tool is our recent result that all NP languages possess zero-knowledge proofs [GMW].)

![gmw](./gmw.png)

One thing that GM and W have swept under the rug a bit here is the fact that the zero-knowledge proofs here have to themselves check the validty proofs of the zero-knowledge proofs from messages sent in previous rounds of the protocol.\footnote{There is actually more description immediately after this about how one can get rid of omission faults too with an honest majority assumption, but I'll put that aside.} Thus, it is pretty highly important for the practicablity of this technique that the zero knowledge proofs do not take more computation to check than they do to generate, and that the checking procedure can itself be proven in zero-knowledge efficiently.

Luckily, in the intervening decades between this paper being published and now, we have invented zero-knowledge proofs that do just this, in the form of recursive zk-SNARKs. In 2024, we are basically now in a golden age for this, in terms of how many people are working on this problem to make this technology more usable and efficient, so it seems like now is a good time to consider this concept more thoroughly.

## Protocol Compilation in general and VDFs

Part of what is so attractive about this construction is that it is essentially fully general. The GMW compiler makes some additional assumptions, such as that every participant has committed to their inputs, an honest majority assumption, and a synchronous network model. But even when we remove these assumptions and just apply the generic SNARKing form of the compiler, I feel the resulting protocol is usually instructive in that it highlights the remaining security holes. It's an interesting perspective: Instead of asking where we need to apply a particular cryptographic primitive, we simply apply it everywhere, letting the primitive do as much work as it possibly can, and ask "what could possibly go wrong".

This leads us to the question: What primitives, other than "recursive zk-SNARK" could we create a "protocol compiler" for?

Verifiable Delay Functions seem like a good candidate. Just as SNARKs create a sort of "correctness guarantee", VDFs create a "timing guarantee". They are themselves not totally unrelated to SNARKs, in their "Verifiability". Here's how I envision the VDF compiler for a protocol working:

1. All parties to the protocol possess hardware to compute a VDF.
2. When the protocol begins, or a party joins the network, every party exchanges random messages with new parties, which they hash into their VDF state.
3. Whenever any party receives a message, or whenever a party introduces external information into the protocol, this message/info is hashed, with a timestamp, into the VDF state.
4. Whenever a party sends a message, they include their VDF state and a proof of the time at which the message was sent.
5. We additionally run the classic GMW compiler on all of this, and in that spirit, parties always check that VDFs are valid and consistent with the timestamps, and that the timestamps are consistent with the current time, ignoring messages that don't validate.

Simplest to demonstrate is how this works for just two parties, where it looks like this:

![vdf](./vdfcompiler.png)

The beauty is that, by virtue of each message coming with its own VDF, the lower party can know when the input to the upper party was introduced to the protocol: They know that it must have been introduced no later than the claimed time since otherwise the second VDF would not have had time to be computed, and (while the upper party might have some kind of foreknowledge of what the information will be) the official introduction of the information to the protocol can be no earlier than the time the last iteration of the first VDF was created. A caveat is that this only holds to within the tolerance of the VDF (i.e. how much longer an honest party takes to compute it than an adversary).

## Applications

Unfortunately, it is a bit hard to come up with existing applications that could benefit from this kind of compilation, because this compiler sort of presupposes that the protocol uses timestamps in a way that is critical to security. Nevertheless, there are a few concepts:

### Preventing "Time Warp" attacks

Time warp attacks refer to attacks in blockchains that manipulate the time at which blocks are published. My colleague Or and I [have a paper](https://arxiv.org/abs/2403.08023) about a type of time warp attack using a quantum computer, which could potentially be prevented by more secure block timestamps.

### Preventing MEV

The concept of "sequencing" refers to the fact that blockchains need to decide on the order transactions will be executed, and the fact that this can sometimes have monetary consequences for the transactors and the entity doing the sequencing. [This post](https://research.chainbound.io/exploring-verifiable-continuous-sequencing-with-delay-functions) proposes VDFs as a way of ensuring sequencers are producing their sequences at the time they claim to.

### Generally having more precise timing of events on blockchains

For example, say I want to host a (puzzle competition / timed chess game / HFT market) on a blockchain. By having the participants compute VDFs on their inputs, the chain can get a more fine-grained view of when they arrive than would otherwise be possible with a coarse-grained slot time.