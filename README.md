# Ozeki

Ozeki is a TUI data browser for [sumo-api.com](https://ko-fi.com/sumoapi) allowing you to browse basho data going back to 1960.
It's UI layout is in a bit of flux at the moment, but is build around a set of custom [Textual]() widgets for displaying banzuke
and torikumi data.

Ozeki® is a registered trademark of the Ozeki Sake Company, founded in 1711, for its world-renowned sake. This software project
is not affiliated with, endorsed by, or connected to that historic company. The name "Ozeki" is used here strictly in reference
to the rank in professional sumo, a sport with it's own deep and revered tradition.

## Features

- [X] Basho view (Banzuke and Torikumi widgets)
- [X] Optional background updates / Live view
- [X] Persistence of selected theme
- [ ] User modifiable/supplied themes
- [ ] Rikishi query and deep-dive stats interfaces

## See it in action

[![demo][asciicast]][asciinima]

## Installation

`$ pip3 install git+https://github.com/fuzzy/ozeki`

All there is to it. It runs without arguments. I personally recommend using a virtualenv, I keep a "user wide" one in my ${HOME}.
Setting up something like that would look like:

```
$ python3 -m venv ~/.localpy
$ echo 'export PATH=${HOME}/.localpy/bin:${PATH}' >> ~/.$(basename ${SHELL})rc
$ source ~/.$(basename ${SHELL})rc
$ pip3 install git+https://github.com/fuzzy/ozeki
$ ozeki
```

## Themes

![dark theme][dark]
![light theme][light]
![sakura theme][sakura]
![oni theme][oni]
![maneki-neko theme][maneki-neko]
![kami theme][kami]

[dark]: themes/ozeki-dark.png
[light]: themes/ozeki-light.png
[sakura]: themes/ozeki-sakura.png
[oni]: themes/ozeki-oni.png
[maneki-neko]: themes/ozeki-maneki-neko.png
[kami]: themes/ozeki-kami.png
[asciicast]: https://asciinema.org/a/hJeWx4vjtfJkv2BUbR0sqf9f4.svg
[asciinima]: https://asciinema.org/a/hJeWx4vjtfJkv2BUbR0sqf9f4
