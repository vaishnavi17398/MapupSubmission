#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[12]:


def calculate_distance_matrix(df):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('dataset-3.csv')

    # Create a dictionary to store distances between toll locations
    distance_dict = {}

    # Populate the dictionary with distances
    for index, row in df.iterrows():
        start_id, end_id, distance = row['id_start'], row['id_end'], row['distance']

        # Add bidirectional distances
        distance_dict[(start_id, end_id)] = distance
        distance_dict[(end_id, start_id)] = distance

    # Create a DataFrame with unique toll locations as indices and columns
    toll_locations = sorted(set(df['id_start']).union(set(df['id_end'])))
    df = pd.DataFrame(index=toll_locations, columns=toll_locations)

    # Initialize the matrix with NaN values
    df = df.fillna(float('nan'))

    # Populate the distance matrix with cumulative distances along known routes
    for start_id in toll_locations:
        for end_id in toll_locations:
            if start_id == end_id:
                df.at[start_id, end_id] = 0
            elif pd.notna(df.at[start_id, end_id]):
                # If the distance is already known, continue to the next pair
                continue
            elif (start_id, end_id) in distance_dict:
                df.at[start_id, end_id] = distance_dict[(start_id, end_id)]
                df.at[end_id, start_id] = distance_dict[(end_id, start_id)]
            else:
                # Calculate cumulative distance along known routes
                known_distances = []
                for intermediate_id in toll_locations:
                    if pd.notna(df.at[start_id, intermediate_id]) and pd.notna(df.at[intermediate_id, end_id]):
                        known_distances.append(df.at[start_id, intermediate_id] + df.at[intermediate_id, end_id])

                if known_distances:
                    # Set the minimum known distance as the cumulative distance
                    df.at[start_id, end_id] = min(known_distances)
                    df.at[end_id, start_id] = min(known_distances)

    return df


# In[14]:


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # Create an empty list to store unrolled data
    unrolled_data = []

    # Iterate over the rows of the distance matrix
    for id_start, row in df.iterrows():
        for id_end, distance in row.items():
            # Exclude same id_start to id_end pairs
            if id_start != id_end:
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a new DataFrame from the unrolled data
    df = pd.DataFrame(unrolled_data)

    return df


# In[16]:


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    # Filter rows with the given reference ID in the id_start column
    reference_rows = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference ID
    average_distance = reference_rows['distance'].mean()

    # Calculate the threshold range (10% of the average distance)
    threshold_range = 0.1 * average_distance

    # Filter rows where the distance is within the threshold range
    df = df[(df['id_start'] != reference_id) & (df['distance'] >= average_distance - threshold_range) & (df['distance'] <= average_distance + threshold_range)]


    return df


# In[20]:


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Add columns for toll rates based on vehicle types
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

