# HACKADISC - LOS NOCTULITOS

## Description

This Python script analyzes a dataset.xlsx file to identify main companies and subsidiaries. It then generates a companies_and_subcompanies.xlsx file that can be used as a seeder for a database.

## Requirements

- Python 3.x
- pandas
- openpyxl

## Installation

1. Clone this repository.
2. Install the dependencies with:
   bash
   pip install pandas sqlalchemy openpyxl

## Usage

1. Ensure the dataset.xlsx file is in the same directory as the script.
2. Run the script:
   bash
   python main.py
3. The script will generate the companies_and_subcompanies.xlsx file with the identified main companies and subsidiaries.

## Dataset Structure

- _multicompanies_: Contains information about main companies and subsidiaries.
- _workers_: Contains information about workers and their companies.

## Output

The script generates an Excel file with two sheets:

- _Companies_: Main companies without matches in 'multicompanies'.
- _SubCompanies_: Subsidiaries with matches in 'sub_company_id'.

The script generates data in a sqlite database called 'hackadisc':

- _Companies_
- _SubCompanies_

## License

This project is licensed under the MIT License.
