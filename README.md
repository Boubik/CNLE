# Czech National Library Extractor

## Description

The National Library Extractor is a Python project specifically designed for the Czech National Library. It allows users to generate a CSV file containing information about books based on a search query provided through a link from the National Library. This project is useful for researchers, librarians, and anyone interested in accessing and organizing book data from the Czech National Library.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [License](#license)

## Installation

1. Clone the repository: `git clone https://github.com/Boubik/CNLE.git`
1. Navigate to the project directory: `cd CNLE`
1. Install the venv: `pip install virtualenv` for older then 3.6 Python version
1. Make virtual Python: `python -m venv venv`
1. Use virtual Python: `source venv/bin/activate` for Unix like systems or `venv\Scripts\activate.bat` for Windows
1. Install the required dependencies: `pip install -r requirements.txt`
1. Setup mail with [guide](https://app.sendgrid.com/guide/integrate/langs/python)

## Features

- Extract data from the Czech National Library
- Save data to a CSV file
- Deduplication (beta feature)

## License

This project is licensed under the [MIT License](LICENSE).
