# Bit Commitment from Factor Counting

Here is a [cute website](https://www.rahulilango.com/coloring/) giving an intro-to-zk through graph colorability.

While the pedagogy of zero-knowledge is something I've thought about, I am most interested in this website for the [bit commitment](https://en.wikipedia.org/wiki/Commitment_scheme) primitive it presents at the end of the tutorial (EDIT: Sadly, seems it's been changed now). I'll describe it here in about the level of formality the site ~~uses~~ used:

**A bit commitment scheme (informal)**: To commit to the bit 0, choose two primes and multiply them together. To commit to the bit one, multiply three primes together. The product is the commitment. To open the commitment, provide the factorization.

## Making this a bit more rigorous

It is at least plausible to me that this informal description could be turned into an actual bit commitment scheme. As far as I know, there is no way to determine the number of prime factors of an integer in polynomial time (although I'm also not sure the hardness of this problem can be proven from the hardness of integer factorization itself). Still, the informal description above leaves a bit to be desired in terms of specifics, in particular in around how the primes are to be chosen.

Suppose that the primes were to be chosen independently and from the same distribution, no matter which bit we were committing to.
This would lead to leakage via the magnitude of the commitment: The average logarithm of the commitments to 1 will be about 1.5x larger than that for commitments to 0. So instead, let us assume that the distribution from which we draw the two primes for a 0 commitment will be different from that from which we draw the three primes for a 1 commitment, but that within those cases, primes will still be chosen from the same distribution. To prevent leakage, we now require two distributions for the magnitude such that the sum of two independent samples from the first is the same as three independent samples from the second. The obvious choice is to take two normal distributions, one having mean and variance 1.5x those of the other (pop quiz: is there any other allowable choice?).

Of course in practice, the distribution we are sampling from is discrete, but we can get a reasonable approximation by sampling the high-order bits as if they came from this distribution.

## Chebyshev's bias

Having dealt with the high order bits, the only avenue for attack I can think of is the low-order bits. There is a strange phenomenon in number theory called [Chebyshev's bias](https://en.wikipedia.org/wiki/Chebyshev%27s_bias) where primes below a value tend to more often be equivalent to 3 (mod 4) than 1 (mod 4).

<!-- Here is my naive intuition for this phenomenon, (which is probably wrong, because none of the references I found explain it this way): Call $Ч_N$ the proportion of odd primes below which are $3 (mod 4)$. There are $\pi(N) \approx N/\log(N)$ (by the [Prime Number Theorem](https://en.wikipedia.org/wiki/Prime_number_theorem)) odd primes below $N$; there are $Ч_N \pi(N)$ are 3 (mod 4) and $(1-Ч_N) \pi(N)$ are 1 mod 4. If we model each prime as being a coin flip to be either 1 or 3 mod 4, then we would expect $\ch_N$ to be about 1/2 (no bias) but with a natural pseudorandom variance like that of a scaled binomial $\pi(N, 1/2)$ random variable, namely of about $\pi(N)/4N$, causing $\ch_N$ to have a standard deviation in this model of about $\sqrt{1/4\log(N)}$. 

But now consider $Ч_{N^2}$. The set of primes less than $N^2$ does not contain any composites less than $N^2$, and in particular, it does not contain any element of subset $P_{N}^2$ of $[1, \dots, N^2]$ consisting of products of two distinct primes below $N$. This set of products will have approximately $\frac{1}{2}(Ч_N^2 + (1-Ч_N)^2) \pi(N)^2$ 1 (mod 4) numbers and $\frac{1}{2}(2 Ч_N (1-Ч_N)) \pi(N)^2$ 3 (mod 4) odd numbers. We notice the former set will thus have more elements than the latter.

Thus, if we model the primes below $N^2$ as being drawn "at random" from the set of odd numbers below $N^2$ which are not in $P_N^2$, we would expect more of them to be 3 mod 4, because there will be

$$ N^2 / 2 - \frac{1}{2}(2 Ч_N (1-Ч_N)) \pi(N)^2 $$

such numbers which are 3 mod 4, but only 

$$ N^2 / 2 - \frac{1}{2}(Ч_N^2 + (1-Ч_N)^2) \pi(N)^2 $$

which are 1 mod 4.

This would give us approximately

$$ Ч_{N^2} \approx \frac{N^2 / 2 - \frac{1}{2}(2 Ч_N (1-Ч_N)) \pi(N)^2 }{N^2 - \frac{1}{2}\pi(N)^2} $$

Or, using the $\pi(N) = N/\log(N)$ approximation

$$ Ч_{N^2} \approx \frac{1 / 2 - \frac{1}{2}(2 Ч_N (1-Ч_N)) 1/\log(N)^2 }{1 - \frac{1}{2}1/\log(N)^2} $$
$$ Ч_{N^2} \approx \frac{1}{2} - \frac{1/2 - \frac{1}{4}1/\log(N)^2}{1 - \frac{1}{2}1/\log(N)^2} + \frac{1 / 2 - \frac{1}{2}(2 Ч_N (1-Ч_N)) 1/\log(N)^2 }{1 - \frac{1}{2}1/\log(N)^2} $$
$$ Ч_{N^2} \approx \frac{1}{2} + \frac{\frac{1}{4}(1 - (4 Ч_N (1-Ч_N)) )/\log(N)^2}{1 - \frac{1}{2}1/\log(N)^2} $$
$$ Ч_{N^2} \approx \frac{1}{2} + \frac{(\frac{1}{4} - (Ч_N (1-Ч_N)) )}{\log(N)^2 - \frac{1}{2}} $$

And with $\ch_N$ having variance around 1/2 equal

As I say, I think there is likely some kind of problem here, and I would love someone to explain the flaw in this thinking if it could be done simply. You could argue that I have done some kind of cherry picking by considering only this very particular set of numbers $P_N^2$ to filter out. tri-prime numbers counteract this, there the bias is $\approx \frac{(a-b)^3}{(a+b)^3}$, so this would seem to be less powerful, although it would get complicated as you considered different magnitudes of primes and larger numbers of factors.
 -->


I haven't been able to find a reference as to whether this bias persists for cryptographically large numbers to an extent that would pose a problem for this scheme. If it did, I suppose you could just use rejection sampling to normalize the frequency of different modularities. But I also understand that a similar bias exists mod 6, so perhaps there is a bit of an arms race there.

## Partially leaked bits

An interesting feature here, that doesn't seem to be the case with most commitment schemes, is that while a naive version of the scheme (say, that sampled primes uniformly at random rather than from an approximately normal distribution) might leak some information about the bit, it doesn't provide a clear way for the adversary to determine the bit with certainty. So even if there is a problem with partial leakage from Chebyshev bias, we could potentially fix this by choosing a bitstring at random from those whose XOR is our desired bit value and then commit to each bit in parallel.

## Final **Question**s

The “1.5x larger” explanation above is not, itself, a very rigorous argument.

What is the minimum statistical distance between Y = X1 + X2 and Z = X3 + X4 + X5, if the Xs are i.i.d. positive-real-valued probability distributions?

Is this scheme, or any variant of it that I’ve described, secure at all?

Can the security assumption be switched from some version of “it is hard to count the factors of a random number with either exactly 2 or exactly 3 prime factors” to something like “it is hard to determine the parity of the count of factors of a random number with either exactly 2 or exactly 3 prime factors”?

Can sampling of “Pre-factored numbers” be of use here? (See related post of mine)

What tradeoffs are there to be made between the security assumptions and the time taken to compute/open commitments?