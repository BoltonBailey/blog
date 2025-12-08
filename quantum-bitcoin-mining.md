# Quantum Bitcoin Mining

_This post assumes some basic knowledge of Proof-of-Work/"Nakamoto" consensus_

I have long been dissatisfied by the state of public discourse about the consequences of quantum computing for blockchains. If I google "Consequences of quantum computers for bitcoin" on incognito mode, I get the following top 5 results:

- [Quantum computers may threaten crypto protocols by 2030](https://www.verdict.co.uk/quantum-computing-breaking-security-encryption/)
- [Why quantum computing isn’t a threat to crypto... yet](https://cointelegraph.com/news/why-quantum-computing-isn-t-a-threat-to-crypto-yet)
- [Cryptocurrency vs. quantum computing: A deep dive into the future of cryptocurrencies](https://cointelegraph.com/learn/cryptocurrency-vs-quantum-computing-a-deep-dive-into-the-future-of-cryptocurrencies)
- [Could Quantum Computers Defeat Bitcoin? Not So Fast.](https://decrypt.co/101340/bitcoin-quantum-computing)
- [Quantum computers and the Bitcoin blockchain](https://www2.deloitte.com/nl/nl/pages/innovatie/artikelen/quantum-computers-and-the-bitcoin-blockchain.html)

Interestingly, not a single one of these articles mentions Grover's algorithm, they all essentially only deal with the eventuality of Shor's algorithm breaking public-key cryptosystems. YouTube videos are mostly the same, saying regarding quantum Bitcoin mining things like ["SHA256 is quantum resistant"](https://youtu.be/xRPCmG6hx7g?t=195) or ["Grover's algorithm is only a quadratic speed up, so it would weaken SHA256 to SHA128, but that's still pretty large, and we can actually double the keys to get back to the same security"](https://youtu.be/_KG2y116VF4?t=640).

Searching for articles specifically about applying Grover's algorithm to mining, I get

- [Is it possible to mine bitcoin by implementing Grover's algorithm on a quantum computer](https://quantumcomputing.stackexchange.com/questions/9798/is-it-possible-to-mine-bitcoin-by-implementing-grovers-algorithm-on-a-quantum-c)
- [Quantum Bitcoin Mining](https://www.mdpi.com/1099-4300/24/3/323)
- [Is Bitcoin (BTC) Safe from Grover's Algorithm?](https://www.yahoo.com/video/bitcoin-btc-safe-grovers-algorithm-151737053.html)

These articles mostly focus on the capabilities a quantum computer would need to be a successful Bitcoin miner today. None of them address an environment where multiple parties are using Grover's algorithm to mine.

This culminated for me in [a recent interview](https://www.bankless.com/podcast/will-quantum-computing-kill-bitcoin-scott-aaronson-justin-drake) of [quantum computing luminary Scott Aaronson](https://en.wikipedia.org/wiki/Scott_Aaronson) by the blockchain media company Bankless. The tagline of [Aaronson's blog](https://scottaaronson.blog/) is "quantum computers won't solve hard problems instantly by just trying all solutions in parallel". Surely this is someone who can elucidate the subtle issues behind this futuristic concept.

Unfortunately, while Aaronson does better than everyone else, he still gets a key point wrong. He [says (at around the 1:18:32 mark)](https://youtu.be/5DRDjeMmOPw?si=tN3-R0J-hLKePhRB&t=4708):

> ... if you got to a world where just about everyone had access to a quantum computer then it’s kind of amusing what would happen, which is that the proof of work just has its hardness just set automatically based on how much mining people have been able to do recently, and so all that would happen would be that pre-images would have to satisfy an ever more stringent condition, and the proof of work would automatically just be made harder to compensate for Grover’s algorithm, and we would all just be back where we started

The presence of all these misconceptions is unfortunate, because the consequences of Grover's algorithm for mining are actually quite interesting, both as an object of academic study, and in terms of their consequences for the long-term viability of proof of work. I'm making this post to set the record straight by explaining why all of these claims are wrong, and to explore some consequences of Grover's algorithm for mining through the lens of a few papers.

## Overview of Grover's Algorithm in simple terms

I'll start by explaining what Grover's algorithm is and how it works. This is a very high-level overview, and I'm not going to go into the matrix algebra or the quantum gates that are used to implement it - I think that focusing on that stuff scares off a lot of classical computer scientists who could otherwise understand and study the consequences the algorithm perfectly well.

Grover's algorithm is an "unstructured search algorithm". This means it's an algorithm useful for finding answers to what you might think of as "NP" problems. You provide Grover's algorithm a description of an algorithm for checking if a solution to a problem is correct, along with a set of possible solutions to a problem. You turn the crank, and after some time you get out a solution. In the context of proof-of-work mining, the problem we are answering is "does a particular nonce lead to a valid bitcoin block".

To go into more detail, Grover's algorithm provides two affordances that you can use to act on a quantum register:

1. **Applying a "Grover Iteration"**. This essentially the "turning the crank" operation. It doesn't provide any information on its own.
2. **Opening the register**. This has a chance of giving you a solution to the problem. The probability of a success depends on the number $k$ of Grover iterations applied, according to the formula $$ \approx \sin^2((2k+1)/\sqrt{N}) $$ where the fraction of possible solutions that turn out to be solutions is $1/N$. This action also resets the register, leaving it as if zero iterations had been applied.

\footnote{On some level, I think calling this an "algorithm" is misleading, you can imagine situations where you would want to "turn the crank" for a while, pause, turn the crank some more, and even turn the crank in reverse, and then open the output. I'll discuss this more in a future post.}

The key feature of these affordances is that the probability of success with Grover's algorithm goes up quadratically with the number of iterations. By applying $k = \frac{\pi}{4} \sqrt{N} = O(\sqrt{N})$ iterations, we get a probability around 1 of successfully solving the problem. By contrast, if we were attempting to solve the problem with a classical computer by trying solutions until one worked, we would expect to need $N$ attempts.

## [Conditions for Advantageous Quantum Bitcoin Mining](https://arxiv.org/abs/2110.00878)

For context, the current (February 2025) number of hashes needed to mine a Bitcoin block is $N = 5 \times 10^{23}$. So if we had a quantum computer which could run Grover iterations at the same rate that a classical computer ran hashes, we would expect the quantum computer to mine a block almost a trillion times faster!

But this view somewhat oversells the quantum advantage here. A key consideration is that even if a quantum computer mines an individual block a trillion times faster than an individual ASIC or ASIC core, this might still take hours or weeks or years to finish. If so, it will be useless to compute the block to completion because by the time we finish, our block will be stale.

The practical thing to do, therefore, is to stop the Grover process _early_ so we can take advantage of what iterations we can complete before it's too late. But this opens up a host of other questions, about the parameter of this process. Luckily, there is a nice paper by Nerem and Gaur that provides some answers, which I will now relay:

### How long should I compute Grover iterations before opening?

16 minutes.

Or, in general, about 1.6 times the average block time of the blockchain in question. Surprisingly, does not depend at all on the clock speed of the quantum computer in question!

### How fast/cheap does quantum computing need to be to make it more profitable than normal mining?

Clearly the faster and cheaper the better. But this also depends on the block time

The answer is, in natural language, that the quantum computer is cheaper if a single grover iteration costs no more than $r/\lambda\_0 \cdot 2.59$ times what a classical hash costs, where $r/\lambda_0$ is the number of iterations the miner can complete in one block time.

<!-- Mining is therefore not "progress-free": It is better to work on a state which has already been worked on for some time before rather than a new state.

1. With Grover's algorithm we cannot see if we have succeeded when we apply the update. We have to choose whether or not to measure, and if we measure and fail, all our work is undone. -->

## [On the insecurity of quantum Bitcoin mining](https://arxiv.org/abs/1804.08118)

I have left out from the discussion of the paper above, perhaps you've noticed it: In discussing the under what circumstances a Grover measure should continue to iterate or open, we have left out what happens on the blockchain in the meantime. As it turns out - the implication are massive for security. I'll switch now to an earlier paper by my colleague Or's discussing this.

### Consequences of opening blocks in response to new blocks

When a new longest-chain Bitcoin block is released, a classical miner is incentivized to stop working on their previous block and start working on the new one, because any blocks built on top of the new one will themselves then be part of the longest chain, and likelier to be eventually confirmed. But with Grover, the functionality of the "opening" facility complicates things. If a miner is to stop working on their Grover block due to a new block coming over the network, they might as well open the register they have immediately. If they do, there is a chance they will find they succeeded!

At this point the miner is now massively incentivized by the possibility of their block becoming valid. They will likely respond by mining on this block themselves, and releasing the block to the bitcoin network in the hopes that others will mine on it as well. Since they are doing this in response to another block appearing, if they are well-connected in the computer bitcoin network, there might even be a good chance that many nodes will receive their block first! And even more worryingly, if they are well-connected in their business relationships with other miners, they might directly bribe other miners to mine on their block.

Incentives for this kind of collusion bring the fundamental assumptions of the fairness and decentralization of Bitcoin mining into question. A key point is that while it's possible to have a stale block in classical bitcoin mining due to network delay, these are very infrequent, and their rarity removes a lot of the incentive to collude.

### How much higher is the stale rate in a world of quantum miners?

Or's paper calculates the stale rate, the ratio of blocks released after an already mined block on the same height, under the assumption that all miners are quantum and plan to measure after time $t$. The formula is

$$ p\_{stale} = 1 - \frac{t}{\ln(1/(1-t))} $$

Where $t$ is in units of block times.

![Image of the stale rate for different measurement times](quantum-stale-rate.png)

Or proposes the mitigation that blocks should be penalized for arriving too long after they were expected to, but this has the drawback of making the fork choice rule no longer a pure function of the chain state.

## [Strategies for Quantum Races](https://drops.dagstuhl.de/opus/volltexte/2018/10144/pdf/LIPIcs-ITCS-2019-51.pdf)

A critical part of the analysis of Bitcoin is showing that miners are incentivized to build on the longest chain. What can we say about how miners would behave under this regime?

For one thing the assumption that all miners will choose to measure at a predetermined time seems unlikely. If this were the case, a clever miner could measure marginally sooner, and have about the same chance of mining a valid block with a much higher chance of mining first. ["Strategies for Quantum Races"](https://drops.dagstuhl.de/opus/volltexte/2018/10144/pdf/LIPIcs-ITCS-2019-51.pdf) is a little more in depth, but only analyzes the one-shot setting, not the possibility of miners restarting when they measure an invalid block.
