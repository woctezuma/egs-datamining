# EGS Data-Mining

[![Build status with Github Action][build-image-action]][build-action]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to data-mine the Epic Games Store (EGS).

The workflow consists in:
1.   listing namespaces associated with a known store page,
2.   extracting codenames from the databases of `items` and `offers`,
3.   filtering out codenames associated with a known store page,
4.   listing one or several namespaces associated with each codename,
5.   listing one or several `items` and `offers` associated with each namespace.

## Requirements

-   Install the latest version of [Python 3.X][python-download-url].
-   Install the required packages:

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

-   [the item tracker][item-tracker-url]
-   [the offer tracker][offer-tracker-url]

![Items and Offers, in order to check entries][generic-menu]

e.g. with the codename `Angelfish` :

![Filtering entries by codenames][generic-cover]

## References

Data trackers:

-   [items][item-tracker-github]
-   [offers][offer-tracker-github]

A few useful websites:
-   [EGData][egdata-website]
-   [EpicDataInfo][egdatabase-website]

Press coverage:
-   [PC Gamer][pcgamer-ff7r-awr]: "Final Fantasy 7 Remake listing shows up on Epic Games Store database tracker"
-   [VGC][vgc-ff7r-awr]: "Alan Wake Remastered and Final Fantasy 7 Remake listings spotted on the Epic Games Store’s database"

<!-- Definitions -->

[build-action]: <https://github.com/woctezuma/egs-datamining/actions>
[build-image-action]: <https://github.com/woctezuma/egs-datamining/workflows/Python application/badge.svg?branch=main>

[codecov]: <https://codecov.io/gh/woctezuma/egs-datamining>
[codecov-image]: <https://codecov.io/gh/woctezuma/egs-datamining/branch/main/graph/badge.svg>

[codacy]: <https://www.codacy.com/gh/woctezuma/egs-datamining>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/a2894131818947b9adba5e487a9a0413>

[generic-cover]: <https://github.com/woctezuma/egs-datamining/wiki/cover.png>
[generic-menu]: <https://github.com/woctezuma/egs-datamining/wiki/img/menu.png>

[item-tracker-url]: <https://database.egdata.app/items>
[offer-tracker-url]: <https://database.egdata.app/offers>

[python-download-url]: <https://www.python.org/downloads/>

[item-tracker-github]: <https://github.com/srdrabx/items-tracker>
[offer-tracker-github]: <https://github.com/srdrabx/offers-tracker>

[egdata-website]: <https://egdata.app/>
[egdatabase-website]: <https://database.egdata.app/>

[pcgamer-ff7r-awr]: <https://www.pcgamer.com/report-alan-wake-remastered-and-final-fantasy-7-remake-coming-to-the-epic-games-store/>
[vgc-ff7r-awr]: <https://www.videogameschronicle.com/news/alan-wake-remastered-and-final-fantasy-7-remake-listings-spotted-on-the-epic-games-stores-database/>
