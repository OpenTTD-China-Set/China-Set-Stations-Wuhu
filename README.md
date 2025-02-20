China Set: Stations - Wuhu
==========================

![Unit tests](https://github.com/OpenTTD-China-Set/china-set-stations-wuhu/actions/workflows/unit-tests.yml/badge.svg)
![Docs](https://github.com/OpenTTD-China-Set/china-set-stations-wuhu/actions/workflows/jekyll-gh-pages.yml/badge.svg)

This repo contains the source code for China Set: Stations - Wuhu.

# Building
## Preparation
This depends on an up-to-date version of `agrf`, which in turn depends on `grf-py`.

Install the Go dependencies with `./install-go-dependencies.sh`. Then add `gopath/bin` to your `PATH` variable.

## Make
After installing dependencies, run `make` to build the newGRF.

# Documentation
The documentation of the main branch of this repository is at [here](https://openttd-china-set.github.io/China-Set-Stations-Wuhu/). As it is dynamically generated from the newest commit, it might contain unfinished content or glitches.

# Licensing and Contribution
The released newGRFs will be GPLv2, and thus only GPLv2+ content is allowed if you want to contribute. The exception is that some files under `third_party` are for testing, debugging or documentation purposes and can be under other licenses.
