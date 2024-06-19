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
   pip install pandas openpyxl
   

## Usage

1. Ensure the dataset.xlsx file is in the same directory as the script.
2. Run the script:
   bash
   python script.py
   
3. The script will generate the companies_and_subcompanies.xlsx file with the identified main companies and subsidiaries.

## Dataset Structure

- *multicompanies*: Contains information about main companies and subsidiaries.
- *workers*: Contains information about workers and their companies.

## Output

The script generates an Excel file with two sheets:

- *Companies*: Main companies without matches in 'multicompanies'.
- *SubCompanies*: Subsidiaries with matches in 'sub_company_id'.

## License

This project is licensed under the MIT License.
