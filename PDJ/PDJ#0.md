# ProjectOr Development Journal, Entry #0

So far, the development of ProjectOr has been an experiment more than anything,
in three ways: firstly, it want to see if I'm actually capable of designing and
implementing a programming language, or become capable of such a thing in the
process of trying and failing; secondly, I want to show beginners what actually
trying to do something new looks like, unlike YouTube tutorials and programming
courses often do, or do very poorly[^1]; thirdly, I want to see if I can
generate engagement in coding streams, in order to decide whether I will invest
more time and effort in this secondary career or not.

[^1]: Programming courses and tutorials very often lack any display of trial
  and failure, or, in the rare case in which these are seen, they are poor in
  quality or realism. Especially in the case of tutorials, development is shown
  in perfect step-by-step fashion, as if the programmer already knew with
  outstanding precision what he had to do, how to do it, and was sure it was
  going to work. Unfortunately, this leads many beginner programmers,
  especially the many who are addicted to said tutorials, to think this is how
  real world programming looks like. This leads them to delay the blossoming of
  their debugging skills, and suffer greatly from it, for it's an integral part
  of being a good programmer. Not only that, but it usually is also damaging to
  their mental health. We are at a point in our society where it's very common
  to compare yourself to others, and the tipical result of that is sadness and
  amotivation. I shall write about these topics with increased depth in the
  future, but let it be concluded that the way tutorials and courses are
  teaching their pupils at cukrent times is a dangerous slope of poor-quality
  information and lack thereof towards sharp spikes of give-ups and "I don't
  need to learn that right now", where "right now" quite often ends up being
  "never.

Now that it's been somewhat tested and mathematical expressions seem to be
correctly interpreted, it's a good time to actually start the hard work. A huge
part of the hardship comes from Syntax Design. Not only has the language to
work, but also to be enoughly descriptive by itself in order to bring ease to
the lives of its users. This is the goal of making most operators and special
elements of the language *keywords* instead of *single character symbols*. It's
also why I've mentioned my intent of allowing the user to define their own
keywords and special symbols (in a way that doesn't conflict with the built-in
keywords, of course).
