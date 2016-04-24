#!/usr/bin/env python

"""Script to pull data from New Relic Insights and dump it into a CSV file

You will need to edit the contents of config.py to customize the script
but should not need to change anything in this file itself.

"""

from config import *
import simplejson as json
import csv
import logging
import time
import urllib
import urllib2
import json
import sys
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILENAME % (time.time()))
logger.addHandler(handler)


def query_newrelic(query):
    query = urllib.quote_plus(' '.join(query.split()))
    url = 'https://insights-api.newrelic.com/v1/accounts/' + INSIGHTS_ACCOUNT_ID + '/query?nrql=' + query
    headers = {'X-Query-Key': INSIGHTS_QUERY_KEY}

    req = urllib2.Request(url, [], headers)
    response = urllib2.urlopen(req)
    json_data = response.read()
    results = json.loads(json_data)

    return results['results'][0]['events']


def main():
    """Main program routine

    """
    start = START_TIME
    end = START_TIME + timedelta(seconds=STEP_AMOUNT_IN_SECONDS)
    header_printed = False
    total = 0

    file_args = 'ab' if APPEND_TO_CSV else 'wb'
    with open(OUTPUT_FILENAME, file_args) as csvfile:
        output = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        while end <= END_TIME:
            query2 = INSIGHTS_QUERY % (str(start), str(end))
            results = query_newrelic(query2)
            if len(results) > 999:
                logger.info('Found 1000 record dataset. It is likely there is now data missing. '
                            'Decrement STEP_AMOUNT_IN_SECONDS and try again')
                if EXIT_ON_1000_RECORDS:
                    sys.exit()
            total += len(results)
            logger.info('Total: %s rows found through %s' % (total, str(end)))

            # Print data into the CSV
            for row in results:
                if not header_printed:
                    output.writerow(row.keys())
                    header_printed = True
                output.writerow(row.values())

            start = start + timedelta(seconds=STEP_AMOUNT_IN_SECONDS)
            end = end + timedelta(seconds=STEP_AMOUNT_IN_SECONDS)

            # We must always end on END_TIME or we miss records
            if end > END_TIME and (end - timedelta(seconds=STEP_AMOUNT_IN_SECONDS)) != END_TIME:
                end = END_TIME
        logger.info('All done')

if __name__ == "__main__":
    main()
