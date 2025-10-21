I was saddened to hear about the recent passing of David Kelly. Kelly was well-beloved as the Director of the Hampshire College Summer Studies in Mathematics. HCSSiM is a 6-week summer program that lets high school students interact with college-level mathematics. My participation in HCSSiM was one of the highlights of my high-school years, and I would encourage any math-loving high-school student to consider applying.

In light of this news, I wanted to share an anecdote about my own time in the program, and how it led to the first paper I published in graduate school.

My time at HCSSiM
I participated in HCSSiM the summer after my junior year of high school. It was a great experience for me. It was perhaps the first time that I had a social circle that was interested in math the way I was — I had participated in math club in high school, but most of my friends were theater kids, so this was really the first time I had a friend circle I could relate to through my interest in math. HCSSiM was, in many ways, a preview of undergrad for me. In retrospect, I think I chose to go to Caltech because the culture there reminded me of the culture at HCSSiM - the small class size and the focus on quixotic traditions are salient similarities.

It was also the first time I got to experience what some might call "real math"1, exploring ideas rather than just learning them. I recall learning about Gaussian integers. At some point we started factorizing them, and we started asking questions about whether these factorizations were unique, as factorizations of natural numbers are. It’s really a credit to the staff there that they understand how to lead students into asking interesting questions, while also getting out of the way to let the students pursue those questions on their own volition.

In 2017, the year after I graduated from college, I had planned to spend the summer with my family before going off to grad school. But in late June, I (and presumably many other HCSSiM alumni) got an email looking for a last-minute addition to the junior staff. I responded to the email with some references and was chosen for the slot.

The Watermelon Puzzle
The initial workshop of HCSSiM starts with a presentation for the students of a particular problem about "cuts" of n-dimensional "watermelons". By the time I became a staff member I had forgotten the problem from when it was shown to me as a student, so I paid careful attention.

I won't go into too much detail about the solution here, so as not to spoil it for anyone who might attend HCSSiM in the future. Suffice it to say, I think the solution to the problem can be approached in a number of ways depending on the insights the students have. In the course of the group-problem solving effort, someone started making a table of solutions for particular values of n and different numbers of cuts. At some point I wrote down the table of solutions in one of my notebooks. I like to maintain tables and plots of various mathematical curiosities like this in my notebooks (I guess I'm sentimental that way, and I thought this particular table was a nice guide to the problem).

My First Year of Grad School
After the summer was over, I started my first year of grad school. Unlike a lot of other students in my department, I came in with a clear idea of who I wanted my advisor to be. Most students are advised to take a year of doing independent studies and seminar classes with a variety of professors, but I had had a nice phone call with one of the professors who was interested in my application and so I very quickly signed up to make him my official advisor.

This professor, Matus, worked on "Deep learning theory": Essentially, his work involved using a variety of mathematical techniques from statistical learning theory, dynamics, and combinatorics to prove theorems about neural networks. When you get to the level of a working researcher, you are meant to be pushing forward the frontier of human knowledge. This tends to make your work very niche. This is one of the things that makes finding an advisor matched to your interests simultaneously crucial and difficult. Still, understanding neural nets was one of my keen interests, and I was excited to do this from a mathematical perspective.

To get me up to speed, Matus gave me overviews of a lot of work he had done, smattered with some suggestions for things I could work on. I gravitated towards a particular paper of his about understanding neural network architectures in terms of the number of times they could cross the x-axis.

Serendipity
Matus's paper had focused on a construction for a function with input dimension of 1. It was possible to use tricks to apply the result in higher dimensions, but making the result more inherently multidimensional seemed like an important way we could extend the result, so I started looking at ways we could do this.

Unfortunately, this setting seemed a lot trickier. I spent a few weeks trying different things to no avail. The essential problem was that the original result had been counting the number of times a univariate function had crossed back and forth over the x-axis, but it wasn't so simple to analogize this in higher dimensions. The best analogy was to view the neural network as an piecewise affine map and count the pieces, but it was tricky to understand how additional layers affected this count.

Frustrated by my inability to understand the problem, I started making a table of the number of pieces that were possible from a single layer of the network, starting with a k-dimensional input, moving to an n-dimensional output.

This was where things began to feel familiar.

