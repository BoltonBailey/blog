# [zk-SNARK Terminology](https://thequantummilkman.substack.com/p/zk-snark-terminology)

![A cube of proof system properties](./proof-system-cube.png)

I and [others](https://youtu.be/hBupNf1igbY?t=108) ([including](https://a16zcrypto.com/posts/article/17-misconceptions-about-snarks/) the great Justin Thaler) have noticed that the term "ZK" is often used as an abbreviation for "zk-SNARK" in blockchain contexts, even when the application under discussion has no fundamental need for the "Zero Knowledge" property, and where the term "SNARK" would therefore be more precise. I experience this in my own collaborations - Some of my formalist colleagues describe our joint project as "the ZK project" even though it doesn't utilize zero knowledge. Are they wrong to do so, even though the majority of people in their industry understand what they mean (and probably use the term that way themselves)?

## Fundamental Redundancy of "zk" altogether

Part of the issue is that essentially all SNARKs that are not "ZK" can be trivially modified to be so. There is a fundamental reason for this - most of the "zk" is already covered by the "S"! If a proof system produces proofs that contain only $\tilde{O}(1)$ data from a linear witness, then the proof can convey very little about the witness information-theoretically speaking. It is therefore not particularly hard to make a SNARK protocol zero-knowledge by modifying it. This has blurred the distinction between zk- and non-zk-SNARKs.

My recommendation is somewhat contra Thaler's. Rather than prescribing more precision in the terms that people are using, we should just establish the norm that SNARK programmers should very conistently make their SNARKs _actually be zero-knowledge_. The drawbacks are minimal:

1. Relative to the difficulty of programming a SNARK, making the SNARK zero-knowledge is easy.
2. The performance difference is hardly noticeable, considering that running a program under a SNARK is already much more expensive than running it generically.
3. It will never be a problem for the SNARK not to be zero-knowledge, because if it is desired that some data from the witness be communicated by the prover, they can just include that information in the clear alongside the zk-SNARK [^1].

### Can this be made rigorous?

I would describe most of the modification procedures for making SNARKs zk as similar to "introduce a few redundant random operations somewhere in the circuit being proved". This is not entirely general though - one can contrive SNARKs that intentionally leak parts of their input for which this operation does not result in zk. What I would be very interested in a generic transformation that gets around this. Unfortunately, I think this is kind of theoretically moot, as you can always just attach a final preprogrammed zk-SNARK on the end. Perhaps that assumes something about the security assumptions though - is there a generic transformation that takes a black-box SNARK and zkifies it without introducing any additional cryptographic assumptions?

<iframe src="https://manifold.markets/embed/BoltonBailey/will-there-be-a-generic-transformat" title="Will there be a generic transformation that zk-ifies a SNARK by end of 2025?" frameborder="0" width="600" height="300"></iframe>

## This goes for the "N" too

Returning to the topic. Many SNARKs (zk or otherwise) are based on Interative Oracle Proofs or "IOPs". The astute will notice a bit of a contradiction here - How is it that "interactive" oracle proofs are giving rise to "noninteractive" arguments of knowledge? The answer is that there is a technique called the "Fiat-Shamir transform" which simply removes the interactivity. Again, it is not fully general, but it applies to essentially every SNARK in existence. It begs the question, though: If the authors of all these papers are just writing interactive protocols and then including a sentence in section where they say "and then we apply Fiat-Shamir", but what right do they claim to have produced "SNARKs". Surely they just made a "Succinct argument" and the references did the rest!

## Reverse Cryptography

I recently had a long conversation with another colleague about whether a particular primitive we were studying was stronger than another. The stronger primitive could be built from the weaker with recursive SNARKs. I usually tend to think about primitives in this relationship has having equivalent strength, because I know there are recursive SNARK protocols that are accepted to work in practice (though in theoretical terms, they have strange catches). Not helpful was the additional confusion about whether it was acceptable to do away with the succinctness. This would have left a primitive that had the same capabilities, but which blew up exponentially the more it was used.

There is a tradition of "[reverse mathematics](https://en.wikipedia.org/wiki/Reverse_mathematics)" which tries to derive exactly which conditions are needed what to prove a statement. Cryptography and complexity theory is similar. Papers are usually pretty rigorous about the "reverse cryptography" of only stating the assumptions you need. I feel ambivalent about this. I understand the desire to be rigorous, and often there are important theoretical distinctions in these nuances (I haven't even mentioned SNAR**G**s in this post). But I feel that it's a bit more parsimonious to just assume that whatever you're working with is a ZK-SNARK and let the reader suss out which assumptions can be dropped. At the very least, it would be cool if we could get some consistency: I'd like all eight corners of the cube above to take the form "(zk-)(S)(N)ARK". We should popularize "SARK" and "NARK" for example.

## STARK

I'll conclude with a mini-rant about "STARK". STARK refers to [the system developed by Ben-Sasson et al.](https://eprint.iacr.org/2018/046.pdf), and stands for "Scalable Transparent ARgument of Knowledge".

While this is a very cool proof system, I dislike the terminology. STARK is just a type of SNARK, but the similarity in how the terms sound makes it tricky to speak clearly and be understood. I often hear the phrase "SNARKs or STARKs". This is redundant or a category error - STARKs are just a particular strain of SNARKs, so one should usually just say "SNARKs".

I don't know why the "S" changed from "succinct" to "scalable", those words mean basically the same thing. By "transparent" they mean the setup is not trusted - I think this is the main distinction I hear Eli Ben-Sasson focus on when he's interviewed to justify the term. But other systems like [Brakedown](https://eprint.iacr.org/2021/1043) have the same properties on this front and describe themselves as SNARKs. I feel the better choice would have been to do something analogous to the "universal" SNARKs and called these types of SNARKs "transparent SNARKs".

[^1]: As a minor caveat, there may be some applications where the output of the SNARK should be deterministic. In these cases it is impossible for the SNARK to be completely zero-knowledge, since if the verifier needs to distinguish two witnesses, they can do so by running the prover. But in these cases, we could just fix a seed for the RNG, so a zk-SNARK could be easily converted to what we need.
