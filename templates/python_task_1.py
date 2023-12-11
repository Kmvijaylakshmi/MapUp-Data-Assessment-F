import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
     # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    df2 = df.fillna(0)


    # Create a pivot table with 'id_1' as index, 'id_2' as columns, and 'car' as values
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill diagonal values with 0
    np.fill_diagonal(car_matrix.values, 0)


    return car_matrix
    print(car_matrix)
# Example usage:
# Assuming your CSV file is named 'dataset-1.csv'
car_matrix = generate_car_matrix('/dataset-1.csv')
print(car_matrix)


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
 # Add a new categorical column 'car_type'
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_count = dict(sorted(type_count.items()))

    return type_count

# Example usage:
# Assuming df is your DataFrame from 'dataset-1.csv'
df = pd.read_csv('/dataset-1.csv')
result = get_type_count(df)
print(result)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
 # Read the CSV file into a DataFrame
    df = pd.read_csv('/dataset-1.csv')

    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Example usage:
# Assuming your CSV file is named 'dataset-1.csv'
result = get_bus_indexes('dataset-1.csv')
print(result)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

     # Read the CSV file into a DataFrame
    df = pd.read_csv('/dataset-1.csv')

    # Calculate the average of 'truck' values for each 'route'
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of routes in ascending order
    filtered_routes.sort()

    return filtered_routes

# Example usage:
# Assuming your CSV file is named 'dataset-1.csv'
result = filter_routes('dataset-1.csv')
print(result)


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
import pandas as pd

def multiply_matrix(car_matrix):
    """
    Modify values in the DataFrame based on the specified logic.

    Args:
        car_matrix (pandas.DataFrame): Input DataFrame.

    Returns:
        pandas.DataFrame: Modified DataFrame with values rounded to 1 decimal place.
    """
    # Create a copy of the input DataFrame to avoid modifying the original
    modified_matrix = car_matrix.copy()

    # Apply the specified logic to modify values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Example usage:
# Assuming you have the DataFrame 'car_matrix' from Question 1
modified_result = multiply_matrix(car_matrix)
print(modified_result)
    


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
# Convert start and end timestamps to datetime objects
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'],errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'],errors='coerce')

    # Extract day of the week and hour from start and end timestamps
    df['start_day_of_week'] = df['start_timestamp'].dt.dayofweek
    df['end_day_of_week'] = df['end_timestamp'].dt.dayofweek
    df['start_hour'] = df['start_timestamp'].dt.hour
    df['end_hour'] = df['end_timestamp'].dt.hour

    # Group by (id, id_2)
    grouped = df.groupby(['id', 'id_2'])

    # Check completeness for each group
    completeness = grouped.apply(lambda group: time_check(group))

    return completeness

def check_group_completeness(group):
    # Check if the start timestamps cover a full 24-hour period
    start_hour_coverage = set(group['start_hour'])
    full_start_hour_coverage = set(range(24)) == start_hour_coverage

    # Check if the end timestamps cover a full 24-hour period
    end_hour_coverage = set(group['end_hour'])
    full_end_hour_coverage = set(range(24)) == end_hour_coverage
     # Check if the start timestamps span all 7 days of the week
    start_day_of_week_coverage = set(group['start_day_of_week'])
    full_start_day_of_week_coverage = set(range(7)) == start_day_of_week_coverage

    # Check if the end timestamps span all 7 days of the week
    end_day_of_week_coverage = set(group['end_day_of_week'])
    full_end_day_of_week_coverage = set(range(7)) == end_day_of_week_coverage

    # Return True if all conditions are satisfied, indicating completeness
    return (
        full_start_hour_coverage and full_end_hour_coverage and
        full_start_day_of_week_coverage and full_end_day_of_week_coverage
    )

# Example usage:
csv_file_path = '/dataset-2.csv'
df = pd.read_csv(csv_file_path)
