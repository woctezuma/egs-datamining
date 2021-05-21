# EGS Data-Mining

[![Build status with Github Action][build-image-action]][build-action]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to data-mine the Epic Games Store (EGS).

## Requirements

- Install the latest version of [Python 3.X](https://www.python.org/downloads/).
- Install the required packages:

```bash
pip install -r requirements.txt
```

## Data acquisition

To download data from the trackers (at most once per day):

```bash
python download_data.py
```

## Usage

To figure out codenames of games for which the store page is not yet online:

```bash
python filter_codenames.py
```

The output is shown in `data/outputs.json`
as of May 21, 2021.

Then one can look for hints of unreleased games by manually filtering entries with one of the codenames at:

- [the item tracker][item-tracker-url]
- [the offer tracker][offer-tracker-url]

![Items and Offers, in order to check entries][generic-menu]

e.g. with the codename `Angelfish` :

![Filtering entries by codenames][generic-cover]

## References

Data trackers:

- [items](https://github.com/srdrabx/items-tracker)
- [offers](https://github.com/srdrabx/offers-tracker)

A few useful websites:
-   [EGData](https://egdata.app/)
-   [EpicDataInfo](https://epicdatainfo.vercel.app/)

<!-- Definitions -->

[build-action]: <https://github.com/woctezuma/egs-datamining/actions>
[build-image-action]: <https://github.com/woctezuma/egs-datamining/workflows/Python application/badge.svg?branch=main>

[codecov]: <https://codecov.io/gh/woctezuma/egs-datamining>
[codecov-image]: <https://codecov.io/gh/woctezuma/egs-datamining/branch/main/graph/badge.svg>

[codacy]: <https://www.codacy.com/gh/woctezuma/egs-datamining>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/a2894131818947b9adba5e487a9a0413>

[generic-cover]: <https://github.com/woctezuma/egs-datamining/wiki/cover.png>
[generic-menu]: <https://github.com/woctezuma/egs-datamining/wiki/img/menu.png>

[item-tracker-url]: <https://epicdatainfo.vercel.app/items>
[offer-tracker-url]: <https://epicdatainfo.vercel.app/offers>
