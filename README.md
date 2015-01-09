# csv2sqlite
Convert CSV files to a sqlite3 database.

The table name is the csv file name (without the .csv extension). The first row is treated as the header for all columns.

This script was originally written for the purpose of converting an excel file into a sqlite database for inclusion in an Android app. For this reason it performs the following extra functions:
* converting empty values to null
* adding an `android_metadata` table to the database 
* adding a `__id` primary key column to each table.

Goes well together with [android-sqlite-asset-helper](https://github.com/jgilfelt/android-sqlite-asset-helper).

# Usage
    python2 csv2sqlite.py my_fabulous_data.csv
    
# Example
    $ cat airlines.csv
    Code;Airline;Country
    LH;Lufthansa;Germany
    BA;British Airways;United Kingdom
    
    $ python2 csv2sqlite.py airlines.csv airlines.db
    Making table airlines with 3 columns
    Imported 3 rows into airlines.db
    
    $ sqlite3 airlines.db
    sqlite> ...
    sqlite> select * from airline_data
    __id    Code    Airline            Country
    1       LH      Lufthansa          Germany
    2       BA      British Airways    United Kingdom


