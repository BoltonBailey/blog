
# [Futarchy would be better with combinatorial markets](https://thequantummilkman.substack.com/p/better-futarchy-with-combinatorial)

[A](https://dynomight.net/prediction-market-causation/) number of ([old](https://dynomight.net/prediction-market-causation/) and) [recent](https://dynomight.net/futarchy/) [blog](https://www.overcomingbias.com/p/decision-conditional-prices-reflect) posts and [manifold](https://manifold.markets/BoltonBailey/futarchys-fundamental-flaw-the-mark) [markets](https://manifold.markets/Tumbles/futarchys-fundamental-flaw-the-mark-d9LsnOnzhI) [have](https://manifold.markets/Tumbles/futarchys-fundamental-flaw-the-mark-OR85qIqIcN) [come](https://dynomight.net/futarchy-market/) out debating the [efficacy](https://news.manifold.markets/p/experiments-with-futarchy) of [Futarchy](https://mason.gmu.edu/~rhanson/futarchy.html).

This post will address none of these! Instead, I'll cover some thoughts (originating mostly in Manifold discord discussions dating a few years back) about what I think is likely a strict improvement to futarchy as it is almost always presented. Namely: Rather than using prediction markets that replace the "called-off"/"reverted"/"N/A" bets with a combinatorial market over the decision and outcomes.

## Futarchy as it is usually explained

Here is an explanation of futarchy (really it's an explanation of "decision markets", which I think is the right term for the decision making mechanism behind futarchy).

We have a decision to make, let us suppose there are two choices and each choice can either lead to a good or bad outcome (you could imagine more choices and a larger spectrum of outcomes, but this is simpler to explain. All the ideas in this post can be generalized to other settings). We want to maximize the chances of getting a good outcome.

We make two prediction markets

* The first market will:
  *  Resolve YES if option A is chosen and we get a good outcome.
  *  Resolve NO if option A is chosen and we get a bad outcome.
  *  Resolve N/A if option A is not chosen, meaning all trades made in the market will be undone, as if they had never happened.
* The second market will:
  *  Resolve YES if option B is chosen and we get a good outcome.
  *  Resolve NO if option B is chosen and we get a bad outcome.
  *  Resolve N/A if option B is not chosen.

Thus the first market price reflects the probability of getting a good outcome if A is chosen 
and the second market reflects the probability of getting a good outcome if B is chosen.
We therefore choose according to which market has a higher price/probability (either averaged over some window, or at a specific time)

## The issue with N/A resolutions

The issue with this design is the part where we undo all trades in the market for the option that isn't chosen.

To see why this is a problem, or at least more complicated than it appears, consider the following scenario:

1. You think option A is underpriced, so you put €50 on the platform to buy 100 shares of YES at 50%.
2. The rest of the market comes around to your point of view. The probability of a good outcome for option A goes up to 75%. Yay!
3. You sell your 100 shares for €75.
4. You withdraw the money from your account, and buy yourself something nice with the €25 you profited.
5. Option B turns out to be priced even higher, so option A resolves N/A.

At this point, the market has a problem. It's supposed to undo all the trades made on market A, which should mean making sure that the profit you made is reverted. 
But you have already left the building! Now the prediction market has to find someone to go out and break your kneecaps to get you to return the money.

More seriously, the upshot of all this is that the platform can't let you cash out your profits, or use them to bet on other markets, until the decision is made. 
This restricts the usefulness of your holdings and makes you less likely to trade on the markets in the first place.

## The better option

But this is unnecessary. Here's an alternative market design for futarchy based on a single market with four linked share types.

* The first share type pays out if decision A is taken and we get a good outcome
* The second share type pays out if decision A is taken and we get a bad outcome
* The third share type pays out if decision B is taken and we get a good outcome
* The fourth share type pays out if decision B is taken and we get a bad outcome

### But now that we don't revert the markets, how will we know what the conditional probabilities are?

Using the law of conditional probability! 

$$ P(Good | A) = P(Good \& A)/P(A) $$

Really this is just how conditional probability is defined in the first place: 
The probability that we get a good outcome given that we choose A 
is just the probability of choosing A and getting a good outcome, divided by the chance that we choose A at all.
The probability that we choose A and get a good outcome is the probability given by the first share, 
and the probability that we choose A at all is the sum of the probabilities of the first two shares.
Therefore, we can caluclate the conditional probability and use it just as we would in normal futarchy.

### But what if I want to make a trade that pays out like the conditional markets do?

You can still do that!

Let's say that that we're in the situation from step 1 above: 
The conditional probability of a good outcome given A is 50% according to the market, 
and you want to spend €50 making it higher, but you want to do this in such a way that if option B is chosen, you don't have any profit or loss.
The first thing to do is to buy 50 shares each of share types 3 and 4. This costs less than €50, since the probabilities of outcomes 3 and 4 can't total 100% or more, and it guarantees you'll be left with what you started with if option B is chosen. Then, you simply spend what remains of your €50 on shares of the first type.

Because all of this is done on a computer, the computer can even simulate for you what the outcome will be, so that you can get exactly the same user experience as if the market were conditional.

### What advantage does this have that we don't get by conditional markets with locked-in profits?

Let's continue the thought experiment above.

1. After your initial buy of "Good conditional on A" You have 50 shares each of (B, Good) and (B, Bad), and 100 Shares of (A, Good).
2. Again, the rest of the market comes around to your point of view. The probability of a good outcome for option A goes up to 75%.
3. You again sell shares as if you were using conditional markets. 
  * In the scenario above, you sold 100 YES shares in A at 75%, which is equivalent to buying 100 NO shares at €0.25 per share.
  * So the analogous thing to do is to spend €25 to buy 25 more shares each of (B, Good) and (B, Bad), and also 100 shares of (A, Bad)
4. Thus you now have 75 shares each of (B, Good) and (B, Bad), and 100 shares each of (A, Good) and (A, Bad)
5. As is usual in prediction markets, you can redeem a complete set of shares for €1. So you do this x75, and so you get back all of the €75 you put into the market, and you still have 25 shares each of (A, Good) and (A, Bad)

So there's a few benefits over the locked-in profits approach: The first is that you are able to cash in at least some of your shares (though technically the locked-in profits model could be implemented smartly enough to let you withdraw the minimum of all amount you would be able to withdraw under all future scenarios).

But more tellingly, the benefit is that your long position in A shares is now tradeable. If you think the probability of A being chosen is overpriced, you can sell that position without further need to add money to the system. Or if you don't have a strong opinion about what decision will be made, but you trust that the market is efficient, you can sell your position at market price to reduce your risk.

### What are other ways to frame the benefit of this approach?

Another way you could think about this is that it allows more general flexibility in how you express your needs to the market.

For example, it's not often talked about, but one source of liquidity for futarchic markets could be individuals who have a more direct stake in the decision and its outcome than the typical trader. Indeed, many government policies are important to groups that they affect directly. you could imagine that there's a trader who would be especially distraught to see the market choose option B and simultaneously get a bad outcome (perhaps they are part of the group it is speculated policy B would most hurt, if it goes wrong (we could even make separate arbitraged  markets on the parts of welfare sustained by different groups to better capture this)). That trader could hedge their risk by buying shares in the possibility that this would come to pass. But why should we force them to implicitly take a long position in outcomes in A in order to be able to?

## Open question: Details on how liquidity changes

My examples above tries to be as clean as possible in showing the analogies between the two different market structures. The main difference with the combinatorial market is that it allows trades directly on the likehood of decisions.

Could this be a bad thing in some cases? If one option is obviously much better than the other, perhaps it is also obviously more likely to be chosen, which could lead to less available liquidity in the market shares for the alternative. I think this is hopefully not too much of an issue if the liquidity provision is designed carefully - in the worst case we could partially simulate the liquidity structure of the conditional markets by setting up separate automated market making mechanisms trading the conditionals and then arbitraging them against the main markets. It's worth noting that even if the prediction platofrm itself doesn't allow trades on decisions, a black market could spring up to take this liquidity anyway.

Maybe it's actually actively bad to spread information about how low the likelihood of one outcome is, precisely because it will cause people to see that correcting prices on that conditional will not be profitable. But yet again, maybe it's better to have this happen than to have only traders who are not sophisticated enough to estimate this chance accurately for themselves be the dominant forces in that market. 

In any case, I would like to see more experimentation with futarchy structured this way.

