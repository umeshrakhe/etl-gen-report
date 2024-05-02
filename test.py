import time
import pandas as pd


def test_1():
    # Sample dataset (replace this with your actual dataset loading mechanism)
    data = {
        'date': pd.date_range(start='2020-01-01', end='2024-12-31', freq='D'),
        'value': range(1, len(pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')) + 1)
    }
    df = pd.DataFrame(data)

    # Function to filter data based on date range
    def filter_data_by_date_range(df, start_date, end_date):
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Sample date range
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    # Filter data
    filtered_data = filter_data_by_date_range(df, start_date, end_date)

    # Output filtered data
    #print(filtered_data)

def test_2():
    # Sample dataset (replace this with your actual dataset loading mechanism)
    data = {
        'date': pd.date_range(start='2020-01-01', end='2024-12-31', freq='D'),
        'value': range(1, len(pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')) + 1)
    }
    df = pd.DataFrame(data)

    # Convert date column to datetime if not already done
    df['date'] = pd.to_datetime(df['date'])

    # Set date column as index
    df.set_index('date', inplace=True)

    # Sample date range
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    # Filter data using index slicing
    filtered_data = df[start_date:end_date]

    # Output filtered data
    #print(filtered_data)


if __name__ == "__main__":
    start = time.time()
    print("hello")
    test_1()
    end = time.time()
    print(end - start)
    print("-----------------------------------------")
    start = time.time()
    print("hello")
    test_2()
    end = time.time()
    print(end - start)
    