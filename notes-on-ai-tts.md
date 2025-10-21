
# Notes on AI TTS

I recently produced a reading of [one of my favorite manifestos](https://www.cs.ru.nl/~freek/qed/qed.html) with [ElevenLabs](https://elevenlabs.io/). In light of that experience, here are some critiques of the software and advice for anyone else looking to use it, along with ideas for making the technology in general more open.

## Critiques and Advice

Many of these should improve naturally with development of the technology. That said...

### Regeneration of long paragraphs consumes lots of credits

Often I had to regenrate a whole paragraph when there was only a small issue that I needed to correct. It would be nice if portions of long generations that have been edited could be reused in subsequent generations.

Unfortunately, it perhaps goes against the interests of ElevenLabs to implement this, given that the credits are what they sell. **My advice: Head this off by breaking up paragraphs into small pieces or individual sentences in advance.**

### Paragraph boundary issues

When switching voices, I sometimes get an inhalation sound at the very end for the voice which is not going to speak anymore. A related issue: Sometimes when swtiching paragraphs, I get the first phoneme of the next paragraph at the end of the paragraph before it, leading to a weird distortion where that phoneme is repeated. **My advice: Play around with pauses between paragraphs to separate things**.

### Incorrect Pronounciations

These come in many flavors:

* Words are sometimes pronounced as their [heteronyms](https://en.wikipedia.org/wiki/Heteronym_(linguistics)). 
* Foreign names and loanwoards are often mispronounced (though you could argue that to produce the most natural reading of these words in an American voice, these sometimes *should* be mispronounced). 
* You sometimes notice that when a sentence coincidentally contains words that almost rhyme, the model changes the pronunciation to make them rhyme. 
* The model speaks other languages well, but immediately after doing so, it will often pronounce English words with a foreign accent.

**My advice: Use the "pronunciations editor" feature to have words pronounced as you would like. Do this early and often to conserve credits. If you have leeway to edit the text, consider a rewrite which is compatible with reading.**

### Bad Rhythm

This is hard to describe, perhaps because English puts less emphasis on *emphasis* than other languages do. This can result in slight mispronounciations, like using "the" as "thuh" instead of "thee". The model also sometimes gets confused by numbered or lettered lists, it seems to forget what the numbers and letters are for and just says them, rather than pausing for them. Another manifestation of this relates to ["scare" quotes](https://en.wikipedia.org/wiki/Scare_quotes) -- while I think there's a natural way to emphasize spoken sentences to make clear that a particular word choice is not the author's, the model doesn't always nail this.

**My advice: Surround words with asterisks to help emphasize them. Use paragraph breaks and em dashes around number and letter labels in lists. But don't use dashes at the start of a new paragraph for dashed lists because the model will sometimes pronounce the word "dash" or "minus". For these, use paragraphs, or for lists of short phrases, a comma separated list. Also, don't be afraid to convey constructions like quotes by verbally saying a phrase like "quote-unquote"**

### Substitutions and Unabbreviations

When reading "R. Descartes", it says "René Descartes". It frequently does this with other names as well. It sometimes switches numbers for ordinals in lists.

**My advice: These are actually good changes that reflect the fact that some abbreviations used to make text more concise aren't needed or don't translate well to speech. Replace the text with longer-form text that can be pronounced just as quickly. It's worth considering doing this for some abbreviations as well. For example, use "for example" in place of "e.g.".**

## Free audio feeds

ElevenLabs has a good offering, but of course I'd like it to be free, both in the "free beer" sense, and in the "free speech" sense. Currently, ElevenLabs offers both of these, but not simultaneously. 

An open source TTS engine would perhaps be needed for a truly free alternative - perhaps [TorToiSe](https://github.com/neonbjb/tortoise-tts) or [Chatterbox](https://github.com/resemble-ai/chatterbox)?

I think another big benefit of the ElevenLabs offering is the UI so any OSS alternative looking to match that has its work cut out for it. It would also be nice, though, to be able to heavily automate the creation of audiocasts. The content I have in mind is primarily academic work: I would really be happy to see an audio feed of freely-licensed preprint papers. 

A few improvements from the current state of things would be needed for this. Extending the above, more elaborately automated ways would probably need to be made of including words/descriptions/voices that are not in the written work, but that would be helpful in audio. Some things that come to mind are:

* Describe images.
* Mark the start of new section or subsections, beyond just saying the title or number, by saying "section" or "subsection".
* Replace references to citations with paper names.
  * For example "the breakthrough ideas of Wiesner [Wie83], and Bennett and Brassard [BB84] demonstrated the possibility of quantum cryptography" could become "the breakthrough ideas of Wiesner in his paper 'Conjugate coding', and Bennett and Brassard in their paper 'Quantum cryptography: Public key distribution and coin tossing' demonstrated the possibility of quantum cryptography"
* Translate grammatical constructs that are not well suited to audio, like "quotes" or "ellipsis" to more mnatural phrases like "quote-unquote" or "and so on".
* Read quotes in alternative voices, as an audiobook might.
  * Could we match gender/accent of voice to inferred speaker gender/accent?
  * Could we ensure the same alternative voice is always used fro same source?
* Read TeX math or code blocks naturally.
  * A hard problem.


