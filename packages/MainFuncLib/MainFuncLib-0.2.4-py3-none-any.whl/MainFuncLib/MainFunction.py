# Import required libraries
import datetime
import time
from polygon.rest import RESTClient # Make sure to have the latest API client of Polygon installed
from sqlalchemy import create_engine
from sqlalchemy import text
from math import sqrt
import matplotlib.pyplot as plt
from numpy import mean
from numpy import std
from math import floor

"""
Function slightly modified from polygon sample code to format the date string 

Arguments:
    - ts: last_trade.timestamp (timestap from the last_trade object)

Returns:
    - datetime object
"""
def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M:%S')


"""
Function which clears the raw data tables once we have aggregated the data in a 6 minute interval and resets the number of
crosses, max and min parameters for the Keltner Channels.

Arguments:
    - engine: Engine object from sqlalchemy

    - currency_pairs: Nested list with all the information about each currency pair

Returns:
    - None
"""
def reset_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text("DROP TABLE " + curr[0] + curr[1] + "_raw;"))
            conn.execute(
                text("CREATE TABLE " + curr[0] + curr[1] + "_raw(ticktime text, fxrate  numeric, inserttime text);"))

            # reset number of crosses, band_nb and max, min
            # Assumption: we start each time in band nb 0, not 100% correct, but should not lead to big differences
            curr[2] = 0
            curr[3] = 0
            curr[6] = 0
            curr[7] = 9999  # min is set to a random high number


"""
This creates a table for storing the raw, unaggregated price data for each currency pair in the SQLite database

Arguments:
    - engine: Engine object from sqlalchemy

    - currency_pairs: Nested list with all the information about each currency pair

Returns:
    - None
"""
def initialize_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(
                text("CREATE TABLE " + curr[0] + curr[1] + "_raw(ticktime text, fxrate  numeric, inserttime text);"))


"""
This creates a table for storing the (6 min interval) aggregated price data for each currency pair in the SQLite database and
a table for storing the parameteres related to the Keltner Channels

Arguments:
    - engine: Engine object from sqlalchemy

    - currency_pairs: Nested list with all the information about each currency pair

Returns:
    - None
"""
def initialize_aggregated_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text("CREATE TABLE " + curr[0] + curr[1] + "_agg(inserttime text, avgfxrate numeric);"))

            # Create extra table per currency pair to keep track of max, min, VOL, mean and FD
            conn.execute(text("CREATE TABLE " + curr[0] + curr[
                1] + "_maxmin(max numeric, min numeric, VOL numeric, mean numeric, FD numeric);"))


"""
This function is called every 6 minutes to aggregate the data, store it in the aggregate table, and then delete the raw data

Arguments:
    - engine: Engine object from sqlalchemy

    - currency_pairs: Nested list with all the information about each currency pair

    - count: Integer, used to check if is the first time calling this function

Returns:
    - None

"""
def aggregate_raw_data_tables(engine, currency_pairs, count):
    with engine.begin() as conn:
        for curr in currency_pairs:

            # Gives back an a Result object. (See: https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
            result = conn.execute(
                text("SELECT AVG(fxrate) as avg_price, COUNT(fxrate) as tot_count FROM " + curr[0] + curr[1] + "_raw;"))
            for row in result:
                avg_price = row.avg_price
                mean = row.avg_price

            date_res = conn.execute(text("SELECT MAX(ticktime) as last_date FROM " + curr[0] + curr[1] + "_raw;"))
            for row in date_res:
                last_date = row.last_date

            conn.execute(text(
                "INSERT INTO " + curr[0] + curr[1] + "_agg (inserttime, avgfxrate) VALUES (:inserttime, :avgfxrate);"),
                         [{"inserttime": last_date, "avgfxrate": avg_price}])

            # vol = max - min
            vol = curr[6] - curr[7]
            # previous vol
            curr[4] = vol
            # previous mean
            curr[5] = mean

            # Prevent division by 0 error and set first FD to null
            if count == 360 or vol == 0:
                frac_dem = None
            else:
                frac_dem = curr[3] / vol

            conn.execute(text("INSERT INTO " + curr[0] + curr[
                1] + "_maxmin (max, min, VOL, mean, FD) VALUES (:max, :min, :VOL, :mean, :FD);"),
                         [{"max": curr[6], "min": curr[7], "VOL": vol, "mean": mean, "FD": frac_dem}])


