
# Why are monads hard to explain?

What are monads? Many have offered explanations of what they are / why it seems to be so hard to explain what they are:

1. [A monoid in the Category of endofunctors](https://books.google.com/books?id=MXboNPdTv7QC&pg=PA138&lpg=PA138&dq=%22monoid+in+the+category+of+endofunctors%22+mac+lane&source=bl&ots=feQWTkH2Uw&sig=tv-1JwaMOygKGmFE2vM2FhJVS9o&hl=en&ei=5iWsTJCkBIPSsAPQwJ36Aw&sa=X&oi=book_result&ct=result&resnum=1&ved=0CBIQ6AEwAA#v=onepage&q&f=false)
2. [Abstraction](https://byorgey.wordpress.com/2009/01/12/abstraction-intuition-and-the-monad-tutorial-fallacy/)
3. [Burrito](https://blog.plover.com/prog/burritos.html)
4. [Not a burrito](https://byorgey.github.io/blog/posts/2025/06/16/monads-are-not-burritos.html)
5. [in 300 words](https://lambda.xyz/blog/monads/)

This post is my contribution to this discourse.

## Explanations of monads are like explanations of quantum mechanics

I think the closest of the above posts to my perspective is the second one. Monads are indeed an abstraction best learned by working through concrete examples. But this leaves a bit to be desired as an explanation for the unique difficulty of monads because many things in programming are abstract, and learning by example is a good technique for understanding in general.

Here is the spin I would put on it: Monads are hard to explain because they are "close to the math". The fact that many things in programming can be conveniently captured by monads is a mathematical phenomenon we've noticed and taken advantage of, but which is not sufficiently closely analogizable to other things in programming or the real world. 

I would draw an analogy to quantum mechanics, another topic which ["no one understands"](https://www.youtube.com/watch?v=uK2eFv7ne_Q). We know the formalism of the Schrödinger equation, and we can apply it to demonstrate that it has concepts that map on to the concepts of classsical mechanics in certain ways. But there are also important differences and places where the analogy breaks down, so we often feel that the only way to get results out of it is to "shut up and calculate", rather than develop a conceptual understanding.

<!-- 
An example: [Multivariable polynomials are a monad](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/MvPolynomial/Monad.html). I found this fact very confusing when I first learned it, in fact I spent quite a while looking for the `bind` operation.  I didn't think to look for it in the monad file because I didn't conceptualize multivariable polynomials as monads, and I wasn't thinking that the thing that I was looking for would be in this file. I think this conceptualization failure was because it had been explained to me that monads were just forms of computation. But the in monad interpretation of polynomials does not really fit well into this framework, at least in my own thinking.
 -->

## Monad terminology is confused

Perhaps one reason why monads are hard to explain is that there are many interrelated formalizable concepts, that it is hard to say what things are "monads".

To clarify what I mean by this, I have a [Manifold survey](https://manifold.markets/BoltonBailey/which-of-these-is-a-monad) asking which of a variety of terms is an example of "a monad" (if you are going to complete the survey, please do so before reading on). I have given examples from the Lean programming language and ascribed to each its type.

1. `[1, 2, 3] : List Nat`
2. `List Nat : Type`
3. `List.{u} : Type u -> Type u`
4. `List.instMonad : Monad List`
5. `Monad List : Type (max (u + 1) v)`
6. `Monad.{u, v} : (m : Type u → Type v) -> Type (max (u + 1) v)`
7. `List.instLawfulMonad : LawfulMonad List`
8. `@LawfulMonad List : [inst✝ : Monad List] -> Type (max (u + 1) v)`
9. `LawfulMonad List : Type (max (u + 1) v)`
10. `LawfulMonad.{u, v} : (m : Type u → Type v) -> [inst✝ : Monad m] -> Prop`

Whatever your answer is, the unfortunate issue is that a discussion of an application of monads will usually involve many of these, and unless you are very precise with your words, it is easy to refer to different concepts with the same terminology.

### My answers

What is the best way to name for things of each of these types?

* `List.{u} : Type u -> Type u`
  * Things of this type often seem to be called "monads" in tutorials.
  * But a tricky aspecct of this is that in general, not everything of type `Type -> Type` is a monad. "Type Transformations" might be a general term.
  * Type transformations T such that there is an instance of `Monad T` might be the best candidate for "what is a monad", but you could call these "monadic type transformations" to be more specific.
* `[1, 2, 3] : List Nat`
  * Clearly we could call things of type `List Nat` "lists of naturals", or things which have a type which is of the form `List \alpha` simply "lists".
  * It's trickier to come up with a more general term when we have something like this (i.e. any term of a type obtained by applying a monad to another type)
  * If it's specified by do notation or a list comprehension, you could describe it in those terms (i.e. "a do notation term")
* `List Nat : Type`
  * Things of type `Type` are obviously "types", 
  * But again, not all types are the result of applications of monads to other types. ("Monadic types" perhaps?)
  * In general, things which have the form of List applied to some alpha I might call "list types".
* `List.instMonad : Monad List`
  * I would call things of type `Monad List` "list monad instances" or "monad instances for List".
  * I would call things having type `Monad alpha` for some alpha "monad instances" or "monad instances for alpha".
  * I would call `List.instMonad` in particular "*The* list monad".
* `Monad List : Type (max (u + 1) v)`
  * As above, things having type `Monad alpha` for some alpha I call "monad instances" or "monad instances for alpha".
* `Monad.{u, v} : (m : Type u → Type v) -> Type (max (u + 1) v)`
  * Our discussion here is really only limited to this single term of this type. I don't know if I would call `Monad` "a monad" or "the monad". Perhaps "the monad typeclass".

The lawful terms are all roughly analogous to the corresponding terms that don't assert lawfulness, just with "lawful monad" instead of "monad". In fact I might not even be quite calling the non-lawful versions what I call them above, definitely if they were provably not lawful I would prefer to call them something else.



