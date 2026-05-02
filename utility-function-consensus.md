
# Utility Function Consensus


<!-- 

This is an old post/notes file perhaps related to my performal methods post. I add it for context/linkability.

---
title: "Utility Function Consensus"
date: 2021-06-26T23:04:46-04:00
draft: true
tags:
    - blockchain
    - cryptocurrency
--- 

-->


## The Tradeoffs of a Cryptocurrency

A cryptocurrency has a variety of goals conducive to its usefulness:

1. Transactions are confirmed quickly
2. Transactions aren't costly for users
3. The currency doesn't inflate too much (or too little!)
4. Network, storage, and compute requirements of (archival/full/light) nodes are minimal
5. The chain is secure against (51%/34%/x%) attacks

In order to meet these goals, there are a few parameters that the protocol must set. And indeed, they must be set carefully, since increasing or decreasing the parameters will have salutary effects on some goals while having detrimental effects on others. These parameters include:

* Block Reward (increasing improves security, but causes inflation)
  * With EIP1559, you could also think of this as fraction of transaction fee burnt
  * Uncle reward is also important in some models and has the same tradeoff
* Block Rate (increasing helps confirmation speed, but hurts security)
  * This is usually controlled indirectly through difficulty in PoW chains.
* Block Size (increasing helps confirmation speed, hurts compute requirements)
* Transaction fee (increasing improves security, hurts user experience)
  * Base fee per transaction or per gas
  * Sales-tax-style percentage of transaction amount fee (more on this [below](#sales-tax-style-fees)).

There are a variety of factors that influence the optimal setpoint for the parameters:

* The supply curve of hashrate on the network
* The demand curve for transactions of various amounts
* The speed of block propagation at different block sizes

But vexingly, these factors aren't known before the genesis block, and they might change over time as the blockchain gains adoption and goes through "hype cycles".

## A Utility Function Approach

The broad approach I am proposing here is to optimize the parameters directly over a utility function over the five goals I mention. This is a somewhat similar idea to the [EIP-1559 AMM idea](https://ethresear.ch/t/make-eip-1559-more-like-an-amm-curve/9082), but I am trying to take it a little further to extend this to all of the parameters the chain sets.

This would work by defining a model of blockchain usage, and expressing the effects of that model in terms of what we can detect programmatically on the chain. We then predict factors like supply and demand based on what we see and compute optimal values for the parameters.

### Modeling Block Supply and Demand

We could estimate the blockspace/gas demand curve by doing a regression (perhaps linear, perhaps more complicated) on the frequency of transactions against their sizes and the amount of fees those transactions pay. Note that if the weight of the data from $k$ blocks ago in the regression decreases exponentially in $k$, the regression parameters can be updated in constant time.

For Proof-of-Work chains, we could estimate the hashrate supply curve by a similar regression on the estimated hashrates against the reward/difficulty ratio.
One thing to be careful of: Estimating the hashrate requires knowing the block time, so time warp attacks might occur if there are incentives.

We could estimate the speed of block propagation through the uncle rate.

### What would the utility function be?

Here are some utilities you could impose:

* A utility on the block reward of `-k/(max_reward - block_reward)`, where `max_reward` is a specific fraction of the [total unminted coins](./smoothing-the-halvening-and-the-unminted-pool.md). This utility reflects the philosophy popular on Bitcoin twitter that the issuance rate should have an absolute limit (in that the utility approaches negative infinity as the reward approaches the limit). It also espouses that lower inflation is better and that controlling inflation is more important when we are near the maximum amount of issued coins.
* A utility on the mine time of the next block in the form of `-(mined_time - target_time)^2`. The utility of a given hashrate is then given by the expectation of this value when the mined time is distributed exponentially according to the hashrate. This reflects the philosophy that blocks should be published regularly. It also allows us to _truly_ target a block every ten minutes, in the sense that the $n$th block is targeted $10n$ minutes after genesis, rather than just each block ten minutes after the previous. This way, you can better predict the approximate timing of blocks long term.
* Coin holders could vote on the relative value of security and non-inflation (median voter wins, votes allocated in proportion to worth). Thus, instead of a fixed economic policy, you get an oligarchic economic policy. This approach enjoys a similar argument to that in favor of Proof of Stake: Those with the most money in the system are the most incentivized to keep the system stable.
* We impose a cost of some kind on the average hashrate being too low/below some bar, representing the minimum necessary hash power to launch a 51% attack. There are a few ways one could set this - there could be a fixed cost, coinholders could vote, or we could allow merge-mining to try to determine the world-wide hash rate and base the penalty on that.
* We remove the block gas limit (or as in EIP 1559, set a `block_size_target` lower than some absolute limit) and impose a cost on the amount of time a validator lags behind if they can process only `block_size_target` gas per block time. This has the potential nice effect of incentivizing delaying the next block a little after a *really* full block comes, so that everyone has time to process.

## Sales Tax Style Fees

Above, you noticed that I mentioned the possibility of including fees that scale as a percentage of the size of the transaction. This is impossible in smart contract chains due to the possibility of wrapping the main token. As for pure-cryptocurrency chains, I am aware of none that do this. I think much of the cryptocurrency community just rejects this idea out of hand, in favor of the simpler narrative of "A form of money equally accessible to everyone, regardless of wealth".

But I think that ignoring this idea of including a percentage fee, or more broadly, a fee that changes with the size of the transaction, leaves a lot on the table in terms of what blockchains could be as an economic system.

I am not an economist but bear with me as I act like I am. I think it's reasonable to say that higher-amount transactions are naturally made more often by wealthier people. Since these people are richer, one thing we could say is that for them, the marginal value of money is less. Furthermore, the more money a transaction sends, the more important it will be that that transaction is secured properly in way where it is unambiguous when the transaction has gone through. These factors should be reflected in a higher (per-throughput) demand for management of higher-amount transactions, which means the fees should be higher.

This is borne out in my understanding of everyday finance. If I pay $5 cash for some tacos, then there are no fees. If I have to pay a $40 bill with a credit card, my bank will charge me some fees to maintain my account. If I wire money internationally, there is a larger fee and presumably I try to make these transactions as big and infrequent as possible. If a financier trades a large amount of securities, they pay a clearing house fees to settle that transaction that [change based on the size](https://www.theocc.com/Company-Information/Schedule-of-Fees).

So what would be the effect of charging a percentage fee in a cryptocurrency? Would the extra price for higher-amount transactions scare these users away, making the total number of transactions go down, and destroying the ecosystem by making it unpopular? I would argue not, especially with the other recommendations in this post: The chain can still process the same amount of transactions, so when the fees of the higher-value transactions increase, the additional revenue supports the security of the chain, *allowing the base level transaction fees to go down*. The result would be that it would become easier for non-corporate entities to use blockchain.

The ultimate effect is more in line with my sense of the spirit of blockchain: It exists not as a way for businesses to make more profits, but as a social movement to give regular people more control over their finances.
