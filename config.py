import datetime
# ##
# SET THE FOLLOWING CONSTANTS TO CONFIGURE WHAT GETS LOADED.
# ##

# Your Insights credentials go here
INSIGHTS_ACCOUNT_ID = '123456'
INSIGHTS_QUERY_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# This is the query you want to run. DO NOT USE: SELECT *
# Also, leave the last line (SINCE '%s' UNTIL '%s' LIMIT 1000) AS IS!!
# Otherwise, you should be able to customize as needed.
INSIGHTS_QUERY = '''
      SELECT appId, appName, duration, error
      FROM Transaction WHERE host LIKE '%staging%'
      SINCE '%s' UNTIL '%s' LIMIT 1000
    '''

# Here you define the date range for the data you want to pull in
# These are required arguments. These values are ordered like a timestamp:
# year, month, day, hour, minute, second.
START_TIME = datetime.datetime(2016, 4, 13, 19, 49, 20)
END_TIME = datetime.datetime(2016, 4, 13, 19, 50, 20)

# This step time must be set to determine how the data will be paginated
# when querying Insights. Since the query will only return 1000 records
# at a time, this value should be as large as possible without triggering
# the 1000 item threshold. It defaults to 1, which will run very slow but
# is the most widely compatible value.
STEP_AMOUNT_IN_SECONDS = 1

# Default behavior is for the script to die when it sees 1000 records.
# If you don't care about missing data, you can change this to False.
EXIT_ON_1000_RECORDS = True

# Default behavior is to create a new CSV everytime the program is run
# If the program died (such as from a STEP_AMOUNT_IN_SECONDS value that
# was too high) you can change APPEND_TO_CSV to True and adjust
# STEP_AMOUNT_IN_SECONDS and START_TIME to pick up where the program died.
APPEND_TO_CSV = False

# This is the name of the CSV that will be produced
OUTPUT_FILENAME = 'insights-data.csv'

# The name of the logfile. %s will be the timestamp
LOG_FILENAME = 'insights2csv-%s.log'
