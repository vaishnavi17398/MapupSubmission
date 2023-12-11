#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[38]:


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
    # Pivot the DataFrame to get the desired matrix
    df=pd.read_csv('dataset-1.csv')
    df.pivot(index='id_1', columns='id_2', values='car')

    # Set diagonal values to 0
    for i in range(min(df.shape[0], df.shape[1])):
        df.iloc[i, i] = 0

    return df


# In[88]:


def get_type_count(df)->dict:
    
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    def categorize_car_type(car_value):
        """
        Custom function to categorize 'car' values into types.

        Args:
        car_value: Value from the 'car' column.

        Returns:
        str: Car type ('low', 'medium', 'high').
        """
        df=pd.read_csv('dataset-1.csv')
        if car_value <= 15:
            return 'low'
        elif 15 < car_value <= 25:
            return 'medium'
        else:
            return 'high'
    
    df['car_type'] = df['car'].apply(categorize_car_type)
    
    # Calculate the count of occurrences for each 'car_type' category
    
    dict = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    
    dict = {k: v for k, v in sorted(dict.items())}

    return dict
    

   


# In[90]:


def get_bus_indexes(df)->list:
    """
    Identify and return the indices where the bus values are greater than twice the mean value.

    Args:
        df (pandas.DataFrame): Input DataFrame

    Returns:
        list: List of indices where bus values are greater than twice the mean.
    """
    # Calculate the mean value of the 'bus' column
    df=pd.read_csv('dataset-1.csv')
    mean_bus = df['bus'].mean()

    # Identify indices where bus values are greater than twice the mean
    list = df[df['bus'] > 2 * mean_bus].index.tolist()

    # Sort the indices in ascending order
    list.sort()

    return list


# In[95]:


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df=pd.read_csv('dataset-1.csv')
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    list = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    list.sort()

    return list

    


# In[102]:


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df=pd.read_csv('dataset-1.csv')
    df.pivot(index='id_1', columns='id_2', values='car')

    # Set diagonal values to 0
    for i in range(min(df.shape[0], df.shape[1])):
        df.iloc[i, i] = 0
    matrix = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    matrix = matrix.round(1)

    
    

    return matrix

