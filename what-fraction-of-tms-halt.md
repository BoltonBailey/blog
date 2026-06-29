# What fraction of TMs halt?

Here are some markets:

Links:
- https://manifold.markets/IsaacKing/what-fraction-of-turing-machines-im-f038c705880f
- https://manifold.markets/BoltonBailey/what-fraction-of-turing-machines-im-2e5fae714293

The above markets ask variants of the question "as the number of states in a Turing machine increases, what fraction of machines halt?".
Here are my thoughts.

## Which models are interesting?

Clearly the answer to this question depends on the model, and as people in [this Math StackExchange thread](https://math.stackexchange.com/questions/73187/density-of-halting-turing-machines) have shown, you can get the answer to be 0 or 1 for some models.
But these models seem slightly contrived to me (I am not used to the idea that a TM can "fall off the edge" of its tape).

Measures that seem natural where the question is open include:
\footnote{(I assume in this post that the tape symbols are binary with the tape infinite in both directions and initially all 0, but you could change these assumptions)}

1. (`TM-Model-A`) The uniform measure where there are (4(n+1))^(2n) TMs with n non-halting-states.
   (Every (state, head-symbol) pair returns a direction and symbol to write, **as well as** and halt or another state)
2. (`TM-Model-B`) The uniform measure where there are (4n+1)^(2n) TMs with n non-halting-states.
   (Every (state, head-symbol) pair returns **either** halt or a direction, symbol to write, new state)
3. (`TM-Model-A'`) TMs in model A, but where we form the digraph which maps all states to the set of possible next states, and remove any TMs that have states such that there is no path from the start state.
   (Clearly, such states aren't relevant to the halting status, which is why it is natural to ignore them, For example, bbchallenge.org removes such machines).
4. (`TM-Model-B'`) defined analogously.

This leads to some **Question**s, many of which are concrete:

- Does the limit exist for any of these?
- What are the liminf and limsup?
  Can we compute bounds on them?
- If the limit is 0 or 1, can we compute limit/liminf/limsup for asymptotic rate at which we approach?
- What relationships can we formulate between the limiting behavior of these models, even without specific bounds?
  - For example, `TM-Model-B` must be less likely to halt than `TM-Model-A`, because one can map `TM-Model-A -> TM-Model-B` by forgetting the motion and writings of halt transitions.
    This preserves halting, reduces the measure more the more halting transistions are present, which should correlate with halting probability.
- Can we come up with more general parametrizable models of which these are instances?

## On the Hamkins-Miasnikov 1/e^2 argument.

[This paper](https://arxiv.org/abs/math/0504351) has an argument that `TM-Model-A` has no incoming edges to the halting state with probability approaching $1/e^2 \approx 0.135$.
Thus, this is a lower bound on the fraction that do not halt.

One can adapt this to `TM-Model-B` to get $1/e^{1/2}\approx 0.606$ as a lower bound on non-halting.

### Pushing it further: More backtracking

One can also push it further: Considering the state digraph, clearly "the halting state is never referenced" is a subcase of "the halting state is not reachable from the initial state".
So we can argue that because each state has essentially a Poisson(2) distributed number of incoming edges (for large $n$), we never halt if the tree of incoming edges terminates at some finite level (except for the small probability that the initial state is in this tree, which goes to 0).
Some quick python code tells me that this gets us from 13.5% to about 20%.

**Question**: Is there a closed form for the probability that a tree where each node independently has Poisson(2) parents is infinite?
What about Poisson(k)?

### Pushing it even further: Halting trajectories

But we could also push it further than this: If there are limited incoming paths to halt, then perhaps many of them are impossible by reasoning about the state of the tape.
For example, if the written symbol at one point in the path contradicts the read symbol later in the path, then this trajectory can't be an incoming trajectory for a halt, and so we could exclude these as well.

[I vibe-coded a python script to investigate this](https://gist.github.com/BoltonBailey/78fd2f5f9be11fb0d44fb89c2650bf59), and got non-halting lower bounds of around 0.71 for `TM-Model-B` and 0.26 for `TM-Model-A` , (though in this case, the bounds are statistical).

## Further thoughts on the digraph

It seems to me that this state digraph is likely to have a [large strongly connected component](https://en.wikipedia.org/wiki/Giant_component) (of size a constant fraction of n) as n grows.

**Question** Can we confirm this?

If this is true, then it seems likely we can relate the primed models to the unprimed ones: The initial state is very likely to reach this component quickly, so most of our reasoning is about this component, and the question of the behavior of the model factors into a question about the likelihood that the halting state is in the component and the likelihood that a halt occurs if so.

It seems like in this model, the number of incoming paths is not distributed as Poisson(2), but rather 1 + Poisson(1), which has the same mean, but less variance.
It's hard for me to tell if this would be useful.

## Proofs of Halting

This is a lot of material proving lower bounds on non-halting.
Can we instead prove lower bounds on halting?

Perhaps a convenient way of reasoning about `TM-Model-A` to prove a bound like this is to pretend we don't halt on the halt state and that the halt state is just a state like any other.
We can then instead ask what fraction of states the infinite trace of the Turing machine execution visits (and the chance that it would have halted is just the chance that the "halt" state is in this set).

We can use this to prove that an $n$ state machine halts with at least $~ 1/\sqrt{n}$ chance, because the birthday paradox suggests that this is the fraction of states that are visited before any state is revisited (note that until we revisit a state, our next state is always uniformly random), and so we visit at least this many states in expectation.

Can we do better than this?
What happens after we revisit a state for the first time?
My intuition goes something like this:

1. When we revisit a state for the first time, we have visited $~\sqrt{n}$ states, and we have visited $~n^{1/4}$ tape cells, which now have random contents.
   We sit somewhere in the middle of these.
2. We may now do some replication of our previous trace from that state, but not for very long.
   This portion of the tape was likely overwritten with random bits since we last visited, and so we will soon visit the same state, but read a different bit.
3. This will take us back into the unvisited states for $~\sqrt{n}$ more steps, and we will probably overwrite everything we did while we were replicating our state trace from before, so we can again assume the tape is random when we next revisit a state.

So we can repeat this reasoning, but it's not clear how long before it breaks down.

<!-- 

Ok, here is my reasoning. consider an n-state machine, and consider the number of "k-step halting traces", which we define as 

a sequence of k (state, read symbol, direction) triplets, 

We will say that such a sequence is a valid halting sequence for a TM if there is a tape segment and a starting location on that tape, such that the sequence of (state, read symbol, direction) triplets is the sequence you get from executing the TM on that tape, starting with the first state and starting tape head symbol, and the seqence ends by halting.


In order for a machine to halt, a halting trace must be valid (except if the machine halts in under k steps, which is low probability as n to infty). 

~So for any n,k the probability that a n-state machine halts is at most the chance that an n-state machine halts in <=k steps + the sum over all c values, of the probability that there exists a k-step-c-cell halting trace.

There should be (4n)^k different traces. The probability that a trace is valid for a random TM (assuming N large enough that states won't appear twice) should be

* (1/n)^k for the chance that each state is indeed the following state from the last given the state transition function.
* (1/2)^k for the chance that each direction is indeed the direction given by the state transition function.
* (1/2)^(k-c), where c is the number of cells visited by the direction trace, because any time a cell is visited for a subsequent time after the first, there is a 1/2 chance that the previously written symbol at that location is not what the machine reads.

This leaves 2^c / (4n)^k, and I guess since (4n)^k is so big, this means we expect a number of valid traces like a poisson with mean 2^c.
 -->
