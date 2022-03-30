# ProjectOr Development Journal, Entry #-1

Welcome to the ProjectOr Development Journal (PDJ). This is the first entry on
the journal, and it describes the purpose of these entries. They are all
currently written by Volatus (whom you may know as Lucas B. M., or, if you're
an old-timer, Religard). There is no intent to make PDJ "open" (no pull
requests containing new PDJ entries or changes to existing entries will be
accepted until such entries are removed from the forked branch).

## What is this?

The ProjectOr Development Journal is a collection of entries related to the
[ProjectOr Programming Language](https://github.com/volatusveritas/projector)
project. In a sense, it serves as a summary of updates, registering changes and
new/removed/deprecated features, but consistent updates on changes are not
guaranteed at all. The actual purpose of it is to serve as a kind of devlog,
whereby I will explain the reasoning behind my decisions for the syntax,
features and implementation (and describe my difficulties, of course). This is
not my first try at a programming language and, if it fails, it will of course
not be my first failure.

> If you have any tips or wants to contact me/ask anything, the best place to
> find me is at Discord, just send a message to `Volatus#7684` (I know this is
> not the best or most efficient method of communication for a public project,
> but it should be enough while I don't create a Discord server for [my Twitch
> channel](https://twitch.tv/veritasvolatus).

## What is ProjectOr?

ProjectOr is a **generative programming language** (a neologism to indicate
that the main task of the language is to generate values based on templates and
other forms of structure description). It is mainly intended for tabletop RPG
games, but may apply to any situation in which the generation of templated
values could prove useful. It is very keyword-based (for increased readability)
and is made so it can easily be used inside other projects (e.g. one could
create a Discord bot and use ProjectOr as its backbone to generate values). It
is currently written in Python, more for practicality than anything.

> There is intent to port ProjectOr to C, C++, Java, C# and JavaScript (which,
> of course, will take a long time for me to do unless some angelic individuals
> decide to bestow upon me the blessing of their gentleness and take into their
> hands the task of porting it).

<!-- This comment is an MD028 fix-hack -->

> When I talk about ProjectOr in the present tense, I'm really indicating what
> the plans for the future of the language are. At this point in time,
> ProjectOr is very immature as a language in general, even more so as a
> generative programming language.

## Why is this entry numbered negative one?

Because (real) programmers start counting at zero. This is the entry before the
entries, like a prelude, therefore it's one before zero, which is negative one.
Entry number zero will be the first entry, number one will be the second entry,
and so on and so forth.

### Checkpoint Entries

Every entry which is a multiple of eight will be a **Checkpoint Entry**, a
special entry in which I shall record what happened in the previous entries up
to the first entry after the last checkpoint, just like the end of a chapter in
a book.

> Now you may ask: "Why eight? Is there any reason behind such a specific
> choice?", and I shall answer, like the ones who know me should expect, that
> there is no particular motive for this number to have been chosen... besides
> the fact it's the closest integer to ten which is a power of two, of course.
