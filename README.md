# ProjectOr

ProjectOr is a (work in progress) generative programming language intended for
RPG campaigns and games alike. Its aim is to allow its users to define
generation templates whereby the language understands how to generate adequate
values when queried to do so. The name "ProjectOr" (bring your attention to the
capitalized 'O' at the end) is a reference to its expression-based nature.

> **Developer Note**: ProjectOr, for me, has the secondary purpose of being a
> learning project. That is one of the reasons why I chose Python to be the
> language behind it. In the future, when the amount of knowledge to be
> cultivated through this project is about as small as meaningless, I have
> plans to port most of it to C in order to greatly improve performance.

<!-- This comment is an MD028 fix-hack -->

> **Streamer Note**: a lot of the production process and work being done on the
> language will be streamed at [my Twitch
> channel](https://twitch.tv/veritasvolatus). I do plan on sharing progress at
> Twitter as well, although I'm not very fond of it. A seemingly better idea is
> to make a YouTube series out of it (once I've decided on it the links for
> either my Twitter or YouTube will be here).

Key functionality goals (an incomplete list):

- [x] Expression Interpretation
- [x] Variable Assignment and Access
- [ ] Range Generation
- [ ] Dice Objects
- [ ] Non-Numerical Value Generation
- [ ] Non-Numerical Dice Objects
- [ ] Generation Templates
- [ ] Functions
- [ ] Keyword Definitions
- [ ] Aliases

## Running ProjectOr

The recommended way to run ProjectOr is

```powershell
python -OO -S -m projector <options>
```

where `<options>` signifies ProjectOr's initialization options (initialize with
`-h` or `--help` to learn more), although you can do without the `-OO -S`
fragment if you wish (or use any Python options).
