# Sampling certified primes

Suppose you want to sample a prime number uniformly at random from all primes less than some large $N$. How might you go about this?

One approach would be to sample positive integers at random from $\{1, \dots, N\}$, testing each with the Miller-Rabin test, until you found a number that tested as prime. This would be sufficient for most practical purposes. But there is a chance this could return a composite, so we technically do not meet the precise terms of our specification. And even if we do return a prime, we will have no proof that we have done so. 

We could replace Miller-Rabin with AKS. Then we could prove any numbers we return will be prime, (and once we have returned a prime, we can produce a "proof" of its primality in particular in the sense that we can just provide the number and tell a verifier to use AKS to check it). But this would take $O(n^5)$ or $O(n^6)$. Even if we are clever and do an initial Miller-Rabin test followed up by AKS to speed up generation, we are still experiencing an expected $O(n^5)$ time testing procedure.

The goal of this post is to try to find a procedure that faster or at least quickly certifiable, based on some other ideas in computational number theory.

## Two related ideas

My approach is based on two ideas, which I now summarize:

### ["pre-factored" numbers](https://www.cs.cmu.edu/afs/cs/user/akalai/genfactor/web/factor/factor.html).

If our task had been, rather than to sample a random *prime* less than n, to sample the prime factorization of a random *natural number* less than n, the naive approach of sampling a random number and then attempting to factor it would not run in expected polynomial time. Nevertheless, there is a way to accomplish this task in polynomial time using a clever and simple procedure of Kalai (some other guy, Bach, did it first and better, but less simply, so I'll ignore that). 

Roughly - we first sample a list where the first element is a random natural less than $N$, and each subsequent number is a uniformly random natural no more than the previous. We then multiply the primes in the list we sampled. This does not give us a uniform distribution, or even a distribution supported on numbers $\le N$, but it is possible to use rejection sampling to correct this.

This of course requires a primality test. As above, this could be Miller-Rabin (and hence probabilistic), or AKS (and deterministic but compute-intense).

### [Pratt primality certificate](https://en.wikipedia.org/wiki/Primality_certificate#Pratt_certificates) 

A [relatively simple theorem in number/group theory](https://en.wikipedia.org/wiki/Lucas_primality_test) tells us that it is possible to prove a number $p$ prime given the prime factors of $p-1$ (and proofs that the elements of that factorization are indeed prime). Applying this concept recursively, one can produce a proof that $p$ is prime by providing 

* The prime factorization of $p - 1$
* The prime factorizations of $q_i - 1$ for each $q_i$ in the prime factorization of $p$.
* The prime factorizations of $r_{i,j} - 1$ for each $r_{i,j}$ in the prime factorization of $q_i - 1$.
* And so forth

In fact, this tree of primes will contain polynomially many elements, so this fact is a (simple) proof that Primality is in NP. But note that this on its own doesn't give us a quickly verifiable generated prime because we still can't generate a Pratt certificate for a uniformly sampled number in polynomial time.

## Putting these together: Pre-Pratt-Certified Numbers

Inspired by these, we ask two questions:

**Question** Is there an expected polytime procedure for sampling a (prime, Pratt certificate) pair uniformly at random?

**Question** Is there an expected polytime procedure for "pre-Pratt-certified predecessor factorization" which, given input $N$, returns a number $M$ uniformly at random from $\{1, 2, \dots, N\}$, along with a Pratt certificate for every prime in the factorization of $M-1$ (as long as $M$ is not itself 1)?

(Exercise: Show each implies the other)

Here's an attempt for pre-Pratt-certified predecessor factorization based on adapting the above procedure as closely as possible.

1. As in Kalai's procedure, we will sample a list of decreasing numbers, starting with $s_1 \gets \{1, \dots, N-1\}$.
2. However, rather than simply sampling $s_{1}$ and subsequent $s_{i+1}$ with a generic uniform random number sampler, we will sample with a recursive call to the "pre-Pratt-certified predecessor factorization" procedure.
3. Now, when we take the product of the primes in the list, we have Pratt certificates for all of them.
4. Rather than returning the product itself as the top-level number, we return the product plus one (we slightly modify our rejection sampling to accomodate this)
5. The Pratt certificates of the listed primes together constitute a Pratt certified factorization of the returned value.

## Time complexity

How long does this procedure take?

First we analyze the pre-Pratt-certified numbers procedure. Let $T(n)$ be the expected time taken to run the procedure to sample an $n$-bit number, and let $P(n)$ be the time to check the Pratt certificate of an $n$ bit number.

* Doing some rough and possibly-incorrect hand waving, each $s_i$ has approximately one less bit than the previous, so the time to sample a list is something like $\sum_{i = 1}^{n-1} T(i)$
* For each $s_i$ we must check the Pratt certificate to determine primality, so we have $\sum_{i = 1}^{n-1} P(i)$
* We expect to have to sample a list O(n) times due to resampling, as in Kalai's original algorithm

So we have the recurrence

$$ T(n) \le c * n * (\sum_{i = 1}^{n-1} T(i) + \sum_{i = 1}^{n-1} P(i)) $$

Unfortunately, this is exponential time, since even $T(i) = T(i-1) + T(i-2)$ is exponential.

## Can this be saved?

Can we save this? Brain dump time.

The key issue seems to be that we are calling the procedure recursively on multiple numbers of about the same size as the input. Let's try to avoid this.

### Avoiding recursing on composites

Most numbers in the list will be composite and therefore we don't need to have certificates for them. How can we modify our procedure to avoid recursing on composites? 

Unfortunately it's not as simple as saying "if the number we sample is composite don't compute the Pratt certificate for it" - we only learn what the number we are sampling is after we take the product and add one, when the certificate has already been constructed.

But perhaps there is a way we can nonetheless avoid computing certificates for composites. Rather than sampling a Pratt-certified number uniformly at random, we can first decide whether the number we sample should be prime or composite, and then only sample the print certificate if it is prime.

In order to make the decision whether it should be primer prop composite it would be ideal to know the probability that a given number less than as I prime. But actually we don't exactly need to know this. We can simply  sample a random number test it for primality the traditional way i.e. using ks. Then we can throw that out and proceed to sample either a prime (Pratt-certified, by recursively running the sampling procedure until we get a prime), or a composite.

This actually doesn't help us much, since while we aren't recursing on composites, when we do need a prime we have to do lots of Pratt resampling until we get one, so the number of resamples is about the same. Nevertheless, this feels like an interesting and potentially useful manipulation.

### Avoiding work when a resample is inevitable due to exceeding the bound

Clearly if we generate a prefix to our list with a product greater than $N$, we will throw out the sample and retry. We can identify when this happens and avoid any additional work on the sample.

In order to complete this short-circuit, it seems like we will have to sample at least two certified primes, which isn't ideal.

We can avoid this by a similar procedure as before. Rather than sampling a number to determine if it's prime or composite, determine wherther its 

1. "PRIME NOT SUFFICIENTLY LARGE TO CAUSE RESTART"
2. "PRIME SUFFICIENTLY LARGE TO CAUSE RESTART", 
3. "COMPOSITE".

This way, we avoid Pratt sampling in all but the first case, and it's now possible to quickly restart a sample after only one Pratt prime has been found

### Avoiding resampling due to rejection

There is also a condition in the Kalai procedure which says that even if we are successful in generating a number $r$ below $N$, we still resample with probability $r/N$ no matter what. How can we short circuit these resamples?

Fitting in with an emerging pattern, let's try to come up with a solution along the lines of this short circuiting. Notice that we can actually do this not just with the sampling of the next value, but with the whole list.

1. Drop a checkpoint
2. See if a simulation causes us to restart,
3. If not, do it for real, returning to the chekpoint until we succeed 

resample with probability $r/N$ is equivalent to "choose x uniformly in 0,1 and resample if r/N is less than this". The first thing we can do is move the sampling of this x to the beginning of the list construction procedure, so that we now know we will resample unless the final result is in a particular range.

So far this doesn't help us much, since if our current total is below the range, there is always the chance that later primes could increase it.

Perhaps instead of constructing the list from high to low, we could constuct it from low to high? Is this even possible? Perhaps we could arrange to pre-decide how many k-bit primes there would be for each k in the factorization?

### Bach's test

I have been trying to avoid reading the [Bach paper on the more efficient algorithm](https://pages.cs.wisc.edu/~cs812-1/pfrn.pdf) because it's very dissappointing to me that you have to x15 the page count to do better. But perhaps this could yield an insight?

### Pocklington

There seems to be a variant of the test called the [Pocklington test](https://en.wikipedia.org/wiki/Pocklington_primality_test) that only requires a single recursive certificate. Could this be used?

## Concluding thoughts

While these ideas are interesting, I am ultimately not optimistic. It seems like the key problem is that a lot of numbers have prime factors with only a few fewer digits, and so we have to be ready to construct a chain of these that such that when we multiply each by its lower facotrs and add one, the next value up the chain always coincidentally turns out prime.

Let me know if you have any ideas to fix this!

