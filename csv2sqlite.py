# Converts a CSV file (typically exported from individual .xls sheets) to a sqlite db as a new table
#
# - The CSV filename (without .csv extension) is used as the table name.
# - The columns from the first row are used as column names in the table.
# - You can store multiple tables (from multiple csv files) in the same sqlite3 db
# - The table will contain an __id primary key and an android_metadata table to make it android-compatible.
# - Typically the .db file should be zipped and copied to <android-project>/assets
#
# Usage: python2 csv2sqlite.py my_fabulous_data.csv db.sqlite
#
# Author: Nachiket Apte <napte@sapient.com>

import csv, sqlite3, sys, os

try: 
    filename = sys.argv[1]
except IndexError: 
    print 'Missing argument: python csv2sqlite.py <tablename.csv>'
    sys.exit(2)
try: 
    sqlitefilename = sys.argv[2]
except IndexError: 
    print 'Using default name for db: mydb.sqlite'
    sqlitefilename = "mydb.sqlite"

# open our csv file for parsing. We use a standard db filename which may contain 
# multiple tables from different csv files
reader = csv.reader(open(filename, 'r'), delimiter=';')
table, fileExtension = os.path.splitext(filename)

conn = sqlite3.connect(sqlitefilename)
curs = conn.cursor()

# Android-specific shizz. Remove if not relevant
curs.execute("DROP TABLE IF EXISTS android_metadata")
curs.execute("CREATE TABLE IF NOT EXISTS android_metadata (locale TEXT DEFAULT 'en_US')")
curs.execute("INSERT INTO 'android_metadata' VALUES ('en_US')")
##

counter = 0

# Screw fancy functions, I'm a python noob
tableInsertValues = "?";
tableInsertSql = "INSERT INTO " + table + " (__id"

for row in reader:
    if counter == 0:
        # first row of csv, create table based on columns
        colNameCreateString = ""
        for colName in row:
            # No spaces in column names. All other formatting is preserved
            colName = colName.replace(' ', '')
            
            # All columns are strings, good luck future developers
            colNameCreateString += ", " + colName + " TEXT"
            
            # Magic here
            tableInsertSql += ", " + colName
            tableInsertValues += ", ?"
        
        # make our insert statement based on the column values
        tableInsertSql += ") VALUES (" + tableInsertValues + ");"
        
        # make and execute our create statement
        curs.execute("DROP TABLE IF EXISTS " + table)
        print "Making table " + table + " with " + str(len(row)) + " columns"
        try:
            curs.execute("CREATE TABLE IF NOT EXISTS " + table + " ( __id INTEGER PRIMARY KEY" + colNameCreateString + ");")
        except sqlite3.OperationalError:
                # Some .xls files might be missing a title row
                print "First row must contain headers! This one contains " + str(row)
                sys.exit(2)
    else:
        # insert row as data
        to_db = [counter]
        for colVal in row:
            colVal = colVal.strip(); # trim
            if len(colVal) == 0:
                # excel is dumb sometimes, convert empty strings to null values
                to_db.append(None)
            else:
                to_db.append(unicode(colVal.strip(), "utf8"))
        curs.execute(tableInsertSql, to_db)
    
    counter += 1
conn.commit()
print "Imported " + str(counter - 1) + " rows into " + sqlitefilename