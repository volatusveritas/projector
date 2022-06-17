# Projector Development Journal, Entry #2

It's been a long time since I've worked on Projector. I got into an internship,
then left, but I won't bother you with the details of it all. Long story short,
I didn't have time to work on this. I learned a few things, and came back. I
won't give up on this project, but I'll do more careful planning before coding
something new. At its current state, the code is broken (and while it's easy to
revert it to a previous version that was working perfectly, that would not be
easy to extend and to implement new features on); I'll probably rewrite a lot
of it, I'm not sure.

I'm trying to work a bit more on the EBNF grammar so I
have a layout of what I expect the language to be able to interpret, I've also
got to carefully plan how *templates* are going to work, as they'll be a pretty
unique element of this language. Right now I see them as functions, models from
which values are generated, and just like functions, there are the ones you
define once to use multiple times, and the ones you only use once ([Anonymous
Functions](https://en.wikipedia.org/wiki/Anonymous_function)), so there will be
those templates you define once to use multiple times, and the ones you only
use once, or Anonymous/Lambda Templates.
