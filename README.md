# Daresbury Lab Open Day Heatmap

The aim of this repository is to display the interest of people through a heatmap of the Daresbury Lab, while adding a way for people to learn more about the stand they're viewing.

The way we're going to achieve this is through a series of QR codes dotted around each stand which, upon scanning, will take a person to a website giving more information about the stand (or the background/topic). Alongside redirecting the user to a website, scanning a QR code means that person will show up pseudo-anonymously on the heatmap.

## Tech Stack

Website:

- pnpm
- Typescript
- AstroJS

API:

- Python
- FastAPI
- SQLAlchemy

Database:

- Postgres

QR Creation:

- Python - Jupyter Notebook
- [segno](https://pypi.org/project/segno/)

Heatmap:

- TO BE ADDED

## Installation

Refer to individual component READMEs.

## Contribution

Refer to individual component READMEs.

## Manifest

- QR_codes folder contains the prototype QR code generating Python scripts.
- documentation folder contains supporting information from STFC.