In perhaps the most serendipitous moment of my professional life, as I started to make this table, I realized it was exactly the same table I had made to understand the watermelon problem at HCSSiM a few months earlier. In retrospect, the analogy was obvious - The dimensions of the watermelon were like the dimensions of the output space, and the "cuts" were like the applications of the ReLU nonlinearity. Most importantly, this gave me a formula for counting the affine pieces, which let me precisely quantify how additional layers were increasing the expressive power of the network. Working through the math, I found that this bound gave had the same asymptotics as an easy construction generalized from the earlier paper, so not only was the bound quantifiable, it was essentially optimal.

A NeurIPS Paper and an NSF Fellowship
The next step was to write the paper up. I found this something of a slog. While I was familiar with writing rigorous proofs from my undergraduate math major, there's something a bit different about doing that kind of thing coherently at the scale of a 22-page paper. After a number of revision passes with Matus, I eventually submitted the manuscript to NeurIPS, one of the most prestigious conferences on machine learning.

My paper was accepted! And not only that, it was accepted for a spotlight presentation (essentially, I got to give a short talk on the paper on one of the conference stages). This is something that only happens for around 20% of accepted papers, so this was like a massive bonus stamp of approval on top of the acceptance, which was already confirmatory of my value to the academic community.

This was especially great as a CV builder for someone in their first year of grad school. Many first and second year grad students are encouraged to apply for the NSF Graduate Research Fellowship Program (NSF GRFP). Having a paper bonus-accepted to a top-tier conference is great fodder for an application. And the cherry on top was that I had a great story to tell in the “broader impact” section about how I had been a staff member at HCSSiM and how that was linked to my great success. I received the NSF Fellowship, which locked me in to three years of sweet, sweet government funding.

Moving on in Academia
The rosy way to continue this story would be to tell you that I did three or four more years of great research with Matus, got my Ph.D. in machine learning, and landed a tenure-track professorship at a top university in the full swing of the LLM boom.

That's not what happened. Around 3 years into my Ph.D. I stopped working with Matus and went to look for another advisor.

I wish there was a simple explanation for this, but there were ultimately a lot of factors at play that caused me to want to change things.

Personal issues in other parts of my life.

Research in deep learning theory didn't hold the meaning for me I originally thought it would. Part of this is that the deep learning revolution has been more about engineering than theory, so much of the mathematical work one can reasonably do to understand neural networks on a deep level doesn't have much objective explanatory power. This is not to say that this kind of work isn't valuable or important, but it wasn't giving me the satisfaction I was looking for.

I found math-paper writing hard. Academic writing has actually never felt right for me. There is a lot of emphasis on documentation. You are expected to differentiate your ideas from similar prior work, rather than show their connections to far-reaching concepts. But writing math is especially hard because you have to communicate in an understandable style while maintaining full rigor. It’s hard to do this without becoming repetitive.

To be frank, I think that these issues together would probably have been enough to cause me to leave grad school altogether, if not for one thing - the NSF Fellowship. I still had two years left which basically guaranteed me two additional years of income. This made me a very attractive proposition as a potential advisee, because whoever I went with wouldn't have to fund me for a full 5 years from their own budget. I took a semester and a half to take new classes and explore other areas of research, and I eventually found an advisor whose interests were more closely aligned with what I wanted to do2.

Learnings
I had originally intended to publish this blog on “Yellow Pigs Day”, July 17th. This is a special holiday to HCSSiM and David Kelly that celebrates some of their long-held traditions.

It’s appropriate that I publish it a week late - I never was good at writing to a deadline. I feel my writing has become a deep contrast to the academic style. I eventually did my Ph.D. thesis on application of formal methods, a field which is all about writing your math so that computers can understand it, rather than just humans. And now I blog, which I find a more freeing way to express ideas, without the need to justify their originality at length.

When I was just starting to look for a new advisor, I met with the head of our division, and he gave me some advice along the lines of “find one thing you are passionate about and focus deeply on that one thing”. I feel this is great advice for success in computer science, which seems like a somewhat siloed environment to me, even compared to other academic fields. Yet I followed the advice terribly. I have always been too in love with drawing connections between different areas. But while that approach works poorly in CS, I think its a way of thinking that many mathematicians, and Kelly in particular, would endorse.

The watermelon theorem is the purest example I have of a connection I made in service of a coherent theoretical advance. I wonder if making this sort of connection is something that mathematicians more professional than I experience all the time. Certainly I never drew anything like it myself again. I wonder if expecting but not obtaining more of this divine inspiration is part of what led to the breakdown of my research program with my first advisor.

Maybe this is the sort of connection that only comes once in a career. But luckily for me, once seems to have been enough.