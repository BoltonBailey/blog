# Thoughts on Condorcet Methods

In an election where each voter ranks a list of candidates in order of their preferences, a [_Condorcet Winner_](https://en.wikipedia.org/wiki/Condorcet_method) is a candidate who would head-to-head against each other alternative.
Interestingly, it is [not always the case that a Conderocet winner will exist in such elections](https://en.wikipedia.org/wiki/Condorcet_paradox).
Nevertheless, this concept is compelling and has been generative in the field of social choice theory.

## Minimax Condorcet method

An appealing politco-philisophical reason for wanting a Condorcet winner is that in any election, the alternative candidate who did the best head-to-head against the winning candidate can become the focal point for dissatisfaction with the winner's government.
This is particularly destabilizing when this set of dissatisfied people is in the majority, because of the sense that the government is opposed to the people at large, and if conditions are bad enough, it could open the possibility for rebellion.

But, given the reality that it is not always possible to elect a Condorcet winner, we can still try to do the "best possible".
With this framing, I think the most natural procedure becomes: Choose the candidate that minimizes the maximal possible size of the set of voters who would rally around any one other candidate.
Put another way, we choose the candidate that minimizes the "Condorcet vulnerability factor" where the Condorcet vulnerability factor of a candidate A is the maximum, over all other candidates B, of the margin by which A would lose to B head-to-head (so A is a Condorcet winner if the Condorcet vulnerability factor is negative)

It seems this system exists and is fittingly called [the Minimax Condorcet Method](https://en.wikipedia.org/wiki/Minimax_Condorcet_method).
Unfortunately, it apparently fails a number of other desirable criteria for voting systems.
But this nevertheless seems like a principled approach, and I would like to see it explored more.

## The Smith Set

Perhaps the fact that Condorcet winners don't always exist is part of the reason that "Condorcet methods" sometimes feel a bit contrived - Any Condorcet method has to specify what should be done in the case that a Condorcet winner doesn't exist, at which point we might start asking ourselves why we aren't just using that method to begin with.

A nice generalization of the concept of Condorcet Winner is the [_Smith set_](https://en.wikipedia.org/wiki/Smith_set): The smallest set of candidates that beats all candidates outside the set.
If you think of the set of head-to-head races as a directed ["Tournament" graph](https://en.wikipedia.org/wiki/Tournament_(graph_theory)) where a Condorcet winner is a terminal node, then the terminal node of the [condensation](https://en.wikipedia.org/wiki/Strongly_connected_component#Definitions) of this graph would comprise the Smith set.
Happily, this means that the set will always be nonempty, so there is no "Smith paradox" - we can choose voting methods that always choose a candidate from the Smith set.
But unhappily, the same problem arises, because the Smith set can have multiple members and we are now forced to decide on a mechanism for choosing between them.

Here's a potential solution: The Smith Set "tournament" graph evokes a two-player game like rock-paper-scissors or rock-paper-scissors-lizard-spock where there are a number of options, each of which wins and loses against each other option.
One might think of this as a game between powerful binary opposing interests who each wanted to choose a candidate to back, not knowing who their counterparty would choose, where the two candidates chosen will eventually go head-to-head to decide which interest should win out.

Such a game must have a Nash equilibrium, which suggests the idea of deciding the outcome of the election on the basis of a random draw from such an equilibrium.
This would have the nice property of always choosing a candidate from the Smith set.
And practically, if we lend creedence to the view that games like the opposing-interest game do play out behind the scenes in normal politics, then this scheme has the virtue of being structurally similar to the existing system, but with the corruption-like element removed.

A downside of this approach is that if we had stereotypical Condorcet paradox reweighted 49%/26%/25% this would still give 33% to each candidate to win.
Perhaps a variant of the approach where the payoffs are the vote margins would work better?

## IRV With 1 Dimensional Voters

The [Median Voter Theorem](https://en.wikipedia.org/wiki/Median_voter_theorem) assumes voters exists on an ideological spectrum, left to right, and will rank the candidates according to ideological proximity.
This being the case, the theorem shows that the candidate closest to the median voter will be a Condorcet winner.

*Proof* This candidate must beat all candidates to their (left/right) head-to-head, since they will get the votes of all candidates to the (right/left) of the median, plus the median herself.

Given that in this important, simple model does *not* experience the Condorcet paradox, it's worth asking whether common voting schemes always elect the Condorcet winner under the model's assumptions.

Infact the answer is: Not always!
[IRV sometimes fails to elect the Condorcet winner here](https://en.wikipedia.org/wiki/Condorcet_method#Comparison_with_instant_runoff_and_first-past-the-post_(plurality)).

## Further Questions

- The classic Condorcet paradox example shows that in an election with three candidates, the "Condorcet vulnerability factor" of the minimax Condorcet candidate can be as high as 1/3.
  - Is this different with a larger number of candidates?
  - For other voting methods, what is the largest Condorcet vulnerability factor of a candidate that method can choose?
- What variants of the Smith game are there?
  - One radical aspect of this proposal is that it randomizes the winner, so replacing the random sampling with the highest-probability option of one approach, but I like the idea that that this version might somehow encapsulate the notion behind various impossibility theorems that suggest strategic voting is sometimes unavoidable.
  - [Do games like these always have Unique Nash Equilibria](https://mathoverflow.net/questions/506372/can-a-tournament-game-have-multiple-msne)?
    If not, how should we choose a specific one to use?
- What other voting methods can fail to choose the Condorcet winner under the assumptions of the MVT?
  - What about other models of electorate preference, like a 2-dimensional ideology space, or the ideology-quality model from [this](https://isps.yale.edu/sites/default/files/files/di-pb-2-3-23-v3.pdf) paper?
    - Do these models always have a Condorcet winner?
    - Which voting methods always choose it, or always choose it when it exists?
    - If it doesn't exist, what Condorcet vulnerability factors are possible?