"""
This the sanity check for the returned values of Polygon. I noticed that Polygon sometimes returns an incorrect value that is 
almost exact the same as 1/correct. This makes me believe that Polygon probably sometimes switches the from and to currency.

I use the reasoning that it is statiscally very unlikely that avg_price > prev_mean + 750*0.025*prev_vol and,
avg_price < prev_mean - 750*0.025*prev_vol

Arguments:
    - client: Object of Polygon client

    - avg_price: Float, avg price of currency pair

    - prev_mean: Float, previous mean price 

    - prev_vol: Float, previous volatility

    - from_: Float, the from_ currency

Returns:
    - avg_price

"""
def filter_out_incorrect_values(client, avg_price, prev_mean, prev_vol, from_):
    while (((avg_price > prev_mean + 750 * 0.025 * prev_vol or avg_price < prev_mean - 750 * 0.025 * prev_vol)) or \
           (from_ == "EUR" and avg_price < prev_mean - 0.095)) and prev_vol != 0:
        print("Incorrect value:", avg_price)
        try:
            resp = client.get_real_time_currency_conversion(from_, to, amount=100, precision=2)
        except:
            continue
        last_trade = resp.last
        avg_price = (last_trade.bid + last_trade.ask) / 2

    return avg_price


"""
This main function repeatedly calls the polygon api every 1 seconds for 10 hours and stores the results.

Arguments:
    - currency_pairs: Nested list with all the information about each currency pair
"""
def mainFunc(currency_pairs, time):
    # The api key given by the professor
    key = "beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq"

    # Number of list iterations - each one should last about 1 second
    count = 0
    agg_count = 0

    # Create an engine to connect to the database; setting echo to false should stop it from logging in std.out
    engine = create_engine("sqlite+pysqlite:///sqlite/final.db", echo=False, future=True)

    # Create the needed tables in the database
    initialize_raw_data_tables(engine, currency_pairs)
    initialize_aggregated_tables(engine, currency_pairs)

    # Open a RESTClient for making the api calls
    client = RESTClient(key)

    # Loop that runs until the total duration of the program hits 10 hours (= 36000 seconds).
    while count < time:

        # Make a check to see if 6 minutes has been reached or not
        if agg_count == 360:
            # Aggregate the data and clear the raw data tables
            aggregate_raw_data_tables(engine, currency_pairs, count)
            reset_raw_data_tables(engine, currency_pairs)
            agg_count = 0

        # Only call the api every 1 second, so wait here for 0.28 seconds, because the
        # code takes about .72 seconds to run
        # Tune this if you want run for less currency pairs or modify the code
        time.sleep(0.28)

        # Increment the counters
        count += 1
        agg_count += 1

        # Loop through each currency pair
        for currency in currency_pairs:
            # Set the input variables to the API
            from_ = currency[0]
            to = currency[1]

            # Call the API with the required parameters
            try:
                resp = client.get_real_time_currency_conversion(from_, to, amount=100, precision=2)
            except:
                continue

            # This gets the Last Trade object defined in the API Resource
            last_trade = resp.last

            # Format the timestamp from the result
            dt = ts_to_datetime(last_trade.timestamp)

            # Get the current time and format it
            insert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Calculate the price by taking the average of the bid and ask prices
            avg_price = (last_trade.bid + last_trade.ask) / 2

            # set needed parameters
            prev_vol = currency[4]
            prev_mean = currency[5]
            curr_max = currency[6]
            curr_min = currency[7]

            avg_price = filter_out_incorrect_values(client, avg_price, prev_mean, prev_vol, from_)

            if last_trade.ask > curr_max:
                # Update current maximum
                currency[6] = last_trade.ask

            elif last_trade.bid < curr_min:
                # Update current minimum
                currency[7] = last_trade.bid

                # Assumption point on a band is not a cross, has to be > or <

            # Keltner bands, count the number of crosses in realtime
            prev_band_nb = currency[2]

            # Formula used to calculate the band nb:
            # band_nb = floor((abs(avg_price - prev_mean))/(0.025*prev_vol))

            if avg_price > prev_mean + 0.025 * prev_vol and prev_vol != 0:
                band_nb = floor((avg_price - prev_mean) / (0.025 * prev_vol))

            elif avg_price < prev_mean - 0.025 * prev_vol and prev_vol != 0:
                band_nb = floor((avg_price - prev_mean) / (-0.025 * prev_vol))

            else:
                band_nb = 0  # lays within the keltner channel

            # Can't go over 100 for the band_nb
            band_nb = 100 if band_nb > 100 else band_nb

            # For debugging purposes:
            #             print("Curr1:", from_, "curr2:", to, "Band_nb:",currency[2])
            #             print("Curr1:", from_, "curr2:", to, "Nb_crosses:",currency[3])

            # Set new prev_band_nb and increment crosses counter
            currency[2] = band_nb
            currency[3] = currency[3] + abs(band_nb - prev_band_nb)

            # Write the data to the SQLite database, raw data tables
            with engine.begin() as conn:
                conn.execute(text(
                    "INSERT INTO " + from_ + to + "_raw(ticktime, fxrate, inserttime) VALUES (:ticktime, :fxrate, :inserttime)"),
                             [{"ticktime": dt, "fxrate": avg_price, "inserttime": insert_time}])