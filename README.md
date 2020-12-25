# Tomorrow Bank Statement Converter

## What is this about?

[Tomorrow Bank](https://www.tomorrow.one/) is a great German Online Bank with a Green policy. Unfortunately, its implemenation of PSD2 compliance does not allow accessing bank accounts other than from one application, i.e. their mobile app. This prevents sychronization of bank transfers into banking applications such as [Money Money](https://moneymoney-app.com/).



This project aims to implement a parser that consumes Tomorrow's monthly statement PDF and converts it into a CSV file to be imported in Money Money.

## How to use?

### Installation

```shell
$ pip install .
# or for MacOS
$ pip3 install .
```

### Run

```shell
$ tconverter bankstatement.pdf
```

This will create a `bankstatement.csv` file in the same location.

### Manual

```
usage: tconverter [-h] file_path

positional arguments:
  file_path

optional arguments:
  -h, --help  show this help message and exit
```

