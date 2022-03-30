# ProjectOr Development Journal, Entry #0

So far, the development of ProjectOr has been an experiment more than anything,
in three ways:

- firstly, I want to see if I'm actually capable of designing and implementing
  a programming language, or become capable of such a thing in the process of
  trying and failing;
- secondly, I want to show beginners what actually trying to do something new
  looks like, unlike YouTube tutorials and programming courses often do, or do
  very poorly[^1];
- thirdly, I want to see if I can generate engagement in coding streams, in
  order to decide whether I will invest more time and effort in this secondary
  career or not.

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
  to compare yourself to others, and the typical result of that is sadness and
  amotivation. I shall write about these topics with increased depth in the
  future, but let it be concluded that the way tutorials and courses are
  teaching their pupils at current times is a dangerous slope of poor-quality
  information and lack thereof towards sharp spikes of give-ups and "I don't
  need to learn that right now", where "right now" quite often ends up being
  "never".

Now that it's been somewhat tested and mathematical expressions seem to be
correctly interpreted, it's a good time to actually start the hard work. A huge
part of the hardship comes from Syntax Design. Not only has the language to
work, but also to be enoughly descriptive by itself in order to bring ease to
the lives of its users. This is the goal of making most operators and special
elements of the language *keywords* instead of *single character symbols*. It's
also why I've mentioned my intent of allowing the user to define their own
keywords and special symbols (in a way that doesn't conflict with the built-in
keywords, of course).

## A keyword-based language

Last stream (29/03/2022) I discussed how I wanted the keywords to make sense
and at the same time fit into a fantasy dungeon-like setting (as you can see, I
love throwing challenges at myself in rather unnecessary amounts). So the
brainstorming began and I decided to name the basic data types as dungeon
elements and contraptions. Here is the result of such playful labor:

- Integer (int) became `abacus`. An abacus only has whole pieces and its
  antique nature fits somewhat well with a medieval RPG setting.
- Floating point (float) became `decimal`. I tried to find some object to which
  attach floating point numbers, but couldn't, so I just went with the standard
  name for it.
- Boolean (bool) became `lever`. Levers only have two mechanical states, and
  the natural consequence of such a thing is that true and false have now
  become `on` and `off`, respectively.
- String (str) became `scroll`. A scroll can be short or long, and is nothing
  but a collection of individual characters or symbols, just like a string.
- Array (arr) became `chest`. A chest stores items rather unorganizedly (it's
  hard to extract a specific item) and the contents pile up (when you add more
  and more items, the ones at the bottom become harder to get out), just like
  an array.
- Dictionary (dict, HashMap) became `backpack`. Compared to a chest, a backpack
  is very organized and has specific pockets for specific kinds of items, so
  it's easier to get specific items out as long as you know what you're trying
  to get out, just like a dictionary.
- Linked list (llist) became `chain`. A chain is composed by `links`, connected
  to the one before and after itself. It's not a complex task to remove one of
  the links, as all you need to do is connect the one which was before and
  after together, just like a linked list.

### Poetry-like syntax

I also discussed how the way we usually declare and initialize typed variables
doesn't make a lot of lyrical sense (the usual structure is type, identifier,
assignment operator, and value, in that order) and while `int amount = 15` read
as "integer named 'amount' with value 15" makes sense, all you need to do is
introduce array notation and the whole thing breaks; `int amounts[2] = {0 ,1}`
read as "integer named amounts which is actually an array with two elements
with values 0 and 1" doesn't make that much sense, now does it? My solution
is to always introduce the type after the name in isolation, so it always makes
sense, observe:

- `amount (int) = 15` read as "amount (an integer) with value 15";
- `amounts (int[]) = {0, 1}` read as "amounts (an integer array) with values 0
  and 1;
- `precisionTable (float[][]) = ...` read as "precisionTable (a two-dimensional
  array of floats) with value ...";

### Compound types' keyword syntax

Next, I though of how to turn array notation (`int[]`, `float[][]`, or
`char[]`, for example) into a more readable syntax that (ab)uses keywords, and
so my final conclusion came to be `chest of <type>` where `<type>` is the type
of data to sequentialized, look at some examples:

- `lines (chest of scroll) = ["first line", "second line"]`;
- `amounts (chest of abacus) = [5, 3, 7]`;
- `switches (chest of lever) = [on, off, off, on, off]`;

Now, for multi-dimensional arrays, I'm conflicted between comically allowing
the use of chained array statements as the usual, which looks a bit goofy:

- `precisionTable (chest of chest of rational) = ...`;
- `obstructionMask (chest of chest of lever) = ...`;
- `tileNames (chest of chest of scroll) = ...`;
- `voxels (chest of chest of chest of abacus) = ...`;

and compressed notation, which is a bit more efficient both to parse and write,
but looks a bit ouf o place in a medieval environment:

- `precisionTable (2D chest of rational) = ...`;
- `obstructionMask (2D chest of lever) = ...`;
- `tileNames (2D chest of scroll) = ...`;
- `voxels (3D chest of abacus) = ...`;

I had some other ideas like `russian doll` and stuff, but I couldn't find a way
to fit it that wasn't extremely verbose. For now, we are going with the second
option, compressed notation. Linked lists will use the same notation, except
for the fact that `chest of` will become `chain of`.

Dictionaries are a bit different, because typed dictionaries need to be
provided with two types: the type of key to be used, and the type of the
values. So, to keep things consistent, I'm going to make an extension of the
already determined array notation. I have some possibilities in mind; the
following examples suggest a dictionary which maps integers to strings:

- `backpack of abacus like scroll`;
- `backpack of abacus meaning scroll`;
- and even `backpack where abacus means scroll`;
- and `backpack where abacus is scroll`;

I'll leave it at that, for I haven't made my mind yet. Stay tuned because I'll
get back with a decision in PDJ#1.

## Correct delegation of parsing tasks

Before, I had the tokenizer generate single tokens, such as the addition
operator token, or the integer and string tokens, but it was also responsible
for grouping values inside parentheses, and it would deliver a TokenGroup token
with other tokens inside to the parser. This is not optimal, because the
tokenizer doesn't know context (that's the parser's task) and as a result often
obfuscates the actual meaning of these parentheses (it also made it quit
difficult to implement the aforementioned variable declaration syntax, which
makes use of parentheses. The way they were parsed also felt hacky.
Additionally, the concerns of my code were incorrectly separated; in a simple
and maybe shallow way of describing it:

- the tokenizer's job is to generate individual tokens, ignoring whatever their
  surrounding symbols may mean (it's non-contextual);
- the parser's job is to, based on the tokens generated by the tokenizer,
  recognize the meaning of these symbols under context, and generate an
  appropriate execution tree;
- the evaluator's job is to, based on the execution tree generated by the
  parser, produce and format an output;

My solution was to create new token types, in a nicely organized tree of
inheritance because I'm using classes. I created a parent class inheriting from
Token called SymbolCoupleToken, which is used to represent any token symbol
which makes a pair. From it, I derived classes for specific symbols. Now, the
Tokenizer generates single tokens when it finds opening and closing pair-making
symbols (parentheses, brackets, braces and chevrons alike).

## If you're gonna go there

If you're willing to invest your time in porting ProjectOr to other languages,
here are some suggestions from the author for repo names (besides "ProjectOr"
followed by the language name, or vice-versa, of course):

- to C: CrojectOr;
- to C++: ProjectOr++/PlusjectOr;
- to Java: JavajectOr;
- to C#: ProjeSharp/SharpjectOr;
- to Lua: LuajectOr;
- to JavaScript: JSJectOr;
