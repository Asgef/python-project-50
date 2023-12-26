<div align="center">

<h1>Hexlet project: Difference Generator</h1>

program that determines the difference between two data structures

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Asgef/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Asgef/python-project-50/actions) [![linter-test](https://github.com/Asgef/python-project-50/actions/workflows/main.yml/badge.svg)](https://github.com/Asgef/python-project-50/actions/workflows/main.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/d41463e860801f3c92da/maintainability)](https://codeclimate.com/github/Asgef/python-project-50/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/d41463e860801f3c92da/test_coverage)](https://codeclimate.com/github/Asgef/python-project-50/test_coverage)

</div>

## Description

This project was created as part of the "Python Developer" course on the [Hexlet educational platform](https://hexlet.io). Difference Generator, an application that calculates the difference between two data structures, such as JSON or YAML. The representation of the differences is output in a convenient format for studying or processing data.

#### Sopported format

- JSON
- YAML

#### Output text

- Tree style text
- Plain text
- JSON


## Requirements
Python 3.11 or higher  
pip 23 or higher  
git 2.34 or higher

## Installation
    

    python3 -m pip install --user git+https://github.com/Asgef/python-project-50.git

## Usage

"The application is used both as a **command line interface (CLI) tool** and as an **external library**."


### As a Command Line Interface tool

    gendiff [-f file_format] file_path1 file_path2

or

    gendiff [--format file_format] file_path1 file_path2
    
### As an external library

    from gendiff import generate_diff  
    diff = generate_diff(file_path1, file_path2, file_format)


## Demonstration

### Stylish format

#### Comparison of 2 flat files:

[![asciicast](https://asciinema.org/a/V9kM8csaoldL2BOQH0xGdD9b5.svg)](https://asciinema.org/a/V9kM8csaoldL2BOQH0xGdD9b5)

#### Comparison of 2 nested files:

[![asciicast](https://asciinema.org/a/J8oPJ6cTocyXii8w9LEFy6JJY.svg)](https://asciinema.org/a/J8oPJ6cTocyXii8w9LEFy6JJY)

### Plain format

#### Comparison of 2 flat files:

[![asciicast](https://asciinema.org/a/VRHANtxM4tjEfUuNDN9wp99SB.svg)](https://asciinema.org/a/VRHANtxM4tjEfUuNDN9wp99SB)

#### Comparison of 2 nested files:

[![asciicast](https://asciinema.org/a/0qCF7BoDBA5Yt28NJtaglM60D.svg)](https://asciinema.org/a/0qCF7BoDBA5Yt28NJtaglM60D)

### JSON format

[![asciicast](https://asciinema.org/a/ZDKS2UItKhZitU2aUtqfNU4I3.svg)](https://asciinema.org/a/ZDKS2UItKhZitU2aUtqfNU4I3)

#### Comparison of 2 nested files:

[![asciicast](https://asciinema.org/a/AdjcW0NZ4dG9BoNsyEtE17Gku.svg)](https://asciinema.org/a/AdjcW0NZ4dG9BoNsyEtE17Gku)
