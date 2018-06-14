# ghstars.py

Since GitHub does not list stars in the frontpage anymore, I want do something about my tiny digital ego. This is a simple Python 3.3+ script to report repositories with stars, sorted by star count.

This script uses GH Public API, which has a [rate limit](https://developer.github.com/v3/#rate-limiting). You can easily exceed it if a big organization (ie, Microsoft) is queried a couple times.

## Usage

Make sure you have `requests` installed and run:

```
python ghstars.py owner [owner2 owner3 ...]
```

For example:

```
> python ghstars.py insilichem

 Repo                     Stars
 ======================   =====
 insilichem/pychimera        21
 insilichem/esigen            7
 insilichem/gaudi             4
 insilichem/ommprotocol       4
 insilichem/tangram           2
 insilichem/gaudiview         1
```