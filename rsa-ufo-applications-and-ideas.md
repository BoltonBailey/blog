# Sander UFOs

- [Substack link](https://thequantummilkman.substack.com/p/sander-ufos)

Following up my [previous](https://thequantummilkman.substack.com/p/sampling-certified-primes) [posts](https://thequantummilkman.substack.com/p/bit-commitment-from-factor-counting), here is a more successful and perhaps more practical application of prefactored numbers.

This takes the form of a way to make some small improvements to "Efficient Accumulators without Trapdoor", by Tomas Sander [paywalled link](https://link.springer.com/content/pdf/10.1007/978-3-540-47942-0_21.pdf), [h/t this post](https://ethresear.ch/t/accumulators-scalability-of-utxo-blockchains-and-data-availability/176/4?u=boltonbailey).

## "Efficient Accumulators without Trapdoor" TL;DR

The main quest of "Efficient Accumulators without Trapdoor" is to create a number that no one can completely factor.
This is useful for cryptography in a few ways (see below).

For the purposes of the paper, this means the following:

- The number cannot itself be prime, otherwise it would be trivial to check and provide the factorization.
- It should not be possible to factor the number by just checking for divisiblity by all small prime factors up to `k` bits in size, and dividing those out.
  - Together with the previous point, this means the number must have multiple prime factors of `k`-bits or greater.
    We call such a number a "k-UFO".
  - These properties are meant to guarantee that someone seeing the number, with no other information about it, would not be able to factor it.
- But over and above the number being hard to factor in a blank slate, the paper is also looking to ensure the process of constructing the number does not leave the constructor with enough information to factor it.
  For emphasis, *no one* should be able to factor the number - it's not sufficient to have somebody [multiply two large primes](https://en.wikipedia.org/wiki/RSA_cryptosystem), because then they would know the factors.

To get a sense of why this is tricky, notice that it's not enough to simply agree on a large pseudorandom number, like "the first few hundred digits of pi".
A large random number has a [small but nonneglible chance](https://en.wikipedia.org/wiki/Prime_number_theorem) to be prime itself, and therefore easy to factor.
Even if we run a primality test to check this is not the case, there's still a chance that the number could be a relatively small multiple of a prime, and this level of risk is above what we consider secure in cryptography.

### The basic idea

While a single `n`-bit random number chosen uniformly at random has some inverse-polynomial chance of being prime, it also has inverse-polynomial chance to have two prime factors at least `n/3` bits in length.
Therefore, if we multiply `r` such numbers together, we have a number $N = \prod_{i=1}^r N_i$ which is negligibly likely to be factorable.

A number derived in this way satisfies the transparency condition: We can choose the `N_i` to be something like "the bits of pi broken up into 4096-bit limbs".

## Savings

The main downside of this approach is that the modulus ends up being pretty large, so I look to improve it by making the number smaller, or proving that you don't need a `r` to be very large to get a certain level of security.

### Savings by grinding out / excluding small factors

This was mentioned in the paper and thread: If we sample a number in this way, some `N_i` will be primes, and we can exclude these.
Still other `N_i` will have small factors - we can improve the scheme by checking numbers for such factors (up to, say, 2^30) and dividing them out.
But I actually think it's better to simply replace samples having small prime factors altogether by resampling.
My intuition is this: We should be choosing our sample to have the optimal size with respect to the tradeoffs on algorithmic properties, and using a smaller sample is essentially like artificially choosing suboptimally.

### Savings/parallelization using CRT

Cryptographic applications will generally involve modular arithmetic over `N`.
Because `N` here is constructed as a product of smaller numbers, it is possible to carry out arithmetic mod `N` via the Chinese Remainder Theorem, by representing the number as a vector of moduli for each `n_i`, and doing the arithmetic over those.
This has the benefit that if one is using a $O(f(x))$-time multiplication algorithm, multiplication will take $O(r f(k))$ time, rather than $O(f(r k))$ time.

This is a speedup, since $f$ is superlinear for all known practical multiplication algorithms, and it is more of an improvement the more superlinear $f$ is.
For example, using the $O(n^{1.58})$-time Karatsuba algorithm and $r = 128$, this would be speedup of $128^{0.58} \approx \times17$.

Furthermore, since the CRT allows us to do the arithmetic in parallel, the parallel time speedup goes from $O(f(r k))$ in parallel time to $O(f(k))$.

Note that this has the nice alternative interpretation of being a repetition-amplification of the underlying cryptographic protocol, since we are effectively running that protocol in parallel.
If we are in the parallel setting, our protocol is just as efficient as one using a single semiprime (except that we might be choosing ours larger to make it possible to have two distinct factors as large as direct sampling would give us).

### More exact security analysis by pre-factorized number statistics

Sander's approach to proving the security of this system is to use the prime number theorem to lower bound the fraction of `n`-bit numbers which are `k`-UFOs for $n/3 \le k \le 5n/12$ at about $\frac{1}{2} \ln^2(\frac{n}{2k}) + O(1/n)$.
But this approach has some downsides:

- This argument only works for $n/3 \le k \le 5n/12$
- The best fraction it can possibly guarantee you is 0.082201 at $k/n = 1/3$
- There is a fudge factor associated with the approximation in the Prime Number Theorem
  - If you wanted to concretely prove a bound with this, you might have to look through the literature for concrete constants to the prime number theorem
  - But even if you find such constants, they might not be the best possible for your value of $n, k$
- None of this reasoning involves the "grinding out" step from above, so it will be even harder to account for the savings that gives you.

Here is my proposal: Instead of analytically computing the lower bound on the fraction of random numbers that don't experience grinding which are UFOs, we can make a statistical estimate of this fraction by [sampling many pre-factorized numbers](https://inst.eecs.berkeley.edu/~cs276/fa20/notes/Kalai_generating_factored.pdf), filtering out the ones that would have been ground away, and looking at the factorizations of those that remain.
In fact, it seems we can modify the Kalai algorithm to directly generate numbers with no prime factors below our `2^{30}` threshold by simply stopping the list procedure early.

Of course, this raises the possibility that we could experience a sampling error to cause us to overestimate security.
But this can be solved by adding the chance of such an error into our estimate of the chance of missing UFOs `r` times, and doing enough samples so that the latter dominates.
It's worth noting that the security parameter for this part of the scheme does not have to be as large as the parameter which dictates `k`, because increasing the compute that the adversary brings to bear does not increase the chance that our statistical procedure (which any honest auditor can replicate) experiences sampling error.

#### Computations

Here is the data summary of some samples I collected of various sizes from a Rust script I wrote:

```
Statistics from 24 samples (factor_lower_bound = 2^30), with UFO threshold of 2^1024:
318 bit number: non-ufo composite
589 bit number: non-ufo composite
1194 bit number: non-ufo composite
1619 bit number: non-ufo composite
1809 bit number: non-ufo composite
1887 bit number: non-ufo composite
1983 bit number: non-ufo composite
2034 bit number: non-ufo composite
2062 bit number: non-ufo composite
2294 bit number: non-ufo composite
2352 bit number: non-ufo composite
2610 bit number: non-ufo composite
2720 bit number: non-ufo composite
2728 bit number: non-ufo composite
2943 bit number: non-ufo composite
3398 bit number: ufo
3655 bit number: ufo
4744 bit number: non-ufo composite
5038 bit number: ufo
5351 bit number: ufo
5370 bit number: non-ufo composite
5425 bit number: ufo
5436 bit number: non-ufo composite
5841 bit number: ufo
```

It would take more time to compute more samples, but my conclusions from this are:

- It seems really justified to avoid lower bitlengths, and make sure all your post-grinding samples are large.
- With these parameters, it seems like by the time we get to 6000-bit numbers, about half of post-grinding numbers are UFOs (more than the 0.082 that the number-theoretical bound gives.)
- If this is right, and we wanted to ensure, say, a 1-in-quadrillion chance of error, we would only need 40 or so 6000-bit samples.

[Here](https://manifold.markets/BoltonBailey/what-fraction-of-these-numbers-are) is a prediction market on this.

## Use Cases

As I mentioned, the RSA-UFO has a number of applications in cryptography.

### Accumulators

The use case Sander had in mind was the "Accumulator", essentially a replacement for a Merkle tree that is supposed to have better properties around batch operations.
I think this use case may have fallen out of favor, though.

### The VDF use case

The [parallelization](./#savings-using-crt) section above suggests an interesting use case: RSA-based verifiable delay functions (See the prior works of [Pietrzak or Wesolowski](https://eprint.iacr.org/2018/712.pdf)).
This primitive is thought to be most useful in settings where the computation of the VDF takes a relatively long unparallelizable time, but is otherwise inexpensive, and where it is highly necessary for multiple parties to trust the modulus.

This makes the RSA-UFO a good candidate for the VDF modulus.
Non-intuitively, the "parallelizability" of the multiplication computation is actually a good thing: It means that the "non-parallelizable" aspect of the VDF using multiple moduli takes the same amount of time to compute as a single modulus would.

### The Quantum Canary use case

(Thanks to Or Sattath for suggesting this use case.)

A [quantum canary](https://www.researchgate.net/profile/Or-Sattath/publication/369199060_Protecting_Quantum_Procrastinators_with_Signature_Lifting_A_Case_Study_in_Cryptocurrencies/links/650ad0b7d5293c106cc9b0e5/Protecting-Quantum-Procrastinators-with-Signature-Lifting-A-Case-Study-in-Cryptocurrencies.pdf#page=4.69) is a public problem which is intended to be solvable by quantum computers, and furthermore, by quantum computers which are *less powerful* than those that would be needed to break modern cryptography.
The hope is that by placing bounties for solving quantum canaries, we can encourage potential attackers to reveal their capabilities before cryptosystems are vulnerable so that we know when to prepare.

Public trust in the modulus is important for this use case, since people will not contribute to the bounty or take a successful claim seriously if they believe the modulus is compromised.

## Final Thoughts and **Question**s

- How do the Bach and Kalai pre-factored number algorithms interact with statistics?
  - Essentially, both of these papers say to either run a deterministic primality test, or repeat a non-deterministic test to taste.
  - But it seems like this leaves out the possibility for a number of tricks.
    - For example, if you are running deterministic tests or non-deterministic tests w/ tolerance for error very low, you might be very disappointed if you do a ton of these expensive tests, only for rejection-sampling to undo your work.
      Instead, you might run only a few Miller-Rabin iterations per prime, enough to be fairly confident but not certain, and then only once you are sure the rejection sampling will succeed do you go back and complete the tests, reseting to the previous state if they fail.
      - Application of call/cc?
    - If the only purpose of the statistical tests is to guarantee that at least `x` fraction of samples are UFOs, and in fact `y > x` fraction are, then I can set the probability of failure of the sampling procedure to `(y - x)/2`, and then prove that these pseudosamples are UFOs with probability at least `(x+y)/2`.
- What is the best non-statistical lower bound on the number of `n`-bit `k`-UFOs with grinding up to `g` bits?
  - Even better than checking that there are no prime factors below `g` bits might be to ensure that a stronger factorization algorithm (elliptic curve based?)
    run for X time does not surface any factors.
    - What is the best (algorithm for generating a) statistical bound on the fraction of UFOs obtained from sampling this way?
    - What is the best non-statistical bound?
- A drawback seems to be that the primes that make up the UFO might not be of the same order of magnitude, so it is hard to reduce directly to RSA-type assumptions.
  What are the best ways to reduce the security of UFOs to the security of RSA keys chosen with primes in some specified way ([examples?](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_svenda.pdf)),
- Given runtimes for arithmetic operations, what is the best choice of parameters `(n,g,r)` for a sampled set of UFOs at a given level of security and UFO `k` value?
  - Answering such a question statistically seems like it would require running multiple statistical tests.
    What is the best way of [Bonferroni-correcting](https://en.wikipedia.org/wiki/Bonferroni_correction) these tests.
