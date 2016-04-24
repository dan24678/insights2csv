insights2csv
============

insights2csv.py allows for easy creation of CSV files from data
pulled from New Relic Insights via their API.

Use Case
---------

New Relic Insights provides basic querying ability via NRQL. However,
NRQL does not allow joins, self-joins, sub-queries and numerous
other advanced features that are standard in more powerful relational
databases. Thus, Insights users may often see a need to dump data from
their Insights tables into a relational DB to run various single-use
queries or data mining exercises. insights2csv.py allows easy extraction
of Insights data into a CSV file, from where it can be imported into
the DB of your choice. 

If you're on OS-X, I'd strongly recommend looking at [Postgres.app](http://postgresapp.com/)
for analyzing your New Relic data. It lets you get a Postgres DB
installed, configured and running in about 3 minutes. 

Basic Workflow
--------------

 1. Edit config.py and enter your New Relic credentials and specify
 the columns, table and timeframe you wish to extract.
 2. Run the script: /path/to/folder/insights2csv.py
 3. Connect to your database
 4. Issue the CREATE TABLE statement to make an empty table with all
 required columns. I recommend BIGINT for timestamps and TEXT types
 for most other columns.
 5. CREATE INDEX statements for all needed indexes.
 6. Import the insights data into the database from the CSV. In Postgres
 the command to do this is as follows:
 `COPY tablename FROM '/path/to/insights-data.csv' (delimiter ',');`
 7. Start slicing and dicing your insights data with all the power of a
 relational DB or data warehouse!!!

Advanced Stuff in config.py
---------------------------

Hopefully, the comments in config.py are self-explanatory but here are
some extra info on each, if you need it.

### INSIGHTS\_ACCOUNT\_ID and INSIGHTS\_QUERY\_KEY
These can be found inside your New Relic account. If you fork insights2csv
don't commit your credentials to a public repo!

### INSIGHTS\_QUERY
This is the query you want to run to extract the Insights data. You should
be explicit about which columns you want to retrieve and do not
use SELECT *. The reason for this is that SELECT * may return different
columns in each result set and you'll end up with a completely broken
CSV. Also, you must leave the last line (SINCE '%s' UNTIL '%s' LIMIT 1000)
unchanged so the Insights data can be paginated.

### START\_TIME and END\_TIME
insights2csv works by paginating the data based on the SINCE/UNTIL 
timestamps. For this reason, if your data exceeds 1000 data points per
second, you won't be able to use insights2csv to get at all your data.
You should use a very small interval between `START_TIME` and `END_TIME`
when you first start testing the script (say, 1 minute) to ensure everything works and
that you are using the best possible value for `STEP_AMOUNT_IN_SECONDS`.
These values are ordered like a timestamp: year, month, day, hour, minute,
second.

### STEP\_AMOUNT\_IN\_SECONDS
This step time must be set to determine how the data will be paginated
when querying Insights. Since the query will only return 1000 records
at a time, this value should be as large as possible without triggering
the 1000 item threshold. It defaults to 1, which will run very slow but
is the most widely compatible value. You may want to start at a higher
value and keep tabs on the script to see if it dies to find the perfect
balance.

### EXIT\_ON\_1000\_RECORDS
Default behavior is for the script to die when it sees 1000 records.
This lets you fine-tune the `STEP_AMOUNT_IN_SECONDS` to find the right
value for your data. If you don't care about missing data, you can
change this to False.

### APPEND\_TO\_CSV
Default behavior is to create a new CSV everytime the program is run.
If the program died (such as from a `STEP_AMOUNT_IN_SECONDS` value that
was too high) you can change `APPEND_TO_CSV` to True and adjust
`STEP_AMOUNT_IN_SECONDS` and `START_TIME` to pick up where the program died.

### OUTPUT\_FILENAME
This is the name of the CSV that will be produced

### LOG\_FILENAME
The name of the logfile. %s will be the timestamp

