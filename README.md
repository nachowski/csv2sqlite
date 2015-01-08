# csv2sqlite
Convert CSV files to a sqlite3 database.

The table name is the csv file name (without the .csv extension). The first row is treated as the header for all columns.

This script is for the particular use case where you want to convert an excel file into a sqlite database for inclusion in an Android app. For this reason it handles a few edge cases such as converting empty values to null or adding a `__ID` column to each table.

# Usage
    python2 csv2sqlite.py my_fabulous_data.csv
