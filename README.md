# Ozeki

Ozeki is a TUI data browser for [sumo-api.com](https://ko-fi.com/sumoapi) allowing you to browse basho data going back to 1960.
It's UI layout is in a bit of flux at the moment, but is build around a set of custom [Textual]() widgets for displaying banzuke
and torikumi data.

## Features

- [X] Basho view (Banzuke and Torikumi widgets)
- [ ] Optional background updates / Live view
- [ ] Rikishi query and deep-dive stats interfaces
- [ ] User modifiable/supplied themes

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

![dark mode][dark]
![light mode][light]

[dark]: ozeki-dark.png
[light]: ozeki-light.png
[asciicast]: https://asciinema.org/a/c6FqgOEok3fWlEyL6JwmTfvoh.svg
[asciinima]: https://asciinema.org/a/c6FqgOEok3fWlEyL6JwmTfvoh
