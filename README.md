# Czech National Library Extractor

## Description

The Czech National Library Extractor is a Python-based project tailored for extracting data from the Czech National Library's catalog. It enables users to generate a CSV file containing book information derived from a search query link provided by the National Library. This tool is particularly beneficial for researchers, librarians, and anyone interested in efficiently accessing and managing book data from the Czech National Library.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Boubik/CNLE.git
   ```

1. Navigate to the project directory: `cd CNLE`

   ```bash
   cd CNLE
   ```

1. If you are using Python 3.5 or older, install virtualenv:

   ```bash
   pip install virtualenv

   ```

1. Make virtual Python: `python -m venv venv`

   ```bash
    python -m venv venv  # For Python 3.6 and newer
    # or
    virtualenv venv      # For Python 3.5 and older
   ```

1. Use virtual Python: `source venv/bin/activate` for Unix like systems or `venv\Scripts\activate.bat` for Windows

    - For Unix-like systems:

        ```bash
        source venv/bin/activate
        ```

    - For Windows:

        ```powershell
        venv\Scripts\activate.bat
        ```

1. Install the required dependencies: `pip install -r requirements.txt`

    ```bash
    pip install -r requirements.txt
    ```

1. Setup mail with SMTP server:
   - Copy the example configuration file: `cp config.py.example config.py`
   - Open the `config.py` file and set the following parameters:
     - `server`: SMTP server address
     - `port`: SMTP server port
     - `username`: SMTP server username
     - `password`: SMTP server password
1. Run the project:

      ```bash
      python app.py
      ```

1. Connects to localhost on the port 5000: [http://localhost:5000](http://localhost:5000)

## Features

- Extracts data from the Czech National Library.
- Saves data to a CSV file.
- Deduplication system (currently in beta).
- Hosted on [cnle.boubik.cz](https://cnle.boubik.cz), making it accessible as a web service.
- Sends extracted data directly to your email.

## License

This project is licensed under the [MIT License](LICENSE).
