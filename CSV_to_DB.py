import sqlite3 as sl
import pandas as pd

# Create/Connect database
conn = sl.connect('tesla_amazon_stock.db')
curs = conn.cursor()

# Create our table if it doesn't already exist
# Manually specify table name, column names, and columns types
curs.execute('DROP TABLE IF EXISTS tesla')
curs.execute('CREATE TABLE IF NOT EXISTS '
             'tesla (`Volume` text, `Date` text, `Open` number)')
conn.commit()  # don't forget to commit changes before continuing

# Use pandas which you already to know to read the csv to df
# Select just the columns you want using optional use columns param
df = pd.read_csv('/Users/jeffreyju/Desktop/USC/Junior/ITP-216/final_project/csv_files/tesla.csv',
                 usecols=['Volume', 'Date', 'Open'])

# drop nulls just like pandas hw
df = df[df["Open"].notnull()]
df = df[df["Open"].notnull()]
df["YEAR"] = df["Date"].str[0:4]
print("Tesla Data: ")
print('First 3 df results:')
print(df.head(3))

# Let pandas do the heavy lifting of converting a df to a db
# name=your existing empty db table name
# con=your db connection object
# just overwrite if the values already there and don't index any columns
df.to_sql(name='tesla', con=conn, if_exists='replace', index=False)

# The rest is from the DB lecture and HW
print('\nFirst 3 db results:')
results = curs.execute('SELECT * FROM tesla').fetchmany(3)
for result in results:
    print(result)

result = curs.execute('SELECT COUNT(*) FROM tesla').fetchone()
# Note indexing into the always returned tuple w/ [0]
# even if it's a tuple of one
print('\nNumber of valid db rows:', result[0])
print('Number of valid df rows:', df.shape[0])

result = curs.execute('SELECT MAX(`OPEN`) FROM tesla').fetchone()
print('Max Observed Temp', result[0])


df = pd.read_csv('/Users/jeffreyju/Desktop/USC/Junior/ITP-216/final_project/csv_files/AMZN.csv',
                 usecols=['Volume', 'Date', 'Open'])

# drop nulls just like pandas hw
df = df[df["Open"].notnull()]
df = df[df["Open"].notnull()]
df["YEAR"] = df["Date"].str[0:4]
print("Amazon Data: ")
print('First 3 df results:')
print(df.head(3))

# Let pandas do the heavy lifting of converting a df to a db
# name=your existing empty db table name
# con=your db connection object
# just overwrite if the values already there and don't index any columns
df.to_sql(name='Amazon', con=conn, if_exists='replace', index=False)

# The rest is from the DB lecture and HW

print('\nFirst 3 db results:')
results = curs.execute('SELECT * FROM Amazon').fetchmany(3)
for result in results:
    print(result)

result = curs.execute('SELECT COUNT(*) FROM Amazon').fetchone()
# Note indexing into the always returned tuple w/ [0]
# even if it's a tuple of one
print('\nNumber of valid db rows:', result[0])
print('Number of valid df rows:', df.shape[0])

result = curs.execute('SELECT MAX(`OPEN`) FROM Amazon').fetchone()
print('Max Observed Temp', result[0])

