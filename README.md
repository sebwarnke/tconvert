# tconvert - A Tomorrow Bank Statement Converter

## What is this about?

[Tomorrow Bank](https://www.tomorrow.one/) is a great German Online Bank with a ESG policy. Unfortunately, its implemenation of PSD2 compliance does not allow accessing bank accounts other than from one application, i.e. their mobile app. This prevents sychronization of bank transfers into banking applications such as [Money Money](https://moneymoney-app.com/).



The converter consumes PDF bank statement that can be downloaded from Tomorrow App and converts them into a CSV file that Money Money is capable of importing.

## How to use?

### Installation

```shell
$ pip install .
# or for MacOS
$ pip3 install .
```

### Running

```shell
$ tconvert bankstatement.pdf
# or, in case you want to run it against multiple files in a directory
$ find -name *.pdf -exec tconvert {} \;
```

This will create a `bankstatement.csv` file in the same location.

### Manual

```
usage: tconvert [-h] file_path

positional arguments:
  file_path

optional arguments:
  -h, --help  show this help message and exit
```

